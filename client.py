#--client.py--#
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import asyncio

PORT = 5020
class Client:

    def __init__(self):
        self._client = ModbusTcpClient('localhost', PORT)

    def play_client(self):
        try:
            self._client.connect()
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")

    def read_data(self, data_type, address):  
        try:
            if data_type == 1:
                response = self._client.read_coils(address, 1)
            elif data_type == 2:
                response = self._client.read_discrete_inputs(address, 1)
            elif data_type == 3:
                response = self._client.read_input_registers(address, 1)
            elif data_type == 4:
                response = self._client.read_holding_registers(address, 1)
            else:
                print("Invalid data type")
                return None

            return response.getBit(0)
        except ModbusIOException as e:
            print(f"Modbus communication error during read: {e}")
            return None

    def write_data(self, data_type, address, values):  
        try:
            if data_type == 1:
                return self._client.write_coils(address, values)
            elif data_type == 2:
                return self._client.write_registers(address, values)
            else:
                print("Invalid data type")
                return None
        except ModbusIOException as e:
            print(f"Modbus communication error during write: {e}")
            return None

    def escrever_variaveis_retencoes(self, address, values):
        return self.write_data(4, address, values)  

    async def rodar_processador(self):
        while True:  
            await asyncio.gather(
                self.atualizar_processador(),
                self.temporizador()
            )

    async def atualizar_processador(self):
        return print("Updating processor")

    async def temporizador(self):
        return asyncio.sleep(5)  


if __name__ == "__main__":
    modbus_client = Client()
    modbus_client.play_client()

    co_value = modbus_client.read_data(1, 0)
    di_value = modbus_client.read_data(2, 0)
    ir_value = modbus_client.read_data(3, 0)
    hr_value = modbus_client.read_data(4, 0)

    print(f"Coil value: {co_value}")
    print(f"Discrete Input value: {di_value}")
    print(f"Input Register value: {ir_value}")
    print(f"Holding Register value: {hr_value}")

    write_type = 1
    write_address = 0
    write_values = [True] * 5
    modbus_client.write_data(write_type, write_address, write_values)

    modbus_client.escrever_variaveis_retencoes(0, [10, 20, 30, 40, 50])
    
