import sys
sys.path.append('..')

import pickle
from datetime import datetime

from tqdm import tqdm

from i2c_reader import I2CReader
from utils import load_config


N_READINGS = 5000


def collect_data(reader: I2CReader):
    data = {}
    print("Collecting data...")
    for _ in tqdm(range(N_READINGS)):
        data[datetime.now()] = reader.get_value_matrix()
    print("Finished")

    return data

def write_file(data):
    ts_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open("test_data/" + f"data_{ts_str}.pkl", 'wb') as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    config = load_config('config.yml')
    reader = I2CReader(config)
    data = collect_data(reader)
    write_file(data)
