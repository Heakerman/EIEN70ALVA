import RPi.GPIO as GPIO
import time

BUTTON_PIN = 18  # BCM 18 (physical pin 12)

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Set the GPIO mode to BCM
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set the button pin as input with pull-up resistor

# This flag controls the main loop
running = True

# To track if button has been pressed
button_was_pressed = False

# Main loop
try:
    print("Waiting for button press... (Ctrl+C to exit)")
    while running:
        input_state = GPIO.input(BUTTON_PIN)  # Read the button state
        
        if input_state == GPIO.LOW and not button_was_pressed:  # Button pressed and not already processed
            print("Button was pressed!")
            button_was_pressed = True  # Set flag to indicate the button press is processed
        
        elif input_state == GPIO.HIGH:  # Button not pressed
            button_was_pressed = False  # Reset the flag when button is released
        
        time.sleep(0.05)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    GPIO.cleanup()  # Clean up the GPIO settings on exit
    print("GPIO cleaned up and program exited.")
