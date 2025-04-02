import time
from pymodbus.client import ModbusTcpClient

# Define Modbus TCP client and connection details
ur5_ip = '172.20.10.150'  # UR5's Modbus IP
ur5_port = 502            # Default Modbus TCP port
input_register_address = 40199   # The Modbus input register to write to
output_register_address = 20198  # The Modbus output register to read from

# Initialize Modbus client
client = ModbusTcpClient(ur5_ip, port=ur5_port, timeout=5)

# Connect to the robot
if client.connect():
    print("Connected to UR5 Modbus server.")
    
    while True:
        user_input = input("Enter an integer (1-3) to send to the robot, or type 'exit' to quit: ")

        if user_input.lower() == 'exit':
            print("Exiting program...")
            break

        # Validate input
        try:
            value_to_send = int(user_input)
            if value_to_send not in [1, 2, 3]:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue

        # Send the integer value
        response = client.write_register(address=input_register_address, value=value_to_send)
        
        if response.isError():
            print(f"Failed to write {value_to_send} to register {input_register_address}. Error: {response}")
        else:
            print(f"Sent integer {value_to_send} to register {input_register_address}.")

        # Wait for a short period (e.g., 1 second)
        time.sleep(1)

        # Reset the register by sending 0
        reset_response = client.write_register(address=input_register_address, value=0)
        
        if reset_response.isError():
            print(f"Failed to reset register {input_register_address}. Error: {reset_response}")
        else:
            print(f"Register {input_register_address} reset to 0.")

        # Read from the output register
        read_response = client.read_holding_registers(address=output_register_address, count=1)

        if read_response.isError():
            print(f"Failed to read register {output_register_address}. Error: {read_response}")
        else:
            output_value = read_response.registers[0]  # Get the first register value
            print(f"Read value {output_value} from register {output_register_address}.")

    # Disconnect
    client.close()
    print("Connection closed.")

else:
    print("Failed to connect to UR5 Modbus server.")