
import { AgmCoreModule } from '@agm/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule }    from '@angular/common/http';
import { MatDividerModule } from '@angular/material/divider';
import { NgModule } from '@angular/core';


//containers
import { AppComponent } from '@app/app';
import { environment } from "@app/../environments/environment";
import { HomepageComponent } from '@app/components/homepage/homepage.component';

//components
import { MapComponent } from '@app/components/map/map.component';
import { EdittripComponent } from '@app/components/edittrip/edittrip.component';
import { TopbarComponent } from '@app/components/topbar/topbar.component';
import { StatsComponent } from '@app/components/stats/stats.component';

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
    AgmCoreModule.forRoot({
      apiKey: apiKey
    }),
    BrowserModule,
    HttpClientModule,
    MatDividerModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
