from collections import deque
import numpy as np
from config_manager import ConfigManager


# manages a stack for the previous sensor values for calibration and recalibration
class ValueStack:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.values = deque(maxlen=config_manager.recalibration_window())
        self.init_values = [[-1 for _ in range(self.config_manager.n_device_sensors())] for _ in range(len(self.config_manager.i2c_addresses()))]

    def update_init_values(self, values, index=0):
        if index:
            self.init_values[index] = values
        self.init_values = values

    def empty(self):
        return len(self.values) == 0

    def append(self, values):
        self.values.append(values)

    def get_values(self):
        vals = list(self.values)
        for sensor in self.init_values:
            if -1 in sensor:
                return vals
        for _ in range(self.config_manager.recalibration_cluster_center_weight()):
            vals.append(self.init_values)
        return vals

if __name__ == "__main__":
    cm = ConfigManager(config_name='config_real.yml')

    value_stack = ValueStack(cm)

    print(value_stack.init_values)
    print(value_stack.empty())
    value_stack.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    print(value_stack.get_values())
    value_stack.update_init_values([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    print(value_stack.get_values())
    print(value_stack.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]))
    print(value_stack.get_values())
    print(value_stack.empty())

