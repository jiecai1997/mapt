import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import { MatDividerModule } from '@angular/material/divider';
import { MatGridListModule } from '@angular/material/grid-list';
import { environment } from "@app/../environments/environment";

//containers
import { AppComponent } from '@app/app';
import { HomepageComponent } from '@app/homepage/homepage.component';

//components
import { MapComponent } from '@app/map/map.component';
import { EdittripComponent } from '@app/edittrip/edittrip.component';
import { TopbarComponent } from '@app/topbar/topbar.component';
import { StatsComponent } from './stats/stats.component';
import { ProfileComponent } from './profile/profile.component';
import { LoginComponent } from './login/login.component';
import { AddtripComponent } from './addtrip/addtrip.component';
import { FlightlistComponent } from './flightlist/flightlist.component';
import { TripnameComponent } from './tripname/tripname.component';
import { TriplistComponent } from './triplist/triplist.component';

let apiKey: string = environment.apiKey;

@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    EdittripComponent,
    TopbarComponent,
    HomepageComponent,
    StatsComponent,
    ProfileComponent,
    LoginComponent,
    AddtripComponent,
    FlightlistComponent,
    TripnameComponent,
    TriplistComponent
  ],
  imports: [
    BrowserModule,
    AgmCoreModule.forRoot({
      apiKey: apiKey
    }),
    MatDividerModule,
    MatGridListModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
