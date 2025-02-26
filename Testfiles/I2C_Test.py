import smbus2
import time
from i2c_lcd import I2cLcd  # External library for LCD handling

# Define the I2C addresses of the five displays
I2C_ADDRESSES = [0x20, 0x21, 0x22, 0x23, 0x24]  # Change these based on jumper settings

# Create LCD objects for each display
bus = smbus2.SMBus(1)  # Use I2C bus 1 on the Raspberry Pi
lcds = [I2cLcd(bus, addr, 4, 20) for addr in I2C_ADDRESSES]  # Now using 4x20 LCDs

# Function to update all displays
def update_displays(messages):
    for i, lcd in enumerate(lcds):
        lcd.clear()
        for row in range(4):
            lcd.move_to(0, row)
            lcd.putstr(messages[i][row])

# Example usage
messages = [
    ["Option 1:", "Yes", "", ""],
    ["Option 2:", "No", "", ""],
    ["Option 3:", "Maybe", "", ""],
    ["Option 4:", "Later", "", ""],
    ["Option 5:", "Never", "", ""],
]

update_displays(messages)