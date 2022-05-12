from time import sleep

from smbus2 import SMBus
import numpy as np

I2C_DEVICE_ADDRESSES = [13, 11, 12]
N_DEVICE_SENSORS = 6

# 4: (12, 5), 8: (11, 0), 15: (11, 3) have different offsets
SENSOR_MATRIX = [
    [(13, 5), (13, 3), (13, 4), (12, 5), (12, 0), (12, 1), (11, 1), (11, 0)],
    [(13, 1), (13, 0), (13, 2), (12, 4), (12, 3), (12, 2), (11, 3), (11, 2)],
]


class I2CReader:
    smbus = SMBus(1)
    i2c_addresses: list[int] = I2C_DEVICE_ADDRESSES
    sensor_matrix: list[list[tuple[int, int]]] = SENSOR_MATRIX
    # sensor_matrix: np.ndarray = np.array(SENSOR_MATRIX)
    
    def __init__(self):
        self.sensor_values: dict[int, list[int]] = {i2c_address: [0] * N_DEVICE_SENSORS for i2c_address in self.i2c_addresses }
        # self.value_matrix: np.ndarray = np.zeros(self.sensor_matrix.shape)
        self.value_matrix: np.ndarray = np.zeros((len(self.sensor_matrix), (len(self.sensor_matrix[0]))))

    # def read(self, i2c_address: int) -> list[int] | None:
    def read(self, i2c_address: int) -> list[int]:
        try:
            block_data = self.smbus.read_i2c_block_data(i2c_address, 0x00, N_DEVICE_SENSORS * 2)
        except Exception as e:
            # print(f"I2C read exception: {e}")
            return None

        return [int.from_bytes(block_data[idx:idx + 2], byteorder='little', signed=False) for idx in range(0, N_DEVICE_SENSORS * 2, 2)]

    def get_value_matrix(self) -> np.ndarray:
        for i2c_address in self.i2c_addresses:
            i2c_device_values = self.read(i2c_address)
            if i2c_device_values:
                for sensor_idx in range(N_DEVICE_SENSORS):
                    self.sensor_values[i2c_address] = i2c_device_values
        
        for row_idx, row in enumerate(self.sensor_matrix):
            for col_idx, (device_addr, sensor_idx) in enumerate(row):
                sensor_value = self.sensor_values[device_addr][sensor_idx]
                if sensor_value in range(0, 1024):
                    self.value_matrix[row_idx, col_idx] = sensor_value
                
        return self.value_matrix


if __name__ == "__main__":
    i2c_reader = I2CReader()
    
    while True:
        print(i2c_reader.get_value_matrix())
        sleep(3)
    
    # while True:
    #     print(i2c_reader.read(11))

