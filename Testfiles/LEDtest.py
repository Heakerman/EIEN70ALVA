from gpiozero import LED
from time import sleep

# Define all LED GPIO pins
led_pins = [9, 25, 11, 8]

# Create LED objects
leds = [LED(pin) for pin in led_pins]

print("Turning on all LEDs.")
for led in leds:
    led.on()

sleep(6)  # Keep them on for 6 seconds

print("Turning off all LEDs.")
for led in leds:
    led.off()
