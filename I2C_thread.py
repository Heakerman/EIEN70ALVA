import smbus2
import time
import threading
from i2c_lcd import I2cLcd  # External library for LCD handling

# Define the I2C addresses of the five displays
I2C_ADDRESSES = [0x27]  # Change these based on jumper settings A0,A1,A2

# Create LCD objects for each display
bus = smbus2.SMBus(1)  # Use I2C bus 1 on the Raspberry Pi. SDA on pin 3, SCL on pin 5, GND on pin 6 and VCC on pin 4
lcds = [I2cLcd(1, addr, 4, 20) for addr in I2C_ADDRESSES]  # 1 is the I2C bus number  # Now using 4x20 LCDs. lcds is a list of 5 LCD objects

# Condition object for synchronizing with the monitor
condition = threading.Condition()

# Example message data structure
messages = [
    ["Option 1:", "Hello world", "  Testar mellanrum", ""],
    ["Option 2:", "No", "", ""],
    ["Option 3:", "Maybe", "", ""],
    ["Option 4:", "Later", "", ""],
    ["Option 5:", "Never", "", ""],
]

# Function to update all displays
def update_displays(messages):
    for i, lcd in enumerate(lcds):
        lcd.clear()
        for row in range(4):
            lcd.move_to(0, row)
            lcd.putstr(messages[i][row])

# The worker thread that waits for a signal to update the display
def display_updater():
    while True:
        with condition:  # Lock the condition
            condition.wait()  # Wait for notification
            update_displays(messages)  # Update the displays when notified

# Start the display updater thread
thread = threading.Thread(target=display_updater, daemon=True)
thread.start()
