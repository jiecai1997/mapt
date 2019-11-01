import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MapComponent } from '@app/components/map/map.component';
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './profile/profile.component';
import { EdittripComponent } from './components/edittrip/edittrip.component';
import { AddtripComponent } from './addtrip/addtrip.component';
import { HomepageComponent } from './components/homepage/homepage.component';


const routes: Routes = [
  { path: 'map', component: MapComponent },
  { path: 'home', component: HomepageComponent },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'addtrip', component: AddtripComponent },
  { path: 'edittrip', component: EdittripComponent },
  { path: '**', redirectTo: '/home', pathMatch: 'full' } // default to homepage
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
