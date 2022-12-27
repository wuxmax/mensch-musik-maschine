import {Component, OnInit} from '@angular/core';
import {ModuleDataService} from "../module-data.service";
import {IModule} from "../../models";
import {SensorDataService} from "../../sensor-data/sensor-data.service";

@Component({
  selector: 'app-module-displayer',
  templateUrl: './module-displayer.component.html',
  styleUrls: ['./module-displayer.component.css']
})
export class ModuleDisplayerComponent implements OnInit {
  modules: IModule[] = [];

  constructor(private moduleDataService: ModuleDataService,
              private sensorDataService: SensorDataService) {
  }

  async ngOnInit() {
    await this.moduleDataService.setupModuleDataService();
    await this.sensorDataService.setupSensorDataService();
    this.modules = this.moduleDataService.modules;
  }
}
