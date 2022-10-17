import sys
from time import sleep

from tqdm import tqdm

from data_preprocessor import MatrixDataPreprocessor
from matrix_processor import MatrixProcessor
from i2c_reader import I2CReader
from utils import load_config, parse_arguments


# CONFIG_FILE = "config.yml"
CONFIG_FILE = "config_test.yml"
# CONFIG_FILE = "config_fader.yml"

if __name__ == "__main__":
    config = load_config(CONFIG_FILE)
    reader = I2CReader(config)
    datpro = MatrixDataPreprocessor(config)
    matpro = MatrixProcessor(config, printing=True)

    sleepy = parse_arguments(sys.argv)
    
    datpro.calibrate(i2c_reader=reader)
    
    while True:
        sensor_values = reader.get_value_matrix()
        normalized_values = datpro.normalize(sensor_values)
        matpro.process(normalized_values)
        
        if sleepy:
            sleep(1)

    

