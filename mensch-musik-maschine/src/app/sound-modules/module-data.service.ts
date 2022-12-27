import { Injectable } from '@angular/core';
import {IDatapoint, IModule, IModuleData, IModuleLogEntry, ISensor, ISensorData} from "../models";
import {BehaviorSubject, interval} from "rxjs";
import {webSocket} from "rxjs/webSocket";

@Injectable({
  providedIn: 'root'
})
export class ModuleDataService {
  public modules: IModule[] = [];

  private readonly _moduleLog = new BehaviorSubject<IModuleLogEntry>({} as IModuleLogEntry);
  readonly moduleLog$ = this._moduleLog.asObservable();

  constructor() { }

  async setupModuleDataService() {
    await this.loadModules();
    this.setupModuleLog();
  }

  async loadModules() {
    this.modules = [
      {name: 'Overview', moduleType: 'Hold', sensors: [
          {name: '15', port: '15', address: '', addressType: 'i2c'} as ISensor,
          {name: '14', port: '14', address: '', addressType: 'i2c'} as ISensor,
          {name: '13', port: '13', address: '', addressType: 'i2c'} as ISensor,
          {name: '11', port: '11', address: '', addressType: 'i2c'} as ISensor]} as IModule,
      {name: 'fader', moduleType: 'Fader', sensors: [
          {name: '13', port: '13', address: '', addressType: 'i2c'} as ISensor,
          {name: '14', port: '14', address: '', addressType: 'i2c'} as ISensor]} as IModule,
      {name: 'hold_1', moduleType: 'Hold', sensors: [
          {name: '11', port: '11', address: '', addressType: 'i2c'} as ISensor]} as IModule,
      {name: 'hold_2', moduleType: 'Hold', sensors: [
          {name: '15', port: '15', address: '', addressType: 'i2c'} as ISensor]} as IModule];
  }

  setupModuleLog() {
    const subject = webSocket('ws://172.20.10.7:80/ws/module_logs');
    const subscription = subject.subscribe({
      next: (msg: any) => {
        msg.module_logs.map((log: any) => {
          this._moduleLog.next({module: {name: log[0]} as IModule, log: log[1]});
        })
      },
      error: err => console.log(err)
    });
    interval(2000).subscribe(() => {
      subject.next(JSON.stringify({op: 'hello'}));
    });
  }
}
