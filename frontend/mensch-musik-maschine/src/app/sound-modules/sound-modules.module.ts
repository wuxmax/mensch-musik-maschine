import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ModuleDataComponent } from './module-data/module-data.component';
import { ModuleDisplayerComponent } from './module-displayer/module-displayer.component';
import {SensorDataModule} from "../sensor-data/sensor-data.module";
import {MatLegacyTabsModule} from "@angular/material/legacy-tabs";
import { ModuleLoggerComponent } from './module-logger/module-logger.component';



@NgModule({
  declarations: [
    ModuleDataComponent,
    ModuleDisplayerComponent,
    ModuleLoggerComponent
  ],
  exports: [
    ModuleDisplayerComponent
  ],
  imports: [
    CommonModule,
    SensorDataModule,
    MatLegacyTabsModule
  ]
})
export class SoundModulesModule { }
