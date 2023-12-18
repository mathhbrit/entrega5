#--server.py--#
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock
import time
import random

class Server:

    def __init__(self):
        
        coil_block = ModbusSequentialDataBlock(0, [False] * 10000)                # Coils (read/write) - 1 bit
        discrete_input_block = ModbusSequentialDataBlock(10001, [False] * 10000)  # Discrete Inputs (read) - 1 bit
        input_register_block = ModbusSequentialDataBlock(30001, [0] * 10000)      # Input Registers (read) - 16 bits
        holding_register_block = ModbusSequentialDataBlock(40001, [0] * 10000)    # Holding Registers (read/write) - 16 bits

        slave_context = ModbusSlaveContext(
            co=coil_block,
            di=discrete_input_block,
            ir=input_register_block,
            hr=holding_register_block
        )

        self.context_slave = ModbusSlaveContext(slaves=[slave_context])

    def control_process(self):
        print("Controlling the process...")
        temperature = random.uniform(20, 30)
        pressure = random.uniform(800, 1200)
        if temperature > 25:
            print("High temperature detected. Taking corrective action...")
        if pressure > 1000:
            print("High pressure detected. Taking corrective action...")
    
    def update_discrete_variables(self):
        print("Updating discrete variables...")
        device_states = [random.choice([True, False]) for _ in range(10)]  
        for i, state in enumerate(device_states):
            address = 10001 + i  
            self.context_slave[0].setValues(2, address, [state])
        print(f"New Discrete Input values: {device_states}")

    def update_register_variables(self):
        print("Updating register variables...")
        new_sensor_values = [random.randint(0, 100) for _ in range(5)]  
        for i, value in enumerate(new_sensor_values):
            address = 40001 + i  
            self.context_slave[0].setValues(4, address, [value])
        print(f"New Holding Register values: {new_sensor_values}")

    def run(self):
        try:
            PORT = 5020
            StartTcpServer(self.context_slave, address=("localhost", PORT))
            print("Modbus Server started...")
            while True:
                self.control_process()
                self.update_discrete_variables()
                self.update_register_variables()
                time.sleep(5)  
        except KeyboardInterrupt:
            print("Modbus Server stopped.")

if __name__ == "__main__":
    server_instance = Server()
    server_instance.run()
