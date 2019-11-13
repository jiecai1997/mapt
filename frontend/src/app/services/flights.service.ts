import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Flight } from '../models/Flight';
import { Point } from '../models/Point';

@Injectable({
  providedIn: 'root'
})
export class FlightsService {

  constructor(private http:HttpClient) { }

  private serverURL = 'http://localhost:5000';

  getFlights():Observable<Flight[]> {

    // this.http.get(this.serverURL + '/list').subscribe( flightData => {
    //   console.log('flights', flightData);
    // });
    return this.http.get<Flight[]>(this.serverURL + '/flights')   
  }

  // eventually, have the backend give us a session token for the current user, and then feed that session token as well
  // as the id into the body of the request. before the request is fulfilled and the flight is added, the session token sent by
  // the frontend through the service must match the session token stored by the backend.
  // we'd need a table for that
  addTrip(uid:number, sessionToken:number, tripName:string, flights:Flight[]){
    const reqBody = {'userID': uid, sessionToken: sessionToken, 'tripName': tripName, 'flights': flights};
    console.log('reqBody', reqBody);
    return this.http.post(this.serverURL + '/trips/add', reqBody).subscribe(result => {
      if(result['success'] == 'true'){
        return 'Success';
      }
      else{
        return 'Add trip failed';
      }
    })

  }


}
