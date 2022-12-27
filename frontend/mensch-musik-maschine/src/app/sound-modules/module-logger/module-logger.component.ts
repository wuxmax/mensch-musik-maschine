import {Component, Input, OnInit} from '@angular/core';
import {ModuleDataService} from "../module-data.service";
import {IModule} from "../../models";

@Component({
  selector: 'app-module-logger',
  templateUrl: './module-logger.component.html',
  styleUrls: ['./module-logger.component.css']
})
export class ModuleLoggerComponent implements OnInit {
  @Input() module: IModule;
  logStack: string[] = []

  constructor(private moduleDataService: ModuleDataService) {
  }

  ngOnInit() {
    this.moduleDataService.moduleLog$.subscribe((log) => {
      if (log.module && log.module.name === this.module.name) {
        this.logStack.push(log.log);
        this.logStack = this.logStack.slice(-10);
      }
    });
  }


}
