import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {interval} from "rxjs";

@Component({
  selector: 'app-data-point',
  templateUrl: './data-point.component.html',
  styleUrls: ['./data-point.component.css']
})
export class DataPointComponent implements OnInit, OnChanges {
  @Input() value: number;
  @Input() clusterBorder: number;
  previousValue: number;
  change = 0.0;

  constructor() {}

  async ngOnInit() {
  }

  color() {
    if (this.change === 0) {
      return '#FFFFFF';
    }
    if (this.value > this.clusterBorder) {
      return '#0000FF' + (Math.round(this.change * 255)).toString(16);
    } else {
      return '#FF0000' + (Math.round(this.change * 255)).toString(16);
    }
  }

  fontColor() {
    if (this.change > 0.5) {
      return '#FFFFFF'
    } else {
      return '#000000'
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (!changes['value']) {
      return;
    }
    if (this.previousValue) {
      this.change = Math.min(1.0, this.change + Math.abs(this.previousValue - this.value) / 30.0);
    }
    this.previousValue = this.value;
  }
}
