from utils import load_config


class ConfigManager:

    def __init__(self, config: dict = {}, config_name: str = ''):
        if self.test_config(config):
            self.config = config
        elif self.test_config(load_config(config_name)):
            self.config = load_config(config_name)
        else:
            self.config = load_config()

    def load_config(self, config: str):
        c = load_config(config)
        if self.test_config(c):
            self.config = c
        else:
            raise 'config has error'

    def change_field(self, menu, field, value):
        if menu:
            if isinstance(self.config[menu][field], int):
                self.config[menu][field] = int(value)
            elif isinstance(self.config[menu][field], float):
                self.config[menu][field] = float(value)
            else:
                self.config[menu][field] = value
        else:
            if isinstance(self.config[field], int):
                self.config[field] = int(value)
            elif isinstance(self.config[field], float):
                self.config[field] = float(value)
            else:
                self.config[field] = value

    def change_config(self, config: dict):
        if self.test_config(config):
            self.config = config
        else:
            raise 'config has error'

    def modules(self):
        return self.config['modules']

    def i2c_addresses(self):
        return self.config['i2c_reader']['i2c_device_addresses']

    def n_device_sensors(self):
        return self.config['i2c_reader']['n_device_sensors']

    def calibration_period(self):
        return self.config['data_preprocessor']['calibration_period']

    def recalibration_period(self):
        return self.config['data_preprocessor']['recalibration_period']

    def recalibration_window(self):
        return self.config['data_preprocessor']['recalibration_window']

    def recalibration_cluster_center_weight(self):
        return self.config['data_preprocessor']['recalibration_cluster_center_weight']

    def n_clusters(self):
        return self.config['data_preprocessor']['n_clusters']

    def error_threshold(self):
        return self.config['data_preprocessor']['error_threshold']

    def midi_controller(self):
        return self.config['midi_controller']

    def midi_note_player(self):
        return self.config['midi_note_player']

    def n_smallest_values(self):
        return self.config['data_preprocessor']['n_smallest_values']

    def threshold(self):
        return self.config['data_preprocessor']['threshold']

    @staticmethod
    def test_config(config: dict):
        if not config:
            return False
        # TODO test config
        return True
