"""
LoraLink - Off-grid P2P LoRa Communication System
Main application file with AES-128 Encryption
"""

import machine
import time
import ucryptolib # Native MicroPython AES library
from radio import LoraRadio
from ui import Display
from keypad import KeypadHandler
from logger import MessageLogger

# Pins configured to avoid GPIO conflicts
LORA_MOSI, LORA_MISO, LORA_SCK = 23, 19, 18
LORA_CS, LORA_RST, LORA_IRQ = 5, 14, 2 

OLED_SDA, OLED_SCL = 21, 22

# 3x4 Matrix Keypad (7-pin scanning configuration)
KEYPAD_ROWS = [13, 12, 15, 4]
KEYPAD_COLS = [32, 33, 25]

# AES-128 requires a 16-byte key
SECRET_KEY = b"HackClubLora123!" 

class Cipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, text):
        # AES works on 16-byte blocks; padding adds spaces to reach block size
        pad = 16 - (len(text) % 16)
        padded_text = text + " " * pad
        # Initialize AES in ECB mode (Mode 1)
        crypto = ucryptolib.aes(self.key, 1) 
        return crypto.encrypt(padded_text)

    def decrypt(self, encrypted_data):
        try:
            # Re-initialize AES to decrypt incoming byte stream
            crypto = ucryptolib.aes(self.key, 1)
            decrypted = crypto.decrypt(encrypted_data)
            # Remove padding spaces and convert bytes back to string
            return decrypted.decode().strip() 
        except:
            return "[Decryption Error]"

def main():
    print("LoraLink: Initializing Secure Layer...")
    
    cipher = Cipher(SECRET_KEY)
    
    # Setup hardware abstraction layers
    radio = LoraRadio(mosi=LORA_MOSI, miso=LORA_MISO, sck=LORA_SCK, cs=LORA_CS, rst=LORA_RST, irq=LORA_IRQ)
    i2c = machine.I2C(1, scl=machine.Pin(OLED_SCL), sda=machine.Pin(OLED_SDA))
    display = Display(i2c)
    keypad = KeypadHandler(KEYPAD_ROWS, KEYPAD_COLS)
    logger = MessageLogger()
    
    display.show_message("LoraLink SECURE", "Key: AES-128")
    
    while True:
        try:
            # Poll radio for encrypted packets
            encrypted_msg = radio.receive()
            if encrypted_msg:
                # Decrypt before displaying to user
                clear_text = cipher.decrypt(encrypted_msg)
                display.show_incoming(clear_text)
                logger.save_message("RX (Secure)", clear_text)
                print(f"Packet: {encrypted_msg} -> Decoded: {clear_text}")
            
            # Scan keypad matrix for new key presses
            key = keypad.get_key()
            if key:
                display.handle_key(key)
            
            # Check if user pressed '#' to trigger transmission
            if display.ready_to_send():
                message = display.get_message()
                if message:
                    # Encrypt string into bytes before sending over the air
                    encrypted_to_send = cipher.encrypt(message)
                    radio.send(encrypted_to_send)
                    
                    display.show_outgoing(message)
                    logger.save_message("TX (Secure)", message)
                    print(f"Sending Secure Packet: {encrypted_to_send}")
            
            # Small delay to prevent CPU overclocking
            time.sleep(0.1)
            
        except Exception as e:
            # Log errors to console and OLED for debugging
            print(f"System Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
