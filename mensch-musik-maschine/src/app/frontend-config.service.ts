import { Injectable } from '@angular/core';
import {BehaviorSubject} from "rxjs";
import {IModuleLogEntry} from "./models";

@Injectable({
  providedIn: 'root'
})
export class FrontendConfigService {
  private readonly _raspberryIp = new BehaviorSubject<string>('169.254.16.124');
  readonly raspberryIp$ = this._raspberryIp.asObservable();

  constructor() { }

  get raspberryIp(): string {
    return this._raspberryIp.value;
  }

  set raspberryIp(value: string) {
    this._raspberryIp.next(value);
  }
}
