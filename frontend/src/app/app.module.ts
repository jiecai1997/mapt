import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import { MatDividerModule } from '@angular/material/divider';
import { environment } from "@app/../environments/environment";

//containers
import { AppComponent } from '@app/app';
import { HomepageComponent } from '@app/homepage/homepage.component';

//components
import { MapComponent } from '@app/map/map.component';
import { EdittripComponent } from '@app/edittrip/edittrip.component';
import { TopbarComponent } from '@app/topbar/topbar.component';
import { StatsComponent } from '@app/stats/stats.component';

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
