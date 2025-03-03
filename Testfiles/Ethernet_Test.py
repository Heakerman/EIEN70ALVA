from pymodbus.client.sync import ModbusTcpClient

# Define the Modbus TCP client and connection details
ur5_ip = '192.168.1.100'  # Replace with the UR5's IP address
ur5_port = 502            # Default Modbus port
client = ModbusTcpClient(ur5_ip, port=ur5_port)

# Connect to the robot
client.connect()

# Define the register where you want to store the integer
register_address = 100  # Replace with the appropriate register address on the UR5

# The integer value to send
value_to_send = 12345  # Replace with the integer you want to send

# Send the integer to the UR5 robot
client.write_register(register_address, value_to_send)

# Close the connection
client.close()

print(f"Sent integer {value_to_send} to register {register_address} on UR5.")