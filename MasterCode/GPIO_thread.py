from gpiozero import Button, DigitalInputDevice, DigitalOutputDevice
import threading
import time

class GPIO_thread(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self.running = True

        # Define GPIO pins for the 5 buttons
        self.BUTTON_PINS = [17, 18, 27, 22, 23]
        self.buttons = []

        # Define GPIO for sensors and motors
        self.elevatorSensor = DigitalInputDevice(5)
        self.bucketSensor = DigitalInputDevice(6)
        self.elevatorMotor = DigitalOutputDevice(13)
        self.clawMotor = DigitalOutputDevice(19)

        # Assign sensor callbacks
        self.elevatorSensor.when_activated = self.elevatorSensor_High
        self.elevatorSensor.when_deactivated = self.elevatorSensor_Low
        self.bucketSensor.when_activated = self.bucketSensor_High
        self.bucketSensor.when_deactivated = self.bucketSensor_Low

        # Set up buttons with handlers
        for i, pin in enumerate(self.BUTTON_PINS):
            button = Button(pin, bounce_time=0.1, pull_up=True)
            button.when_pressed = self.make_button_handler(i)
            self.buttons.append(button)

    # Button press handler generator
    def make_button_handler(self, button_index):
        def handler():
            print(f"Button {button_index + 1} pressed")
            self.monitor.try_send_to_robot(button_index + 1)
        return handler

    # Elevator sensor event handlers
    def elevatorSensor_High(self):
        print("Elevator sensor HIGH – turning motor ON")
        self.elevatorMotor.on()

    def elevatorSensor_Low(self):
        print("Elevator sensor LOW – turning motor OFF")
        self.elevatorMotor.off()

    # Bucket sensor event handlers
    def bucketSensor_High(self):
        print("Bucket sensor HIGH")
        self.monitor.set_bucketSensor(True)

    def bucketSensor_Low(self):
        print("Bucket sensor LOW")
        self.monitor.set_bucketSensor(False)

    # External method to control the claw motor
    def setClawMotor(self, value):
        if value == 1:
            self.clawMotor.on()
        elif value == 0:
            self.clawMotor.off()
        else:
            print("Invalid value for claw motor. Use 1 to turn on and 0 to turn off.")

    # Thread run loop
    def run(self):
        try:
            while self.running:
                time.sleep(0.1)  # Prevent high CPU usage
        except Exception as e:
            print(f"Error in GPIO thread: {e}")
        finally:
            print("GPIO thread exited cleanly.")

    def stop(self):
        self.running = False
