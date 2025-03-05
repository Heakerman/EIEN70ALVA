import smbus2
import time
from i2c_lcd import I2cLcd  # External library for LCD handling

# Define the I2C addresses of the five displays
I2C_ADDRESSES = [0x27]  # Change these based on jumper settings A0,A1,A2


# Create LCD objects for each display
bus = smbus2.SMBus(1)  # Use I2C bus 1 on the Raspberry Pi. SDA on pin 3, SCL on pin 5, GND on pin 6 and VCC on pin 4
lcds = [I2cLcd(1, addr, 4, 20) for addr in I2C_ADDRESSES]  # 1 is the I2C bus number  # Now using 4x20 LCDs. lcds is a list of 5 LCD objects

# Function to update all displays
def update_displays(messages):
    for i, lcd in enumerate(lcds): # Enumerate is used to get the index of the current display
        lcd.clear() # Clear the display
        for row in range(4): # Loop through the rows of the display
            lcd.move_to(0, row) # Move to the start of the row
            lcd.putstr(messages[i][row]) # Write the message to the display

# Example usage
messages = [ # List of messages to display on each display
    ["Option 1:", "Hello world", "  Testar mellanrum", ""],
    ["Option 2:", "No", "", ""],
    ["Option 3:", "Maybe", "", ""],
    ["Option 4:", "Later", "", ""],
    ["Option 5:", "Never", "", ""],
]

update_displays(messages) # Update the displays with the messages
