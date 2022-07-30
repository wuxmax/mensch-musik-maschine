from time import sleep

from tqdm import tqdm

from data_preprocessor import MatrixDataPreprocessor
from matrix_processor import MatrixProcessor
from i2c_reader import I2CReader
from utils import load_config


CONFIG_FILE = "config.yml"

config = load_config(CONFIG_FILE)
reader = I2CReader(config)
datpro = MatrixDataPreprocessor(config)
matpro = MatrixProcessor(config)


if __name__ == "__main__":
    print("Calibrating...")
    reference_values = [reader.get_value_matrix() for _ in tqdm(range(config['data_preprocessor']['calibration_period']))]
    datpro.calibrate(reference_values)
    print("Calibration done!")

    
    while True:
        sensor_values = reader.get_value_matrix()
        normalized_values = datpro.normalize(sensor_values)
        matpro.process(normalized_values)
        sleep(1)
    

