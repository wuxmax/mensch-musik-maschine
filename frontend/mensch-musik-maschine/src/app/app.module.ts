import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import {MatTabsModule} from "@angular/material/tabs";
import {SensorDataModule} from "./sensor-data/sensor-data.module";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {SoundModulesModule} from "./sound-modules/sound-modules.module";
import {HttpClientModule} from "@angular/common/http";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    MatTabsModule,
    SensorDataModule,
    BrowserAnimationsModule,
    SoundModulesModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
