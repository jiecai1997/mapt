import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Flight } from '../models/Flight';
import { Point } from '../models/Point';
import { LoginService } from './login.service';

@Injectable({
  providedIn: 'root'
})
export class FlightsService {

  constructor(private http:HttpClient,
              private loginService:LoginService) { }

  private serverURL = 'http://localhost:5000';


  getFlights(){

    const sessionToken = this.loginService.getToken();
    console.log('token check', sessionToken);

    const uid = this.loginService.getUID();
    const httpOptions = this.createAuthOptions();

    return this.http.get(this.serverURL + '/flights/' + uid, httpOptions);
  
  }

  getTrips() {
    const uid = this.loginService.getUID();
    const httpOptions = this.createAuthOptions();
    this.http.get(this.serverURL + '/trips/' + uid, httpOptions).subscribe(result => {
      console.log('trip result from service', result);
    })

    return this.http.get(this.serverURL + '/trips/' + uid, httpOptions);
  }

  // eventually, have the backend give us a session token for the current user, and then feed that session token as well
  // as the id into the body of the request. before the request is fulfilled and the flight is added, the session token sent by
  // the frontend through the service must match the session token stored by the backend.
  // we'd need a table for that
  // 
  // we also need to think about color - will that get fed in from the frontend? Color string that can be sent w requestBody,
  // have that as a column - will need that in save trip as well
  addTrip(tripName:string, color:string, flights:any[]){
    const reqBody = {'uid': this.loginService.getUID(), 'trip_name': tripName, 'color': color, 'flights': flights};
    console.log('reqBody', reqBody);

    const httpOptions = this.createAuthOptions();

    return this.http.post(this.serverURL + '/trips/add', reqBody, httpOptions);
  }

  // anything to change here? Similar to add right? FIGURE OUT A WAY TO GET SESSIONTOKEN INTO THE HEADERS?
  updateTrip(tripID:string, tripName:string, color:string, flights:any[]){
    console.log('tripId', tripID);
    const reqBody = {'color': color, 'uid': this.loginService.getUID(), 'trip_name': tripName, 'trip_id': tripID, 'flights': flights, 'random': 1234};

    const httpOptions = this.createAuthOptions();

    return this.http.post(this.serverURL + '/trips/update', reqBody, httpOptions);
  }


  public getStats(){
    const httpOptions = this.createAuthOptions();

    this.http.get<any>(this.serverURL + '/stats/' + this.loginService.getUID(), httpOptions).subscribe(result => {
      console.log('stats result from service', result);
    })

    return this.http.get<any>(this.serverURL + '/stats/' + this.loginService.getUID(), httpOptions);
  }


  public getProfileInfo(){
    const httpOptions = this.createAuthOptions();
    const uid = this.loginService.getUID();

    return this.http.get(this.serverURL + '/profile/' + uid, httpOptions);

  }

  // made return statement for failure according to how we specified it in notepad, but do we want to take a separate course of action in
  // the event of failure?
  public updateProfileInfo(username: string, isPublic:boolean){
    const httpOptions = this.createAuthOptions();
    const reqBody = {
      'uid': this.loginService.getUID(),
      'username': username,
      'isPublic': isPublic
    }

    return this.http.post(this.serverURL + '/profile/update', reqBody, httpOptions);
  }

  public verifyLogin(){
    const httpOptions = this.createAuthOptions();
    const uid = this.loginService.getUID()

    return this.http.get(this.serverURL + '/login/verify/' + uid, httpOptions);
  }


  public autocompleteAirports(search: string){
    return this.http.get(this.serverURL + '/airports/' + search);
  }


  public autocompleteAirlines(search: string){
    return this.http.get(this.serverURL + '/airlines/' + search);
  }

  private createAuthOptions(){

    const sessionToken = this.loginService.getToken() || "SESSIONTOKEN";

    const httpOptions = {
      headers: new HttpHeaders({
        'Authorization': sessionToken
      })
    };

    return httpOptions;
  }


}
