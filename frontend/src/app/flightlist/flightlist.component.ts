import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-flightlist',
  templateUrl: './flightlist.component.html',
  styleUrls: ['./flightlist.component.css']
})
export class FlightlistComponent implements OnInit {
  @Input() isAddTrip: boolean;
  trips: Array<any> = [];

  sampleAirports = ['RDU', 'SEA', 'ORD', 'BWI', 'IAD'];
  lastAddedTo: number; // trip which most recently had a flight added to it

  constructor() {}

  ngOnInit() {
    this.initialize();
  }

  initialize(): void {
    this.sampleAirports.sort(); //sort sample airports alphabetically

    if(this.isAddTrip){
      // add one trip with one flight
      this.trips = [{name: 'New Trip', color: "red", flights: []}]
      this.addFlight(0); // start with one flight
    }else{
      //TODO: get trip data
      this.trips = [
        {color: "red", name: "Wedding", flights: [{
          arr: {airport: "RDU", date: new Date('9/10/19'), time: "17:50"},
          dep: {airport: "PHL", date: new Date('9/10/19'), time: "16:10"}
        }]},
        {color: "blue", name: "Graduation", flights: [
          {arr: {airport: "IAD", date: new Date('6/8/19'), time: "11:50"},
          dep: {airport: "SEA", date: new Date('6/8/19'), time: "14:10"}},
          {arr: {airport: "SEA", date: new Date('6/11/19'), time: "8:35"},
          dep: {airport: "IAD", date: new Date('6/11/19'), time: "16:30"}}
        ]},
      ];
    }
  }

  addFlight(tripIndex: number): void{
    this.trips[tripIndex].flights.push({dep: {}, arr: {}});
    this.lastAddedTo = tripIndex;
  }

  getAirportSuggestions(flight: any, isDep: boolean): any {
    const depAirport = (flight.dep.airport || '').toLowerCase(),
          arrAirport = (flight.arr.airport || '').toLowerCase();

    var find: any, exclude: any;
    if(isDep){
      find = depAirport, exclude = arrAirport;
    }else{
      find = arrAirport, exclude = depAirport;
    }

    return this.sampleAirports.filter(airport => airport.toLowerCase() != exclude && airport.toLowerCase().startsWith(find));
  }

  getFlightDescription(flight: any, index: number): string {
    if(flight.dep.airport && flight.arr.airport){
      return `${flight.dep.airport} \u2794 ${flight.arr.airport}`; // DEP -> ARR
    }
    return `Flight ${index + 1}`;
  }

  removeFlight(tripIndex: number, flightIndex: number): void{
    this.trips[tripIndex].flights.splice(flightIndex, 1);
  }

  saveTrip(): void {
    console.log(this.trips);
    this.initialize();
  }
}
