import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SensorDataComponent } from './sensor-data/sensor-data.component';
import { DataPointComponent } from './data-point/data-point.component';
import { SensorBacklogComponent } from './sensor-backlog/sensor-backlog.component';
import {MatButtonModule} from "@angular/material/button";
import { BacklogDialogComponent } from './backlog-dialog/backlog-dialog.component';
import {MatDialogModule} from "@angular/material/dialog";



@NgModule({
    declarations: [
        SensorDataComponent,
        DataPointComponent,
        SensorBacklogComponent,
        BacklogDialogComponent
    ],
    exports: [
        SensorDataComponent
    ],
  imports: [
    CommonModule,
    MatButtonModule,
    MatDialogModule
  ]
})
export class SensorDataModule { }
