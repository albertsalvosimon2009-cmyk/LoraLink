# LoraLink - Off-Grid P2P LoRa Communication System

An open-source decentralized IoT communication system for peer-to-peer text messaging without internet or LoRaWAN infrastructure. Perfect for emergency communication, remote locations, and off-grid networks.

## Features

- **P2P Mesh Communication**: Direct device-to-device messaging
- **No Internet Required**: Fully autonomous network operation
- **T9 Input**: Familiar multi-tap text entry on 3x4 keypad
- **Message History**: Persistent logging to flash storage
- **OLED Display**: Real-time message viewing and status
- **MicroPython**: Easy to modify and deploy on ESP32

## Hardware Requirements

- **Microcontroller**: ESP32 (Wemos D1 R32, LilyGO TTGO, etc.)
- **LoRa Module**: SX1276 or compatible (433/868/915 MHz)
- **Display**: SSD1306 or SH1106 OLED (128x64)
- **Keypad**: 3x4 Matrix Numeric Keypad
- **Connections**: SPI (LoRa), I2C (Display), GPIO (Keypad)

## Hardware Pinout

### LoRa (SPI1)
- MOSI: GPIO 23
- MISO: GPIO 19
- SCK: GPIO 18
- CS: GPIO 5
- RST: GPIO 14
- IRQ: GPIO 26

### OLED (I2C1)
- SDA: GPIO 21
- SCL: GPIO 22
- Address: 0x3C

### Keypad (GPIO)
- 12 GPIO pins for 3x4 matrix
- Pins: 12,13,15,2,4,32,33,25,26,27,14,16

## Installation

### 1. Flash MicroPython Firmware

```bash
# Download firmware from micropython.org
# For ESP32: https://micropython.org/download/esp32/

# Using esptool:
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20231212-v1.22.0.bin
```

### 2. Upload LoraLink Code

Using Thonny IDE:
1. Open Thonny
2. Tools → Options → Interpreter → MicroPython (ESP32)
3. Connect to your ESP32
4. Create new files:
   - `main.py`
   - `radio.py`
   - `ui.py`
   - `keypad.py`
   - `logger.py`
5. Copy code from this repository
6. Save files to device
7. Run main.py

## Usage

### Basic "Hello World" Test

1. **Setup Two Devices**:
   - Flash both ESP32 boards with LoraLink firmware
   - Ensure hardware connections are identical

2. **Start Communication**:
   - Power on both devices
   - Device 1: Use keypad to enter message (T9 input)
   - Press `#` to send
   - Device 2: Should receive message on OLED display

3. **Monitor Serial**:
   - Open Thonny serial console
   - Watch TX/RX logs in real-time

### T9 Keypad Mapping

```
1: . , ? ! 1 ' - ( )
2: a b c 2
3: d e f 3
4: g h i 4
5: j k l 5
6: m n o 6
7: p q r s 7
8: t u v 8
9: w x y z 9
0: [space] 0
*: + (delete)
#: SEND
```

**Example**: To type "HELLO"
- Press 4 (g,h,i) twice → h
- Press 3 (d,e,f) twice → e
- Press 5 (j,k,l) three times → l
- Press 5 (j,k,l) three times → l
- Press 6 (m,n,o) three times → o

## File Structure

```
loralink/
├── main.py           # Application entry point
├── radio.py          # LoRa communication module
├── ui.py             # OLED display interface
├── keypad.py         # T9 input handler
├── logger.py         # Message logging
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Message History

Messages are saved to `/logs/messages.txt` with format:
```
[timestamp] [TX|RX] message text
```

Access via:
```python
from logger import MessageLogger
logger = MessageLogger()
history = logger.get_history()
```

## Troubleshooting

### No Messages Received
- Check LoRa pin connections (especially IRQ)
- Verify both devices use same frequency (915 MHz)
- Check antenna connections
- Monitor serial output for errors

### Display Not Showing
- Verify I2C address (default 0x3C)
- Check SDA/SCL pull-up resistors
- Try I2C scanner to detect device

### Keypad Not Responding
- Verify GPIO pin configuration
- Check for pin conflicts
- Test with simple GPIO read test

## Future Enhancements

- [ ] GPS coordinates with messages
- [ ] Voice message support
- [ ] Multi-hop relay capability
- [ ] Encryption/privacy features
- [ ] Battery monitoring display
- [ ] Web-based network map
- [ ] LoRaWAN gateway bridge mode

## License

MIT License - Feel free to modify and distribute

## Contributing

Fork the repository and submit pull requests with improvements!

## Support

For questions and discussions, open an issue on GitHub.

---

**Happy messaging with LoraLink! 📡**
