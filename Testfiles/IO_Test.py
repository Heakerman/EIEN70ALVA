import RPi.GPIO as GPIO
import time

# Pin configuration
BUTTON_PIN = 18  # Change to your actual button GPIO pin. Test kolla här
LED_PIN = 23     # Change to your actual LED GPIO pin 

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_state = False  # Initial LED state

def button_callback(channel):
    global led_state
    led_state = not led_state  # Toggle state
    GPIO.output(LED_PIN, led_state)
    print("LED ON" if led_state else "LED OFF")

# Add event detection for button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    print("Press the button to toggle the LED.")
    while True:
        time.sleep(0.1)  # Small delay to reduce CPU usage
except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()  # Cleanup GPIO on exit