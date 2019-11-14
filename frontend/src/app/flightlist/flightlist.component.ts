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

  getAirportSuggestions(flight: any, isDep: boolean): any {
    const depAirport = (flight.obj.dep.airport || '').toLowerCase(),
          arrAirport = (flight.obj.arr.airport || '').toLowerCase();

    var find: any, exclude: any;
    if(isDep){
      find = depAirport, exclude = arrAirport;
    }else{
      find = arrAirport, exclude = depAirport;
    }

    return this.sampleAirports.filter(airport => airport.toLowerCase() != exclude && airport.toLowerCase().startsWith(find));
  }

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
