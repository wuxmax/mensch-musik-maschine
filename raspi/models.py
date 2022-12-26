from typing import List
from pydantic import BaseModel


class Config:
    name: str


class ConfigOut(Config, BaseModel):
    name: str


class ConfigIn(Config, BaseModel):
    name: str


class Sensor(BaseModel):
    name: str


class Module(BaseModel):
    name: str


class SensorsOut(BaseModel):
    sensors: List[Sensor]


class ModulesOut(BaseModel):
    module: List[Sensor]


class SensorValues(BaseModel):
    sensors: List[List[float]]


class ClusterBorders(BaseModel):
    cluster_borders: List[List[float]]

