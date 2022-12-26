import json
import threading
from time import sleep
from typing import List

import numpy as np

from fastapi import FastAPI, WebSocket

from value_stack import ValueStack
from simple_data_preprocessor import MatrixDataPreprocessor
from matrix_processor import MatrixProcessor
from i2c_reader import I2CReader
from config_manager import ConfigManager
from models import SensorsOut, ModulesOut, ClusterBorders
from module_logger import ModuleLogger

# CONFIG_FILE = "config.yml"
CONFIG_FILE = "config_real.yml"
# CONFIG_FILE = "config_test.yml"
# CONFIG_FILE = "config_fader.yml"

app = FastAPI(title="MenschMusikMaschine")

config_manager: ConfigManager = ConfigManager(config_name=CONFIG_FILE)
value_stack: ValueStack = ValueStack(config_manager=config_manager)
module_logger: ModuleLogger = ModuleLogger()
reader: I2CReader = I2CReader(config_manager, value_stack)
datpro: MatrixDataPreprocessor = MatrixDataPreprocessor(config_manager, value_stack)
matpro: MatrixProcessor = MatrixProcessor(config_manager, module_logger, printing=True)
x: threading.Thread


def application():
    a = [100, 200, 500, 1000]
    for i in a:
        print('going')
        for j in range(i):
            current_sensor_values = reader.load_sensor_list()
            if not datpro.cluster_borders[0][0] == -1:
                normalized_values = datpro.sensor_to_module(datpro.normalize(current_sensor_values))
                matpro.process(normalized_values)
        datpro.calibrate()

    while True:
        print('going')
        for j in range(config_manager.recalibration_period()):
            current_sensor_values = reader.load_sensor_list()
            normalized_values = datpro.sensor_to_module(datpro.normalize(current_sensor_values))
            matpro.process(normalized_values)
        datpro.calibrate()


@app.on_event("startup")
async def startup_event():
    print('Hello')
    x = threading.Thread(target=application, args=())
    x.start()


@app.on_event("shutdown")
def shutdown_event():
    print('Bye-bye')


@app.get("/")
async def root():
    return {"message": "Hello You! The MenschMusikMaschine is ready!"}


@app.put(path="/config", summary="Change single value. Values are lost on restart")
async def config(field: str, value: str, menu: str = ''):
    config_manager.change_field(menu, field, value)


@app.put(path="/choose_config", summary="Load or reload the config yml file by name")
async def choose_config(name: str):
    config_manager.load_config(name)


@app.get(path="/config")
async def config():
    return config_manager.config


@app.get(path="/sensors",
         response_model=SensorsOut)
async def sensors():
    print(reader.sensor_values)
    return reader.sensor_values


@app.get(path="/cluster_borders",
         response_model=ClusterBorders)
async def cluster_borders():
    return {'cluster_borders': datpro.cluster_borders}


@app.get(path="/smallest_values",
         response_model=List[List[List[float]]])
async def smallest_values():
    values = value_stack.get_values()
    return {'smallest_values': [[np.partition((np.array(values)[:, i, j]), config_manager.n_smallest_values())[
                                 :config_manager.n_smallest_values() - 1] for j in range(len(values[0][0]))] for i in
                                range(len(values[0]))]}


@app.get(path="/modules",
         response_model=ModulesOut)
async def modules():
    return matpro.modules


@app.put(path="/calibrate", summary="(re)calibrate sensors with last x values. Sensors can be filtered by i2c_address")
async def calibrate(i2c_address: str = ''):
    print(i2c_address)
    datpro.calibrate(i2c_address)
    return ''


@app.websocket("/ws/sensor_values")
async def sensor_values(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.receive()
        await websocket.send_json({'sensor_data': reader.sensor_values,
                                   'cluster_borders': datpro.cluster_borders})


@app.websocket("/ws/module_logs")
async def module_logs(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.receive()
        await websocket.send_json({'module_logs': module_logger.get_logs()})
