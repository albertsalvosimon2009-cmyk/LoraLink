"""
LoRa Radio Communication Module
Handles P2P message transmission and reception
"""

import machine
import time

class LoraRadio:
    """LoRa radio communication handler"""
    
    def __init__(self, mosi, miso, sck, cs, rst, irq):
        """Initialize LoRa radio module"""
        self.spi = machine.SPI(1, baudrate=10000000, polarity=0, phase=0,
                               mosi=machine.Pin(mosi), miso=machine.Pin(miso),
                               sck=machine.Pin(sck))
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.rst = machine.Pin(rst, machine.Pin.OUT)
        self.irq = machine.Pin(irq, machine.Pin.IN)
        
        self.cs.on()
        self.reset()
        self.init_lora()
        
    def reset(self):
        """Reset LoRa module"""
        self.rst.off()
        time.sleep(0.1)
        self.rst.on()
        time.sleep(0.1)
        
    def write_register(self, addr, value):
        """Write to LoRa register"""
        self.cs.off()
        self.spi.write(bytes([addr | 0x80]))
        self.spi.write(bytes([value]))
        self.cs.on()
        
    def read_register(self, addr):
        """Read from LoRa register"""
        self.cs.off()
        self.spi.write(bytes([addr & 0x7F]))
        data = self.spi.read(1)
        self.cs.on()
        return data[0]
    
    def init_lora(self):
        """Initialize LoRa parameters"""
        # Set to LoRa mode
        self.write_register(0x31, 0x80)  # RegOpMode - LoRa mode
        time.sleep(0.1)
        
        # Configure frequency (915 MHz)
        self.write_register(0x06, 0xE4)  # Frf MSB
        self.write_register(0x07, 0xC0)  # Frf Mid
        self.write_register(0x08, 0x00)  # Frf LSB
        
        # Configure modulation parameters
        self.write_register(0x1E, 0x74)  # RegModemConfig1 - SF7, BW125kHz
        self.write_register(0x1F, 0x70)  # RegModemConfig2
        self.write_register(0x26, 0x0C)  # RegModemConfig3
        
        # Set TX power
        self.write_register(0x09, 0xF0)  # RegPaConfig - max power
        
        # Enable RX continuous mode
        self.set_mode(0x05)
        
        print("LoRa initialized")
    
    def set_mode(self, mode):
        """Set LoRa operating mode (0x01=TX, 0x04=RX, 0x05=RXCONT)"""
        self.write_register(0x01, mode)
        time.sleep(0.1)
    
    def send(self, message):
        """Send message via LoRa"""
        if isinstance(message, str):
            message = message.encode()
        
        # Set TX mode
        self.set_mode(0x01)
        
        # Write message to FIFO
        self.write_register(0x0D, 0x00)  # FIFO base addr
        self.cs.off()
        self.spi.write(bytes([0x00 | 0x80]))
        self.spi.write(message)
        self.cs.on()
        
        # Set payload length
        self.write_register(0x22, len(message))
        
        # Wait for TX complete (poll IRQ)
        timeout = time.time() + 5
        while time.time() < timeout:
            if self.irq.value() == 0:
                time.sleep(0.1)
                break
            time.sleep(0.01)
        
        # Return to RX mode
        self.set_mode(0x05)
        print(f"Message sent: {message}")
    
    def receive(self):
        """Receive message from LoRa (non-blocking)"""
        # Check for RX done flag
        irq_flags = self.read_register(0x12)
        
        if irq_flags & 0x40:  # RxDone flag
            # Get payload length
            rx_length = self.read_register(0x13)
            
            # Read message from FIFO
            self.write_register(0x0D, self.read_register(0x10))  # Set FIFO pointer
            self.cs.off()
            self.spi.write(bytes([0x00]))  # FIFO addr
            message = self.spi.read(rx_length)
            self.cs.on()
            
            # Clear interrupt flags
            self.write_register(0x12, 0x40)
            
            return message.decode(errors='ignore')
        
        return None
