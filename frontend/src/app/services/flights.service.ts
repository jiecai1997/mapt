import { Injectable } from '@angular/core';
import { Flight } from '../models/Flight';
import { Point } from '../models/Point';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FlightsService {

  constructor() { }

  getFlights():Observable<Flight[]> {

    const listOfJsons = [
      { 'flight': {'firstPoint': {'lat': 32.2226, 'long': -110.9747}, 'secondPoint': {'lat': 35.9940, 'long': -78.8986} }},
      { 'flight': {'firstPoint': {'lat': 25.7617, 'long': -80.1918}, 'secondPoint': {'lat': 35.9940, 'long': -78.8986} }}
    ];

    const listOfFlights:Flight[] = listOfJsons.map(x => this.coordToFlight(x));

    return of(listOfFlights);
  }


  coordToFlight(flightObj): Flight {
    const firstPoint = {
      lat: flightObj['flight']['firstPoint']['lat'],
      long: flightObj['flight']['firstPoint']['long']
    }

    const secondPoint = {
      lat: flightObj['flight']['secondPoint']['lat'],
      long: flightObj['flight']['secondPoint']['long']
    }

    const myFlight:Flight = {
      startPoint: firstPoint,
      endPoint: secondPoint
    }

    return myFlight;

  }

}
