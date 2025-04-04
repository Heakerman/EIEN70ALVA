import time
from pymodbus.client import ModbusTcpClient
import threading

class Ethernet_Thread(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        # Define Modbus TCP client and connection details
        ur5_ip = '172.20.10.150'  # UR5's Modbus IP
        ur5_port = 502            # Default Modbus TCP port
        input_register_address = 40199   # The Modbus input register to write to
        output_register_address = 20198  # The Modbus output register to read from

        # Initialize Modbus client
        self.client = ModbusTcpClient(ur5_ip, port=ur5_port, timeout=5)

        self.monitor = monitor  # Reference to the Monitor instance
        self.IntToSend = 0  # Integer to send to the robot

        self.running = True
        self.robotAcknowledgement = 0  # Flag to indicate if the robot has acknowledged the integer

        self.condition = threading.Condition()  # Condition variable for synchronization

    def run(self):
        while self.running:
            with condition:  # Lock the condition
                condition.wait()  # Wait for notification from the monitor

            if client.connect():
                self.IntToSend = self.monitor.get_robot_Integer()  # Get the robot integer from the monitor
                if(self.IntToSend != -1):
                    client.write_register(adress=input_register_address, value=self.IntToSend)  # Send the integer to the robot
                    sleep(0.1)  # Sleep for a short duration to allow the robot to process the integer
                        
                    client.write_register(adress=input_register_address, value=0)  # Reset the integer to 0

                    while(robotAcknowledgement == 0):
                        self.robotAcknowledgement = client.read_holding_registers(address=output_register_address, count=1)  # Read the output register to check if the robot has acknowledged the integer
                        sleep(4)  # Sleep for a short duration to avoid busy waiting

                    while(robotAcknowledgement == 1):
                        self.robotAcknowledgement = client.read_holding_registers(address=output_register_address, count=1)
                        sleep(1)  # Sleep for a short duration to avoid busy waiting

                    monitor.robotAcknowledgement()  # Acknowledge that the robot has received the integer
                    self.IntToSend = -1  # Reset the integer to -1 after sending

                client.close()  # Close the Modbus connection


    def stop(self):
        if self.running:
            self.running = False
