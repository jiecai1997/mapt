import { AgmCoreModule } from '@agm/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule }    from '@angular/common/http';
import { MatDividerModule } from '@angular/material/divider';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabsModule } from '@angular/material/tabs';
import { NgModule } from '@angular/core';
import { environment } from "@app/../environments/environment";

//containers
import { AppComponent } from '@app/app';
import { HomepageComponent } from '@app/components/homepage/homepage.component';

//components
import { MapComponent } from '@app/components/map/map.component';
import { EdittripComponent } from '@app/components/edittrip/edittrip.component';
import { TopbarComponent } from '@app/components/topbar/topbar.component';
import { StatsComponent } from '@app/components/stats/stats.component';
import { ProfileComponent } from './profile/profile.component';
import { LoginComponent } from './login/login.component';
import { AddtripComponent } from './addtrip/addtrip.component';
import { FlightlistComponent } from './flightlist/flightlist.component';
import { TripnameComponent } from './tripname/tripname.component';
import { TriplistComponent } from './triplist/triplist.component';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MappageComponent } from './components/mappage/mappage.component';

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
    TriplistComponent,
    MappageComponent
  ],
  imports: [
    AgmCoreModule.forRoot({
      apiKey: apiKey
    }),
    AppRoutingModule,
    BrowserModule,
    HttpClientModule,
    MatDividerModule,
    MatGridListModule,
    MatCardModule,
    MatToolbarModule,
    MatTabsModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
