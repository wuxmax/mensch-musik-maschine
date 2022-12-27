import {Component, Input, OnChanges} from '@angular/core';
import {MatDialog, MatDialogRef} from "@angular/material/dialog";
import {BacklogDialogComponent} from "../backlog-dialog/backlog-dialog.component";

@Component({
  selector: 'app-sensor-backlog',
  templateUrl: './sensor-backlog.component.html',
  styleUrls: ['./sensor-backlog.component.css']
})
export class SensorBacklogComponent implements OnChanges {
  @Input() value: number;
  backlog: number[] = [];
  display = false;
  dialogRef: MatDialogRef<any>;

  constructor(public dialog: MatDialog) {}

  ngOnChanges() {
    this.backlog.push(this.value);
    this.backlog = this.backlog.slice(-50)
  }

  toggleBacklog() {
    if (this.dialogRef) {
      this.dialogRef.close();
    }
    this.dialogRef = this.dialog.open(BacklogDialogComponent, { data: { backlog: this.backlog} });
  }
}
