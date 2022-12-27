export interface ISensorData {
  sensor: ISensor;
  dataPoints: IDatapoint[];
}

export interface IModuleData {
  module: IModule;
  dataPoints: number[];
}

export interface IDatapoint {
  totalValue: number;
  clusterBorder: number;
}

export interface ISensor {
  name: string;
  port: string;
  address: string;
  addressType: string;
}

export interface IModule {
  name: string;
  moduleType: string;
  sensors: ISensor[];
}

export interface IModuleLogEntry {
  module: IModule;
  log: string;
}
