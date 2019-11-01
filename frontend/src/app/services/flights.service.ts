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

    const listOfJsons = [
      { 'flight': {'firstPoint': {'lat': 32.2226, 'long': -110.9747}, 'secondPoint': {'lat': 35.9940, 'long': -78.8986} }},
      { 'flight': {'firstPoint': {'lat': 25.7617, 'long': -80.1918}, 'secondPoint': {'lat': 35.9940, 'long': -78.8986} }}
    ];

    const listOfFlights:Flight[] = listOfJsons.map(x => this.coordToFlight(x));
    // this.http.get(this.serverURL + '/list').subscribe( flightData => {
    //   console.log('flights', flightData);
    // });

    return of(listOfFlights);
  }


  coordToFlight(flightObj): Flight {
    const firstPoint:Point = {
      lat: flightObj['flight']['firstPoint']['lat'],
      long: flightObj['flight']['firstPoint']['long']
    }

    const secondPoint:Point = {
      lat: flightObj['flight']['secondPoint']['lat'],
      long: flightObj['flight']['secondPoint']['long']
    }

    const myFlight:Flight = {
      startPoint: firstPoint,
      endPoint: secondPoint,
      opacity: 1
    }

    return myFlight;

  }

}
