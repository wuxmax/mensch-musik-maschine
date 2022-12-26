from time import sleep
from typing import Union, List, Tuple, Dict
from smbus2 import SMBus
import numpy as np

from config_manager import ConfigManager
from value_stack import ValueStack
from utils import load_config


class I2CReader:
    def __init__(self, config_manager: ConfigManager, value_stack: ValueStack):
        self.config_manager = config_manager
        self.value_stack = value_stack
        try:
            self.smbus = SMBus(1)
        except PermissionError as e:
            print('NO I2C CONNECTION POSSIBLE')

        self.sensor_values: Dict[str, List[int]] = {str(i2c_address): [0] * self.config_manager.n_device_sensors() for
                                                    i2c_address in self.config_manager.i2c_addresses()}

    def read(self, i2c_address: int) -> Union[List[int], None]:
        try:
            block_data = self.smbus.read_i2c_block_data(i2c_address, 0x00, self.config_manager.n_device_sensors() * 2)
        except Exception as e:
            # print(f"I2C read exception: {e}")
            return None

        return [int.from_bytes(block_data[idx:idx + 2], byteorder='little', signed=False) for idx in
                range(0, self.config_manager.n_device_sensors() * 2, 2)]

    def load_sensor_list(self) -> np.ndarray:
        sensor_list = np.zeros((len(self.config_manager.i2c_addresses()), self.config_manager.n_device_sensors()))
        for idx, i2c_address in enumerate(self.config_manager.i2c_addresses()):
            i2c_device_values = self.read(i2c_address)
            if i2c_device_values:
                for sensor_idx in range(self.config_manager.n_device_sensors()):
                    sensor_list[idx] = i2c_device_values
                    self.sensor_values[str(i2c_address)] = i2c_device_values
        self.value_stack.append(sensor_list)
        return sensor_list

if __name__ == "__main__":
    cm = ConfigManager(config_name='config_real.yml')

    i2c_reader = I2CReader(cm, ValueStack(config_manager=cm))

    while True:
        print(i2c_reader.load_sensor_list())
        sleep(1)

