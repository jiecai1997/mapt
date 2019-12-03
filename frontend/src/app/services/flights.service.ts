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

  // FIX THIS SHIT
  getFlights(){

    const sessionToken = this.loginService.getToken();
    console.log('token check', sessionToken);

    const uid = this.loginService.getUID();
    const httpOptions = this.createAuthOptions();

    return this.http.get(this.serverURL + '/flights', httpOptions);
  
  }

  getTrips():Observable<any> {
    const httpOptions = this.createAuthOptions();
    return this.http.get<any>(this.serverURL + '/trips', httpOptions);
  }

  // eventually, have the backend give us a session token for the current user, and then feed that session token as well
  // as the id into the body of the request. before the request is fulfilled and the flight is added, the session token sent by
  // the frontend through the service must match the session token stored by the backend.
  // we'd need a table for that
  // 
  // we also need to think about color - will that get fed in from the frontend? Color string that can be sent w requestBody,
  // have that as a column - will need that in save trip as well
  addTrip(userID:string, tripName:string, color:string, flights:any[]){
    const reqBody = {'userID': this.loginService.getUID(), 'tripName': tripName, 'color': color, 'flights': flights};
    console.log('reqBody', reqBody);

    const httpOptions = this.createAuthOptions();

    return this.http.post(this.serverURL + '/trips/add', reqBody, httpOptions).subscribe(result => {
      if(result['success'] == 'true'){
        return true;
      }
      else{
        console.log(result['error']);
        return false;
      }
    })

  }

  // anything to change here? Similar to add right? FIGURE OUT A WAY TO GET SESSIONTOKEN INTO THE HEADERS?
  updateTrip(tripID:string, tripName:string, color:string, flights:any[]){
    const reqBody = {'userID': this.loginService.getUID(), 'tripID': tripID, 'tripName': tripName, 'color': color, 'flights': flights};

    const httpOptions = this.createAuthOptions();

    return this.http.put(this.serverURL + '/trips/update', reqBody, httpOptions).subscribe(result => {
      if(result['success'] == 'true'){
        return 'Success';
      }
      else{
        return 'Modifying trip failed';
      }
    })

  }


  public getStats(uid:number){
    const httpOptions = this.createAuthOptions();
    return this.http.get(this.serverURL + '/stats/?uid=' + this.loginService.getUID(), httpOptions).subscribe(result => {
      if(result['success'] == 'true'){
        return result;
      }
      else{
        console.log('result', result);
        return 'FAILED';
      }
    })
  }


  public getProfileInfo(){
    const httpOptions = this.createAuthOptions();
    const uid = this.loginService.getUID();

    return this.http.get(this.serverURL + '/profile?' + uid, httpOptions).subscribe(result => {
      if(result['success'] == 'true'){
        return result;
      }
      else{
        console.log('GETTING PROFILE INFO FAILED');
      }
    })

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

    return this.http.post(this.serverURL + '/profile/update', reqBody, httpOptions).subscribe(result => {
      if(result['success'] == 'true'){
        return result;
      }
      else{
        console.log('FAILED TO UPDATE ACCOUNT INFO')
        return result;
      }
    })

  }


  private createAuthOptions(){

    const sessionToken = this.loginService.getToken();

    const httpOptions = {
      headers: new HttpHeaders({
        'Authorization': sessionToken
      })
    };

    return httpOptions;
  }


}
