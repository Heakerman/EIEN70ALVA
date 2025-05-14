from gpiozero import Button, DigitalInputDevice, DigitalOutputDevice, LED
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

        # Define GPIO pins for the LEDs
        self.LED_PINS = [24, 25, 8, 7, 12]
        self.leds = [LED(pin) for pin in self.LED_PINS]

        for led in self.leds:
            led.on()  # Turn on all LEDs initially

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

        # Stepper pins
        self.step_pin = DigitalOutputDevice(20)   # STEP
        self.dir_pin = DigitalOutputDevice(26)    # DIR (change if needed)

        self.stepper_running = False
        self.stepper_thread = None

    # Button press handler generator
    def make_button_handler(self, button_index):
        def handler():
            print(f"Button {button_index + 1} pressed")
            self.monitor.try_send_to_robot(button_index + 1)

            # Turn off all leds but the one corresponding to the button pressed
            for j, led in enumerate(self.leds):
                if j == button_index:
                    led.on()
                else:
                    led.off()
            
            time.sleep(1)  # Keep the LED on for 1 second
            for led in self.leds:
                led.on()

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

    # External method grab or release the claw motor
    def clawMotor_grab(self):
        print("Claw motor grabbing")
        self.clawMotor.on()


    def clawMotor_release(self):
        print("Claw motor releasing")
        self.clawMotor.off()

    def start_stepper(self):
        if self.stepper_thread is None or not self.stepper_thread.is_alive():
            print("Starting stepper motor thread")
            self.stepper_running = True
            self.stepper_thread = threading.Thread(target=self.stepper_loop)
            self.stepper_thread.start()

    def stop_stepper(self):
        print("Stopping stepper motor")
        self.stepper_running = False
        if self.stepper_thread:
            self.stepper_thread.join()
            self.stepper_thread = None

    def stepper_loop(self):
        self.dir_pin.on()  # Or .off(), depending on desired direction
        while self.stepper_running:
            self.step_pin.on()
            time.sleep(0.002)
            self.step_pin.off()
            time.sleep(0.002)


    def error(self):
        #Blinks all leds 5 times
        print("Error: Bucket sensor triggered")
        for _ in range(5):
            for led in self.leds:
                led.on()
            time.sleep(0.5)
            for led in self.leds:
                led.off()
            time.sleep(0.5)

        

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
