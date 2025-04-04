import RPi.GPIO as GPIO
import time
import threading

BUTTON_PIN = 18  # BCM 18 (physical pin 12)

class ButtonMonitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.button_was_pressed = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        try:
            print("Waiting for button press... (Thread started)")
            while self.running:
                input_state = GPIO.input(BUTTON_PIN)

                if input_state == GPIO.LOW and not self.button_was_pressed:
                    print("Button was pressed!")
                    self.button_was_pressed = True
                elif input_state == GPIO.HIGH:
                    self.button_was_pressed = False

                time.sleep(0.05)

        except Exception as e:
            print(f"Error in button monitor thread: {e}")

        finally:
            GPIO.cleanup()
            print("GPIO cleaned up and thread exited.")

    def stop(self):
        self.running = False

# Example usage from another python program:
#if __name__ == "__main__":
#    button_thread = ButtonMonitor()
#    button_thread.start()

#    try:
#        # Simulate other tasks in the main program
#        while True:
#            print("Main program running...")
#            time.sleep(2)
#    except KeyboardInterrupt:
#        print("\nProgram interrupted by user.")
#        button_thread.stop()
#        button_thread.join()
#        print("Main program exited.")