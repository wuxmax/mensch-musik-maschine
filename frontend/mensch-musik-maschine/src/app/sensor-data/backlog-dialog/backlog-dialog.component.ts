import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-backlog-dialog',
  templateUrl: './backlog-dialog.component.html',
  styleUrls: ['./backlog-dialog.component.css']
})
export class BacklogDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<BacklogDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {backlog: number[]},
  ) {}
}
