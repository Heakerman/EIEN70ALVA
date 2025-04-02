import RPi.GPIO as GPIO
import time
import threading
from queue import Queue
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

# Pin configuration
BUTTON_PINS = [18, 19, 20, 21, 22]  # Button pins
LED_PINS = [23, 24, 25, 26, 27]     # LED pins
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

# Connect to the robot function
def connect_to_robot():
    global client
    ur5_ip = '192.168.1.100'  # Replace with the UR5's IP address
    ur5_port = 502            # Default Modbus port
    client = ModbusTcpClient(ur5_ip, port=ur5_port)
    client.connect()

def callback(channel):
    global is_processing

    if channel in BUTTON_PINS:
        if is_processing:
            # Ignore new button presses if the robot is still processing
            print("Robot is still processing, ignoring button press.")
            return
        
        button_index = BUTTON_PINS.index(channel) + 1  # Map button pin to integer (1-5)
        print(f"Button {button_index} pressed, sending integer {button_index}")
        queue.put(button_index)  # Put the integer into the queue for robot communication
        is_processing = True  # Set the processing flag to True

    elif channel in SENSOR_PINS:
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

# Setup button and sensor pins
for pin in BUTTON_PINS + SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set button and sensor pins as input
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback, bouncetime=200)

GPIO.setup(MOTOR_PIN, GPIO.OUT)  # Set motor pin as output
GPIO.output(MOTOR_PIN, False)

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

class GPIOthread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
    
    def run(self):
        try:
            print("GPIO event thread running.")
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            GPIO.cleanup()  # Cleanup GPIO on exit

# Start the threads
def start_gpio_thread():
    t_gpio = GPIOthread()
    t_gpio.start()
    return t_gpio

def start_robot_com_thread():
    t_robot = threading.Thread(target=robot_com_thread, args=(queue,))
    t_robot.start()
    return t_robot

# Start both threads
start_gpio_thread()
start_robot_com_thread()
