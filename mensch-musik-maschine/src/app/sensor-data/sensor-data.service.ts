import { Injectable } from '@angular/core';
import {BehaviorSubject, interval} from 'rxjs';
import {IDatapoint, IModule, ISensor, ISensorData} from "../models";
import { webSocket } from 'rxjs/webSocket';
import {HttpClient} from "@angular/common/http";
import {FrontendConfigService} from "../frontend-config.service";

@Injectable({
  providedIn: 'root'
})
export class SensorDataService {

  sensors: ISensor[] = [];

  private readonly _currentData = new BehaviorSubject<ISensorData[]>([] as ISensorData[]);
  readonly currentData$ = this._currentData.asObservable();

  constructor(private http: HttpClient,
              private frontendConfigService: FrontendConfigService) { }

  public get currentData(): ISensorData[] {
    return this._currentData.getValue();
  }

  public set currentData(val: ISensorData[]) {
    this._currentData.next(val);
  }

  setupSensorDataService() {
    this.loadSensors();
    this.setupDataStream();
  }

  loadSensors() {
    // TODO load given Sensors
    this.sensors = [{name: 'testArduino', port: '2', address: '', addressType: 'i2c'} as ISensor,
      {name: 'testArduino2', port: '2', address: '', addressType: 'i2c'} as ISensor,
      {name: 'testArduino3', port: '2', address: '', addressType: 'i2c'} as ISensor,
      {name: 'testArduino4', port: '2', address: '', addressType: 'i2c'} as ISensor]
  }

  setupDataStream() {
    const subject = webSocket('ws://' + this.frontendConfigService.raspberryIp + '/ws/sensor_values');
    const subscription = subject.subscribe({
      next: msg => {
        if (this.currentData.length === 0) {
          this.currentData = Object.keys((msg as any).sensor_data).map((key: string, index: number) => {
            return {
              sensor: {
                name: key
              } as ISensor,
            dataPoints: (msg as any).sensor_data[key].map((i: number, indexDatapoint: number) => {
              return { totalValue: i, clusterBorder: -1} as IDatapoint;
              }) as IDatapoint[]
          } as ISensorData;
          });
        } else {
          Object.keys((msg as any).sensor_data).map((key: string, index: number) => {
            this.currentData[index].sensor = {
              name: key
            } as ISensor;
            (msg as any).sensor_data[key].map((i: number, indexDatapoint: number) => {
              this.currentData[index].dataPoints[indexDatapoint].totalValue = i;
            });
            (msg as any).cluster_borders[index].map((i: number, indexDatapoint: number) => {
              this.currentData[index].dataPoints[indexDatapoint].clusterBorder = Math.round(i);
            });
          });
        }
      },
      error: err => console.log(err)
    });
    interval(1000).subscribe(() => {
      subject.next(JSON.stringify({op: 'hello'}));
    });
  }

}
