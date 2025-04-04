import RPi.GPIO as GPIO
import time
import threading
from queue import Queue
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

# Pin configuration
BUTTON_PINS = [18, 19, 20, 21, 22]  # Button pins
LED_PINS = [23, 24, 25, 26, 27]    # LED pins
SENSOR_PINS = [5, 6]  # Sensor pins
MOTOR_PIN = 13        # Motor pin

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Queue to pass the integer to the robot control thread
queue = Queue()

# Global flag to indicate if the robot is currently processing a command
is_processing = False

# Modbus client setup (without connection)
client = None

# Modbus registers
REGISTER_ADDRESS = 0  # Replace with your actual register address
ACK_REGISTER = 1      # Replace with your actual ACK register address

# Connect to the robot function
def connect_to_robot():
    global client
    ur5_ip = '192.168.1.100'  # Replace with the UR5's IP address
    ur5_port = 502            # Default Modbus port
    client = ModbusTcpClient(ur5_ip, port=ur5_port)
    try:
        client.connect()
        return client
    except Exception as e:
        print(f"Error connecting to robot: {e}")
        return None

def sensor_callback(channel):
    sensor_index = SENSOR_PINS.index(channel) + 1  # Map sensor pin to integer (1-2)
    print(f"Sensor {sensor_index} triggered")

def control_motor(state):
    GPIO.output(MOTOR_PIN, state)
    print("Motor ON" if state else "Motor OFF")

def control_led(led_index, state):
    GPIO.output(LED_PINS[led_index], state)
    print(f"LED {led_index + 1} {'ON' if state else 'OFF'}")

for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)  # Set LED pins as output
    GPIO.output(pin, False)

GPIO.setup(MOTOR_PIN, GPIO.OUT)  # Set motor pin as output
GPIO.output(MOTOR_PIN, False)

# Setup sensor pins
for pin in SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set sensor pins as input
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=sensor_callback, bouncetime=200)

class ButtonMonitor(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.running = True
        self.button_was_pressed = [False] * len(BUTTON_PINS)  # Track each button
        self.queue = queue # store the queue

        for pin in BUTTON_PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        try:
            print("Button monitor thread started.")
            while self.running:
                for i, pin in enumerate(BUTTON_PINS):
                    input_state = GPIO.input(pin)

                    if input_state == GPIO.LOW and not self.button_was_pressed[i]:
                        global is_processing
                        if is_processing:
                            print("Robot is still processing, ignoring button press.")
                            continue

                        print(f"Button {i+1} pressed, sending integer {i+1}")
                        self.queue.put(i + 1)
                        self.button_was_pressed[i] = True
                        is_processing = True

                    elif input_state == GPIO.HIGH:
                        self.button_was_pressed[i] = False

                time.sleep(0.05)

        except Exception as e:
            print(f"Error in button monitor thread: {e}")

        finally:
            GPIO.cleanup()
            print("Button monitor thread stopped and GPIO cleaned up.")

    def stop(self):
        self.running = False

# The robot communication thread, which will send the value to the robot
def robot_com_thread(queue):
    global is_processing
    while True:
        value_to_send = queue.get()  # Wait for an integer from the GPIO thread
        print(f"Sending integer {value_to_send} to the robot...")

        client = connect_to_robot()
        if client is None:
            print("Skipping this command due to connection failure.")
            is_processing = False
            continue

        try:
            client.write_register(REGISTER_ADDRESS, value_to_send)
            print(f"Sent integer {value_to_send} to register {REGISTER_ADDRESS}.")

            # Step 1: Wait for acknowledgment (ACK_REGISTER = 1)
            print("Waiting for robot acknowledgment...")
            while True:
                response = client.read_holding_registers(ACK_REGISTER, 1)
                if response.isError():
                    print("Error reading acknowledgment from robot.")
                    break
                elif response.registers[0] == 1:
                    print("Acknowledgment received from the robot!")
                    break  # Exit loop when ACK_REGISTER is 1
                time.sleep(0.1)

            # Step 2: Wait for robot to reset ACK_REGISTER to 0 before proceeding
            print("Waiting for robot to reset ACK_REGISTER to 0...")
            while True:
                response = client.read_holding_registers(ACK_REGISTER, 1)
                if response.isError():
                    print("Error reading acknowledgment reset.")
                    break
                elif response.registers[0] == 0:
                    print("Robot reset ACK_REGISTER to 0. Ready for next command.")
                    break  # Exit loop when ACK_REGISTER is 0
                time.sleep(0.1)

        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")

        finally:
            client.close()
            print(f"Robot communication completed for value {value_to_send}.")
            is_processing = False  # Allow new button presses

        time.sleep(0.1)

if __name__ == "__main__":
    button_thread = ButtonMonitor(queue)
    button_thread.start()

    robot_thread = threading.Thread(target=robot_com_thread, args=(queue,))
    robot_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        button_thread.stop()
        button_thread.join()
        GPIO.cleanup()
        print("GPIO cleaned up and program exited.")