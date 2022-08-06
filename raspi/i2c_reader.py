from time import sleep
from typing import Union

from smbus2 import SMBus
import numpy as np

from utils import load_config

class I2CReader:    
    def __init__(self, config: dict):
        self.smbus = SMBus(1)
        self.i2c_addresses: list[int] = config['i2c_reader']['i2c_device_addresses']
        self.n_device_sensors: int = config['i2c_reader']['n_device_sensors']
        self.sensor_matrix: list[list[tuple[int, int]]] = config['i2c_reader']['sensor_matrix']

        matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])
        sensor_matrix_shape = (len(self.sensor_matrix), len(self.sensor_matrix[0]))
        try:
            assert matrix_shape == sensor_matrix_shape 
        except:
            print(f"Matrix shape {matrix_shape} does not equal sensor matrix shape {sensor_matrix_shape}")
            exit(1)

        self.sensor_values: dict[int, list[int]] = {i2c_address: [0] * self.n_device_sensors for i2c_address in self.i2c_addresses }
        self.value_matrix: np.ndarray = np.zeros((len(self.sensor_matrix), (len(self.sensor_matrix[0]))))

    def read(self, i2c_address: int) -> Union[list[int], None]:
        try:
            block_data = self.smbus.read_i2c_block_data(i2c_address, 0x00, self.n_device_sensors * 2)
        except Exception as e:
            # print(f"I2C read exception: {e}")
            return None

        return [int.from_bytes(block_data[idx:idx + 2], byteorder='little', signed=False) for idx in range(0, self.n_device_sensors * 2, 2)]

    def get_value_matrix(self) -> np.ndarray:
        for i2c_address in self.i2c_addresses:
            i2c_device_values = self.read(i2c_address)
            if i2c_device_values:
                for sensor_idx in range(self.n_device_sensors):
                    self.sensor_values[i2c_address] = i2c_device_values
        
        for row_idx, row in enumerate(self.sensor_matrix):
            for col_idx, (device_addr, sensor_idx) in enumerate(row):
                sensor_value = self.sensor_values[device_addr][sensor_idx]
                if sensor_value in range(0, 1024):
                    self.value_matrix[row_idx, col_idx] = sensor_value
                
        return self.value_matrix.copy()


if __name__ == "__main__":
    i2c_reader = I2CReader(load_config())
    np.set_printoptions(formatter={'float_kind':"{:.1f}".format})
    
    while True:
        print(i2c_reader.get_value_matrix())
        sleep(1)
    
    # while True:
    #     print(i2c_reader.read(11))

