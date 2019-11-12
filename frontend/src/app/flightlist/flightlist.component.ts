import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-flightlist',
  templateUrl: './flightlist.component.html',
  styleUrls: ['./flightlist.component.css']
})
export class FlightlistComponent implements OnInit {
  sampleAirports = ['RDU', 'SEA', 'ORD', 'BWI', 'IAD'];
  trip: any;

  constructor() {
    this.initialize(); //initialize

    this.sampleAirports = this.sampleAirports.map(a => a.toLowerCase()); //standardize case
    this.sampleAirports.sort(); //sort sample airports alphabetically
  }

  ngOnInit() {
  }

  initialize(): void {
    this.trip = {name: 'New Trip', flights: []}
    this.addFlight(); // start with one flight
  }

  addFlight(): void{
    this.trip.flights.push({
      obj: {
        dep: {},
        arr: {}
      },
      forms: {
        dep: {
          date: new FormControl(new Date())
        },
        arr: {
          date: new FormControl(new Date())
        }
      }
    });
  }

  getAirportSuggestions(flight: any): any {
    const depAirport = (flight.obj.dep.airport || '').toLowerCase(),
          arrAirport = (flight.obj.arr.airport || '').toLowerCase();

    console.log({
      dep : this.sampleAirports.filter(airport => airport != arrAirport && airport.startsWith(depAirport)),
      arr : this.sampleAirports.filter(airport => airport != depAirport && airport.startsWith(arrAirport))
    })
    return {
      dep : this.sampleAirports.filter(airport => airport != arrAirport && airport.startsWith(depAirport)),
      arr : this.sampleAirports.filter(airport => airport != depAirport && airport.startsWith(arrAirport))
    }
  }

  // getAirportSuggestions(query: string): any {
  //   if(query){
  //     query = query.toLowerCase(); //ignore case
  //     console.log(this.sampleAirports.filter(airport => airport.toLowerCase().startsWith(query)))
  //     return this.sampleAirports.filter(airport => airport.toLowerCase().startsWith(query));
  //   }else{
  //     return this.sampleAirports;
  //   }
  // }

  getFlightDescription(flight: any, index: number): string {
    if(flight.obj.dep.airport && flight.obj.arr.airport){
      return `${flight.obj.dep.airport} \u2794 ${flight.obj.arr.airport}`; // DEP -> ARR
    }
    return `Flight ${index + 1}`;
  }

  removeFlight(index: number): void{
    this.trip.flights.splice(index, 1);
  }

  saveTrip(): void {
    this.trip.flights = this.trip.flights.map(flight => flight.obj); // remove references to form controls
    console.log(this.trip);
    this.initialize();
  }
}
