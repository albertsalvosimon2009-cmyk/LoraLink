
"""
T9-Style Keypad Input Handler
Manages 3x4 numeric keypad with multi-tap T9 input
"""

import machine
import time

class KeypadHandler:
    """T9 keypad input handler"""
    
    # T9 key mapping
    T9_MAP = {
        '1': '.,?!1\'-()      ',
        '2': 'abc2',
        '3': 'def3',
        '4': 'ghi4',
        '5': 'jkl5',
        '6': 'mno6',
        '7': 'pqrs7',
        '8': 'tuv8',
        '9': 'wxyz9',
        '0': ' 0',
        '*': '+',
        '#': 'SEND'
    }
    
    def __init__(self, pins):
        """Initialize keypad with GPIO pins (3 rows x 4 cols = 12 pins)"""
        self.pins = [machine.Pin(p, machine.Pin.IN, machine.Pin.PULL_UP) for p in pins]
        self.last_key = None
        self.last_press_time = 0
        self.press_count = 0
        
    def get_key(self):
        """Get pressed key (non-blocking, returns None if no press)"""
        for i, pin in enumerate(self.pins):
            if pin.value() == 0:  # Pin pulled low = pressed
                current_time = time.time()
                
                # Debounce
                if i == self.last_key and current_time - self.last_press_time < 0.3:
                    self.press_count += 1
                else:
                    self.press_count = 1
                    self.last_key = i
                
                self.last_press_time = current_time
                return self._index_to_key(i), self.press_count
        
        # Key released
        if self.last_key is not None:
            released_key = self._index_to_key(self.last_key)
            self.last_key = None
            return released_key, self.press_count
        
        return None, 0
    
    def _index_to_key(self, index):
        """Convert GPIO index to keypad character (0-11 -> 1-9,*,0,#)"""
        key_map = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
        return key_map[index]
    
    def get_char(self, key, press_count):
        """Get T9 character from key and press count"""
        if key not in self.T9_MAP:
            return None
        
        chars = self.T9_MAP[key]
        idx = (press_count - 1) % len(chars)
        return chars[idx]
