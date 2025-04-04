import RPi.GPIO as GPIO
import time
import threading


class GPIO_thread(threading.Thread):
    def __init__(self, monitor):
        threading.Thread.__init__(self)
        
        self.monitor = monitor  # Reference to the Monitor instance
        self.condition = threading.Condition()
        self.running = True
        self.button_was_pressed = False
        
        self.BUTTON_PIN = 18  # BCM 18 (physical pin 12)
        
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        try:
            while self.running:
                input_state = GPIO.input(self.BUTTON_PIN)
                
                if input_state == GPIO.LOW and not self.button_was_pressed:
                    self.monitor.try_send_to_robot(self.BUTTON_PIN)
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