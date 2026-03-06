"""
KeypadHandler - Matrix Scanning & T9 Multi-tap Logic
Handles a 3x4 matrix keypad using 7 GPIO pins.
"""

import machine
import time

class KeypadHandler:
    # T9 multi-tap character mapping
    T9_MAP = {
        '1': '.,?!1',
        '2': 'abc2',
        '3': 'def3',
        '4': 'ghi4',
        '5': 'jkl5',
        '6': 'mno6',
        '7': 'pqrs7',
        '8': 'tuv8',
        '9': 'wxyz9',
        '0': ' 0',
        '*': 'DELETE', # Custom mapping for backspace
        '#': 'SEND'   # Custom mapping for transmit
    }

    def __init__(self, row_pins, col_pins):
        """
        Initialize 4x3 matrix.
        Rows are Outputs (driven low), Columns are Inputs (pull-up).
        """
        self.row_pins = [machine.Pin(p, machine.Pin.OUT) for p in row_pins]
        self.col_pins = [machine.Pin(p, machine.Pin.IN, machine.Pin.PULL_UP) for p in col_pins]
        
        # Matrix layout
        self.keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]
        
        self.last_key = None
        self.last_time = 0

    def get_key(self):
        """
        Scans the matrix. Returns the character string of the pressed key.
        Returns None if no key is pressed or for debouncing.
        """
        current_key = None
        
        # Iterate through rows to find the pressed button
        for r_idx, r_pin in enumerate(self.row_pins):
            r_pin.value(0)  # Drive row LOW
            for c_idx, c_pin in enumerate(self.col_pins):
                if c_pin.value() == 0:  # Column pulled LOW means button is pressed
                    current_key = self.keys[r_idx][c_idx]
            r_pin.value(1)  # Set row back to HIGH
            
        # Basic debouncing and edge detection
        now = time.ticks_ms()
        if current_key and current_key != self.last_key:
            if time.ticks_diff(now, self.last_time) > 200: # 200ms debounce
                self.last_key = current_key
                self.last_time = now
                return current_key
        
        if not current_key:
            self.last_key = None
            
        return None

    def get_char(self, key, press_count):
        """
        Translates a physical key and tap count into a T9 character.
        """
        if key not in self.T9_MAP:
            return ""
            
        options = self.T9_MAP[key]
        # Cycle through characters based on number of taps
        idx = (press_count - 1) % len(options)
        return options[idx]
