"""
OLED Display UI Module
Manages SSD1306/SH1106 display and user interface
"""

import machine
import time
from keypad import KeypadHandler

class Display:
    """OLED display UI manager"""
    
    def __init__(self, i2c, width=128, height=64):
        """Initialize OLED display"""
        self.i2c = i2c
        self.width = width
        self.height = height
        self.buffer = bytearray((width * height) // 8)
        
        self.input_message = ""
        self.cursor_pos = 0
        self.message_sent = False
        self.show_startup()
        
    def show_startup(self):
        """Display startup screen"""
        self.clear()
        self._draw_text(0, 0, "LoraLink v1.0")
        self._draw_text(0, 20, "P2P LoRa Mesh")
        self._draw_text(0, 40, "Initializing...")
        self.update()
        
    def show_message(self, line1, line2=""):
        """Show status message"""
        self.clear()
        self._draw_text(0, 0, line1)
        if line2:
            self._draw_text(0, 20, line2)
        self.update()
        
    def show_incoming(self, message):
        """Display incoming message"""
        self.clear()
        self._draw_text(0, 0, "<<< INCOMING >>>")
        self._draw_text(0, 16, message[:20])
        if len(message) > 20:
            self._draw_text(0, 32, message[20:40])
        self.update()
        time.sleep(2)
        
    def show_outgoing(self, message):
        """Display outgoing message confirmation"""
        self.clear()
        self._draw_text(0, 0, ">>> SENT <<<")
        self._draw_text(0, 16, message[:20])
        if len(message) > 20:
            self._draw_text(0, 32, message[20:40])
        self.update()
        time.sleep(1)
        
    def show_error(self, error_msg):
        """Display error message"""
        self.clear()
        self._draw_text(0, 0, "ERROR:")
        self._draw_text(0, 16, error_msg[:20])
        self.update()
        
    def handle_key(self, key_input):
        """Handle keypad input"""
        key, count = key_input if isinstance(key_input, tuple) else (key_input, 1)
        
        if key == '#':
            self.message_sent = True
        elif key == '*':
            # Backspace
            if self.cursor_pos > 0:
                self.input_message = self.input_message[:-1]
                self.cursor_pos -= 1
        else:
            # Add character using T9
            from keypad import KeypadHandler
            char = KeypadHandler.T9_MAP.get(key, "")
            if char and count <= len(char):
                char_to_add = char[count - 1]
                self.input_message += char_to_add
                self.cursor_pos += 1
        
        self.update_input_display()
        
    def update_input_display(self):
        """Update display with current input"""
        self.clear()
        self._draw_text(0, 0, "Message:")
        self._draw_text(0, 16, self.input_message[:20])
        if len(self.input_message) > 20:
            self._draw_text(0, 32, self.input_message[20:40])
        self._draw_text(0, 48, "# Send | * Delete")
        self.update()
        
    def ready_to_send(self):
        """Check if message is ready to send"""
        return self.message_sent
    
    def get_message(self):
        """Get and clear the message"""
        msg = self.input_message
        self.input_message = ""
        self.cursor_pos = 0
        self.message_sent = False
        return msg
    
    def clear(self):
        """Clear display buffer"""
        for i in range(len(self.buffer)):
            self.buffer[i] = 0
            
    def update(self):
        """Update physical display"""
        # Send buffer to OLED via I2C
        # This is a simplified implementation
        try:
            self.i2c.writeto(0x3C, bytes([0x40]) + self.buffer)
        except:
            pass  # Display not ready
    
    def _draw_text(self, x, y, text):
        """Draw text on buffer (simplified 5x7 font simulation)"""
        # Simplified text rendering
        # In production, use a proper font library
        for i, char in enumerate(text[:20]):
            char_x = x + (i * 6)
            # Simple placeholder - in real implementation, use font bitmap
            pass
