import {Component, Input, OnInit} from '@angular/core';
import {SensorDataService} from "../sensor-data.service";
import {ISensor, ISensorData} from "../../models";

@Component({
  selector: 'app-sensor-data',
  templateUrl: './sensor-data.component.html',
  styleUrls: ['./sensor-data.component.css']
})
export class SensorDataComponent implements OnInit {
  @Input() sensors: ISensor[];
  currentData: ISensorData[] = [];

  constructor(private sensorDataService: SensorDataService) {
  }

  async ngOnInit() {
    this.sensorDataService.currentData$.subscribe((currentData) => {
      this.currentData = currentData.filter((sensorData) => this.sensors.map((s) => s.name).includes(sensorData.sensor.name))
    });
  }
}
