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
        # Wait for an integer from the GPIO thread
        value_to_send = queue.get()  # Block until we get a value from the queue
        print(f"Sending integer {value_to_send} to the robot...")
        
        # Connect to the robot each time before sending a new value
        connect_to_robot()
        
        try:
            # Define the register where you want to store the integer
            register_address = 100  # Replace with the appropriate register address on the UR5
            
            # Send the integer to the UR5 robot
            client.write_register(register_address, value_to_send)
            print(f"Sent integer {value_to_send} to register {register_address} on UR5.")
            
            # Wait for acknowledgment from the robot (e.g., read a status register)
            # Replace 101 with the actual acknowledgment register address
            response = client.read_holding_registers(101, 1)  # Assuming 101 is the acknowledgment register
            if response.isError():
                print("Error reading acknowledgment from robot.")
            else:
                ack_value = response.registers[0]  # Get the acknowledgment value
                if ack_value == 1:  # Assuming '1' means successful acknowledgment
                    print("Acknowledgment received from the robot.")
                else:
                    print("Robot acknowledgment failed.")
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")
        
        # Close the connection after sending the integer and receiving acknowledgment
        client.close()
        print(f"Robot communication completed for value {value_to_send}.")
        
        # Reset the processing flag to allow new button presses
        is_processing = False
        
        # Sleep or wait for the next value in the queue
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
