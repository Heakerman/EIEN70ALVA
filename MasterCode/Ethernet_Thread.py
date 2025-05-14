import time
from pymodbus.client import ModbusTcpClient
from GPIO_thread import GPIO_thread
import threading

class Ethernet_Thread(threading.Thread):
    def __init__(self, monitor, condition, gpio_thread):
        super().__init__()
        # Define Modbus TCP client and connection details
        ur5_ip = '172.20.10.150'  # UR5's Modbus IP
        ur5_port = 502            # Default Modbus TCP port
        self.input_register_address = 40199   # The Modbus input register to write to
        self.output_register_address = 20198  # The Modbus output register to read from

        # Initialize Modbus client
        self.client = ModbusTcpClient(ur5_ip, port=ur5_port, timeout=5)

        self.monitor = monitor  # Reference to the Monitor instance
        self.IntToSend = 0  # Integer to send to the robot

        self.gpio_thread = gpio_thread  # Reference to the GPIO thread
        self.running = True
        self.robotAcknowledgement = 0  # Flag to indicate if the robot has acknowledged the integer

        self.condition = condition  # Condition variable for synchronization

    def run(self):
        while self.running:
            with self.condition:  # Lock the condition
                print("1")
                self.condition.wait()  # Wait for notification from the monitor
                print("2")

            print("3")
            if self.client.connect():
                self.IntToSend = self.monitor.get_robot_Integer()  # Get the robot integer from the monitor
                if(self.IntToSend != -1):
                    self.client.write_register(self.input_register_address, self.IntToSend)  # Send the integer to the robot
                    time.sleep(0.1)  # Sleep for a short duration to allow the robot to process the integer
                        
                    self.client.write_register(self.input_register_address, 0)  # Reset the integer to 0
                    time.sleep(1)
                    while(self.robotAcknowledgement == 0):
                        request = self.client.read_holding_registers(self.output_register_address)  # Read the output register to check if the robot has acknowledged the integer
                        self.robotAcknowledgement = request.registers[0]
                        time.sleep(1)  # Sleep for a short duration to avoid busy waiting

                    while(self.robotAcknowledgement == 1):
                        request = self.client.read_holding_registers(self.output_register_address)  # Read the output register to check if the robot has acknowledged the integer
                        self.robotAcknowledgement = request.registers[0]
                        time.sleep(1)  # Sleep for a short duration to avoid busy waiting

                    self.monitor.robot_acknowledge()  # Acknowledge that the robot has received the integer
                    self.IntToSend = -1  # Reset the integer to -1 after sending

                self.client.close()  # Close the Modbus connection


    def stop(self):
        if self.running:
            self.running = False
