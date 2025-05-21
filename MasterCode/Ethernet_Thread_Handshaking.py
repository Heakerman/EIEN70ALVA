import time
from pymodbus.client import ModbusTcpClient
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
        self.received = 0  # Flag to indicate if the robot has acknowledged the integer

        self.condition = condition  # Condition variable for synchronization

    def run(self):
        while self.running:
            with self.condition:  # Lock the condition
                self.condition.wait()  # Wait for notification from the monitor

            if self.client.connect():
                self.IntToSend = self.monitor.get_robot_Integer()  # Get the robot integer from the monitor
                
                if self.IntToSend > 0 and self.IntToSend < 5: 
                    print("sent integer")
                    self.send_andWait(self.IntToSend)  # Send the integer to the robot
                    
                    
                    print("Grabbing")
                    self.gpio_thread.clawMotor_grab()
                    
                    print("Sending 6")
                    self.send_andWait(6)  # Send the integer to the robot

                    #if not self.monitor.get_bucketSensor(): # Check if the bucket sensor is not triggered
                        #self.gpio_thread.error() # Call the error method in the GPIO thread
                    
                    print("Releasing")
                    self.gpio_thread.clawMotor_release()
                    
                    print("sending 7")
                    self.send_andWait(7)
            
                    self.monitor.robot_acknowledge()
                    print("Has acknowledged")
                    self.IntToSend = -1


                #Happy mode
                if self.IntToSend == 10:
                    self.send_andWait(10)  # Send the integer to the robot
                    self.monitor.robot_acknowledge()
                    self.IntToSend = -1


                self.client.close()  # Close the Modbus connection


    def send_andWait(self, x):
        self.client.write_register(self.input_register_address, x)
        time.sleep(0.1)  # Sleep for a short duration to allow the robot to process the integer
        self.client.write_register(self.input_register_address, 0)
        time.sleep(0.2)

        while(self.received == 0):
            request = self.client.read_holding_registers(self.output_register_address)  # Read the output register to check if the robot has acknowledged the integer
            self.received = request.registers[0]
            time.sleep(0.2)  # Sleep for a short duration to avoid busy waiting

        while(self.received == 1):
            request = self.client.read_holding_registers(self.output_register_address)  # Read the output register to check if the robot has acknowledged the integer
            self.received = request.registers[0]
            time.sleep(0.2)  # Sleep for a short duration to avoid busy waiting
            
        print("received acknowledge from robot")

    def stop(self):
        if self.running:
            self.running = False
