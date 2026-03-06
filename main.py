"""
LoraLink - Off-grid P2P LoRa Communication System
Main application file for ESP32 with LoRa radio
"""

import machine
import time
from radio import LoraRadio
from ui import Display
from keypad import KeypadHandler
from logger import MessageLogger

# Hardware Configuration
LORA_MOSI = 23
LORA_MISO = 19
LORA_SCK = 18
LORA_CS = 5
LORA_RST = 14
LORA_IRQ = 26

OLED_SDA = 21
OLED_SCL = 22

KEYPAD_PINS = [12, 13, 15, 2, 4, 32, 33, 25, 26, 27, 14, 16]  # 3x4 grid

def main():
    """Initialize and run LoraLink"""
    print("LoraLink initializing...")
    
    # Initialize radio
    radio = LoraRadio(
        mosi=LORA_MOSI,
        miso=LORA_MISO,
        sck=LORA_SCK,
        cs=LORA_CS,
        rst=LORA_RST,
        irq=LORA_IRQ
    )
    
    # Initialize display
    i2c = machine.I2C(1, scl=machine.Pin(OLED_SCL), sda=machine.Pin(OLED_SDA))
    display = Display(i2c)
    
    # Initialize keypad
    keypad = KeypadHandler(KEYPAD_PINS)
    
    # Initialize logger
    logger = MessageLogger()
    
    # Show startup message
    display.show_message("LoraLink Ready", "Waiting...")
    print("LoraLink Ready!")
    
    # Main event loop
    while True:
        try:
            # Check for incoming messages
            msg = radio.receive()
            if msg:
                display.show_incoming(msg)
                logger.save_message("RX", msg)
                print(f"Received: {msg}")
            
            # Check keypad input
            key = keypad.get_key()
            if key:
                display.handle_key(key)
            
            # Check for send command (e.g., # key)
            if display.ready_to_send():
                message = display.get_message()
                if message:
                    radio.send(message)
                    display.show_outgoing(message)
                    logger.save_message("TX", message)
                    print(f"Sent: {message}")
            
            time.sleep(0.1)
            
        except Exception as e:
            display.show_error(str(e))
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
