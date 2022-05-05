from smbus2 import SMBus

# I2C_SLAVE_ADDRESS = 11

I2C_SLAVE_ADDRESSES = [11, 12, 13]
N_DEVICE_SENSORS = 6

# class I2CDevice:
#     sensors = range(6)
#     def __init__(self, address: int):
#         self.address = address


# sensor_matrix = [
#     [(0, 0), (0, 1), (0, 2)],
#     [(0, 3), (0, 4), (0, 5)],
# ]


class I2CReader:
    smbus = SMBus(1)
    
    def __init__(self):
        # self.i2c_devices = [I2CDevice(i2c_address) for i2c_address in I2C_SLAVE_ADDRESSES]
        self.i2c_addresses = I2C_SLAVE_ADDRESSES

    def read(self):
        # for i2c_device in self.i2c_devices:
        for i2c_address in self.i2c_addresses:
            try:
                block_data = self.smbus.read_i2c_block_data(i2c_address, 0x00, N_DEVICE_SENSORS)
            except Exception as e:
                return None
    
        return [int.from_bytes(block_data[idx:idx + 2], byteorder='little', signed=False) for idx in range(0, 8, 2)]

