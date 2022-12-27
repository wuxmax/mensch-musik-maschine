import {Component, Input} from '@angular/core';
import {IModule} from "../../models";

@Component({
  selector: 'app-module-data',
  templateUrl: './module-data.component.html',
  styleUrls: ['./module-data.component.css']
})
export class ModuleDataComponent {
  @Input() module: IModule;
}
