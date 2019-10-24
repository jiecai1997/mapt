import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import { MatDividerModule } from '@angular/material/divider';
import { environment } from "../environments/environment";

//containers
import { AppComponent } from './app';
import { HomepageComponent } from './homepage/homepage.component';

//components
import { MapComponent } from './map/map.component';
import { EdittripComponent } from './edittrip/edittrip.component';
import { TopbarComponent } from './topbar/topbar.component';
import { StatsComponent } from './stats/stats.component';

let apiKey: string = environment.apiKey;

@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    EdittripComponent,
    TopbarComponent,
    HomepageComponent,
    StatsComponent
  ],
  imports: [
    BrowserModule,
    AgmCoreModule.forRoot({
      apiKey: apiKey
    }),
    MatDividerModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
