import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import {MatTabsModule} from "@angular/material/tabs";
import {SensorDataModule} from "./sensor-data/sensor-data.module";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {SoundModulesModule} from "./sound-modules/sound-modules.module";
import {HttpClientModule} from "@angular/common/http";
import { FrontendConfigComponent } from './frontend-config/frontend-config.component';
import {MatFormFieldModule} from "@angular/material/form-field";
import {ReactiveFormsModule} from "@angular/forms";
import {MatAutocompleteModule} from "@angular/material/autocomplete";
import {MatInputModule} from "@angular/material/input";
import {MatButtonModule} from "@angular/material/button";

@NgModule({
  declarations: [
    AppComponent,
    FrontendConfigComponent
  ],
  imports: [
    BrowserModule,
    MatTabsModule,
    SensorDataModule,
    BrowserAnimationsModule,
    SoundModulesModule,
    HttpClientModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MatInputModule,
    MatButtonModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
