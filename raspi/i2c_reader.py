from smbus2 import SMBus
import numpy as np

I2C_DEVICE_ADDRESSES = [11, 12, 13]
N_DEVICE_SENSORS = 6

SENSOR_MATRIX = [
    [(0, 0), (0, 1), (0, 2), (0, 0), (0, 1), (0, 2), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 0), (0, 1), (0, 2), (0, 1), (0, 2)],
]


class I2CReader:
    smbus = SMBus(1)
    i2c_addresses: list[int] = I2C_DEVICE_ADDRESSES
    # sensor_matrix: list[list[tuple[int, int]]] = SENSOR_MATRIX
    sensor_matrix: np.nd = np.array(SENSOR_MATRIX)
    
    def __init__(self):
        self.sensor_values: dict[int, list[int]] = {}
        self.value_matrix: np.ndarray = np.zeros(self.sensor_matrix.shape)

    def read(self, i2c_address: int) -> list[int] | None:
        try:
            block_data = self.smbus.read_i2c_block_data(i2c_address, 0x00, N_DEVICE_SENSORS)
        except Exception as e:
            return None

        return [int.from_bytes(block_data[idx:idx + 2], byteorder='little', signed=False) for idx in range(0, N_DEVICE_SENSORS * 2, 2)]

    def get_value_matrix(self) -> np.ndarray:
        for i2c_address in self.i2c_addresses:
            i2c_device_values = self.read(i2c_address)
            if i2c_device_values:
                self.sensor_values[i2c_address] = i2c_device_values
        
        for matrix_idx, (device_addr, sensor_idx) in np.enumerate(self.sensor_matrix):
            self.value_matrix[matrix_idx] = self.sensor_values[device_addr][sensor_idx]

        return self.value_matrix


if __name__ == "__main__":
    i2c_reader = I2CReader()
    i2c_reader.get_value_matrix()

