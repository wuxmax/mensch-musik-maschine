import { Component, OnInit, ViewChild } from '@angular/core';
import {FrontendConfigService} from "../frontend-config.service";
import {map, Observable, startWith} from "rxjs";
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-frontend-config',
  templateUrl: './frontend-config.component.html',
  styleUrls: ['./frontend-config.component.css']
})
export class FrontendConfigComponent implements OnInit {
  raspberryIp = new FormControl('');
  options: string[] = ['169.254.16.124', '172.20.10.--'];
  filteredOptions: Observable<string[]>;


  constructor(private frontendConfigService: FrontendConfigService) {
  }

  ngOnInit() {
    this.filteredOptions = this.raspberryIp.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || '')),
    );
  }

  _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

  updateRaspberryId() {
    this.frontendConfigService.raspberryIp = this.raspberryIp.value || '';
    // this.raspberryIp.setValue($event);
  }
}
