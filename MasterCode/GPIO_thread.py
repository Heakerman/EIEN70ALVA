from gpiozero import Button
import threading
import time


class GPIO_thread(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self.running = True

        self.BUTTON_PIN = 18  # BCM 18 (physical pin 12)
        self.button = Button(self.BUTTON_PIN, pull_up=True)

        self.button_was_pressed = False

    def run(self):
        try:
            while self.running:
                if self.button.is_pressed and not self.button_was_pressed:
                        print("button pressed")
                        self.monitor.try_send_to_robot(2)
                        self.button_was_pressed = True

                elif not self.button.is_pressed:
                    self.button_was_pressed = False

                time.sleep(0.05)

        except Exception as e:
            print(f"Error in button monitor thread: {e}")

        finally:
            print("Thread exited cleanly.")

    def stop(self):
        self.running = False
