import { Injectable } from '@angular/core';
import {IModule, IModuleLogEntry, ISensor} from "../models";
import {BehaviorSubject, interval} from "rxjs";
import {webSocket} from "rxjs/webSocket";
import { FrontendConfigService } from '../frontend-config.service';

@Injectable({
  providedIn: 'root'
})
export class ModuleDataService {
  public modules: IModule[] = [];

  private readonly _moduleLog = new BehaviorSubject<IModuleLogEntry>({} as IModuleLogEntry);
  readonly moduleLog$ = this._moduleLog.asObservable();

  constructor(private frontendConfigService: FrontendConfigService) { }

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
          {name: '15', port: '15', address: '', addressType: 'i2c'} as ISensor]} as IModule,
      {name: 'scene_changer', moduleType: 'SceneChanger', sensors: []} as IModule];
  }

  setupModuleLog() {
    const subject = webSocket('ws://' + this.frontendConfigService.raspberryIp + '/ws/module_logs');
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
