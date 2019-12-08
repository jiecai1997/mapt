import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { FlightsService } from '@app/services/flights.service';
import { LoginService } from '@app/services/login.service';



@Component({
  selector: 'app-flightlist',
  templateUrl: './flightlist.component.html',
  styleUrls: ['./flightlist.component.css']
})
export class FlightlistComponent implements OnInit {
  @Input() isAddTrip: boolean;
  trips: Array<any> = [];

  sampleAirports = [];
  colors = ['red', 'blue', 'green'];
  lastAddedTo: number; // trip which most recently had a flight added to it

  showSpinner: boolean = false;

  constructor(private router: Router, private flightsService: FlightsService, private loginService:LoginService) {}

  ngOnInit() {
    this.initialize();
  }

  initialize(): void {
    this.sampleAirports.sort(); //sort sample airports alphabetically

    if(this.isAddTrip){
      // add one trip with one flight
      this.trips = [{tripName: 'New Trip', color: "blue", flights: []}]
      this.addFlight(0); // start with one flight
    }else{
      // get trip data
      this.flightsService.getTrips().subscribe(
        tripsObj => {
            this.trips = tripsObj['trips'];
            console.log('trips are', this.trips)
          });
    }
  }

  addFlight(tripIndex: number): void{
    this.trips[tripIndex].flights.push({dep: {}, arr: {}});
    this.lastAddedTo = tripIndex;
  }

  getAirportSuggestions(flight: any, isDep: boolean): any {
    const depAirport = (flight.departAirport || '').toLowerCase(),
          arrAirport = (flight.arrivalAirport || '').toLowerCase();

    var find: any, exclude: any;
    if(isDep){
      find = depAirport, exclude = arrAirport;
    }else{
      find = arrAirport, exclude = depAirport;
    }

    return this.sampleAirports.filter(airport => airport.toLowerCase() != exclude && airport.toLowerCase().startsWith(find));
  }

  getFlightDescription(flight: any, index: number): string {
    if(flight.departAirport && flight.arrivalAirport){
      return `${flight.departAirport} \u2794 ${flight.arrivalAirport}`; // DEP -> ARR
    }
    return `Flight ${index + 1}`;
  }

  removeFlight(tripIndex: number, flightIndex: number): void{
    this.trips[tripIndex].flights.splice(flightIndex, 1);
  }

  saveTrip(tripIndex): void {
    this.showSpinner = true;
    const trip = this.trips[tripIndex];

    if(this.isAddTrip){
      // add trip
      this.flightsService.addTrip(trip.tripName, trip.color, trip.flights).subscribe(result => {
        if(result['success'] == 'true'){
          const uid = this.loginService.getUID().toString();
          console.log('uid to navigate to after add trip', uid);
          this.router.navigate([uid]);
        } else{
          console.log(result['error']); //TODO: deal with this case
        }
        this.showSpinner = false;
      })
    }else{
      // update trip
      this.flightsService.updateTrip(trip.tripID, trip.tripName, trip.color, trip.flights).subscribe(result => {
        if(result['success'] == 'true'){
          this.router.navigate(['']);
        } else{
          console.log('Modifying trip failed'); //TODO: deal with this case
        }
        this.showSpinner = false;
      })
    }
  }
}
