from gpiozero import Button
import threading

class GPIO_thread(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self.running = True

        # Define GPIO pins for the 5 buttons
        self.BUTTON_PINS = [17, 18, 27, 22, 23]
        self.buttons = []

        for i, pin in enumerate(self.BUTTON_PINS):
            button = Button(pin, bounce_time=0.1, pull_up=True)
            button.when_pressed = self.make_button_handler(i)
            self.buttons.append(button)

    def make_button_handler(self, button_index):
        def handler():
            print(f"Button {button_index + 1} pressed")
            self.monitor.try_send_to_robot(button_index + 1)
        return handler

    def run(self):
        try:
            # Just keep the thread alive while events handle button presses
            while self.running:
                pass
        except Exception as e:
            print(f"Error in GPIO thread: {e}")
        finally:
            print("GPIO thread exited cleanly.")

    def stop(self):
        self.running = False
