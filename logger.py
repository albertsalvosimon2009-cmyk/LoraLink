"""
Message Logger Module
Saves message history to ESP32 flash storage
"""

import os
import time

class MessageLogger:
    """Message logging to flash storage"""
    
    def __init__(self, log_dir="/logs"):
        """Initialize logger"""
        self.log_dir = log_dir
        self.ensure_dir()
        
    def ensure_dir(self):
        """Create log directory if it doesn't exist"""
        try:
            os.mkdir(self.log_dir)
        except OSError:
            pass  # Directory already exists
            
    def save_message(self, direction, message):
        """Save message with timestamp"""
        timestamp = self._get_timestamp()
        filename = f"{self.log_dir}/messages.txt"
        
        try:
            with open(filename, 'a') as f:
                line = f"{timestamp} [{direction}] {message}\n"
                f.write(line)
                print(f"Logged: {line.strip()}")
        except Exception as e:
            print(f"Log error: {e}")
    
    def get_history(self, limit=50):
        """Retrieve message history"""
        filename = f"{self.log_dir}/messages.txt"
        messages = []
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                messages = lines[-limit:]
        except FileNotFoundError:
            pass
            
        return messages
    
    def clear_history(self):
        """Clear message history"""
        filename = f"{self.log_dir}/messages.txt"
        try:
            os.remove(filename)
            print("Message history cleared")
        except:
            pass
    
    def _get_timestamp(self):
        """Get current timestamp"""
        # Simple epoch-based timestamp
        # For production, use RTC module for proper date/time
        t = time.time()
        return f"{int(t)}"
