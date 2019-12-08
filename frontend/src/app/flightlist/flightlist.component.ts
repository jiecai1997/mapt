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
  airlines = [];
  colors = [{name: 'AliceBlue', grayscale: 0.971}, {name: 'AntiqueWhite', grayscale: 0.915}, {name: 'Aqua', grayscale: 0.666}, {name: 'Aquamarine', grayscale: 0.776}, {name: 'Azure', grayscale: 0.980}, {name: 'Beige', grayscale: 0.928}, {name: 'Bisque', grayscale: 0.887}, {name: 'Black', grayscale: 0.0}, {name: 'BlanchedAlmond', grayscale: 0.908}, {name: 'Blue', grayscale: 0.333}, {name: 'BlueViolet', grayscale: 0.532}, {name: 'Brown', grayscale: 0.325}, {name: 'BurlyWood', grayscale: 0.707}, {name: 'CadetBlue', grayscale: 0.539}, {name: 'Chartreuse', grayscale: 0.499}, {name: 'Chocolate', grayscale: 0.4509}, {name: 'Coral', grayscale: 0.603}, {name: 'CornflowerBlue', grayscale: 0.635}, {name: 'Cornsilk', grayscale: 0.945}, {name: 'Crimson', grayscale: 0.3921}, {name: 'Cyan', grayscale: 0.666}, {name: 'DarkBlue', grayscale: 0.1816}, {name: 'DarkCyan', grayscale: 0.3633}, {name: 'DarkGoldenRod', grayscale: 0.430}, {name: 'DarkGray', grayscale: 0.662}, {name: 'DarkGrey', grayscale: 0.662}, {name: 'DarkGreen', grayscale: 0.1307}, {name: 'DarkKhaki', grayscale: 0.626}, {name: 'DarkMagenta', grayscale: 0.3633}, {name: 'DarkOliveGreen', grayscale: 0.3124}, {name: 'DarkOrange', grayscale: 0.516}, {name: 'DarkOrchid', grayscale: 0.532}, {name: 'DarkRed', grayscale: 0.1816}, {name: 'DarkSalmon', grayscale: 0.660}, {name: 'DarkSeaGreen', grayscale: 0.619}, {name: 'DarkSlateBlue', grayscale: 0.3555}, {name: 'DarkSlateGray', grayscale: 0.267}, {name: 'DarkSlateGrey', grayscale: 0.267}, {name: 'DarkTurquoise', grayscale: 0.54}, {name: 'DarkViolet', grayscale: 0.46}, {name: 'DeepPink', grayscale: 0.551}, {name: 'DeepSkyBlue', grayscale: 0.583}, {name: 'DimGray', grayscale: 0.411}, {name: 'DimGrey', grayscale: 0.411}, {name: 'DodgerBlue', grayscale: 0.560}, {name: 'FireBrick', grayscale: 0.321},   {name: 'FloralWhite', grayscale: 0.973}, {name: 'ForestGreen', grayscale: 0.2705}, {name: 'Fuchsia', grayscale: 0.666}, {name: 'Gainsboro', grayscale: 0.862}, {name: 'GhostWhite', grayscale: 0.981}, {name: 'Gold', grayscale: 0.614}, {name: 'GoldenRod', grayscale: 0.54}, {name: 'Gray', grayscale: 0.501}, {name: 'Grey', grayscale: 0.501}, {name: 'Green', grayscale: 0.1673}, {name: 'GreenYellow', grayscale: 0.620}, {name: 'HoneyDew', grayscale: 0.960}, {name: 'HotPink', grayscale: 0.705}, {name: 'IndianRed', grayscale: 0.508}, {name: 'Indigo', grayscale: 0.267}, {name: 'Ivory', grayscale: 0.980}, {name: 'Khaki', grayscale: 0.797}, {name: 'Lavender', grayscale: 0.928}, {name: 'LavenderBlush', grayscale: 0.967}, {name: 'LawnGreen', grayscale: 0.491}, {name: 'LemonChiffon', grayscale: 0.928}, {name: 'LightBlue', grayscale: 0.809}, {name: 'LightCoral', grayscale: 0.648}, {name: 'LightCyan', grayscale: 0.959}, {name: 'LightGoldenRodYellow', grayscale: 0.928}, {name: 'LightGray', grayscale: 0.827}, {name: 'LightGrey', grayscale: 0.827}, {name: 'LightGreen', grayscale: 0.687}, {name: 'LightPink', grayscale: 0.823}, {name: 'LightSalmon', grayscale: 0.701}, {name: 'LightSeaGreen', grayscale: 0.4967}, {name: 'LightSkyBlue', grayscale: 0.772}, {name: 'LightSlateGray', grayscale: 0.533}, {name: 'LightSlateGrey', grayscale: 0.533}, {name: 'LightSteelBlue', grayscale: 0.776}, {name: 'LightYellow', grayscale: 0.959}, {name: 'Lime', grayscale: 0.333}, {name: 'LimeGreen', grayscale: 0.3986}, {name: 'Linen', grayscale: 0.941}, {name: 'Magenta', grayscale: 0.666}, {name: 'Maroon', grayscale: 0.1673}, {name: 'MediumAquaMarine', grayscale: 0.623}, {name: 'MediumBlue', grayscale: 0.267}, {name: 'MediumOrchid', grayscale: 0.630}, {name: 'MediumPurple', grayscale: 0.624}, {name: 'MediumSeaGreen', grayscale: 0.4601}, {name: 'MediumSlateBlue', grayscale: 0.607}, {name: 'MediumTurquoise', grayscale: 0.633}, {name: 'MediumVioletRed', grayscale: 0.4614}, {name: 'MidnightBlue', grayscale: 0.2117}, {name: 'MintCream', grayscale: 0.980}, {name: 'MistyRose', grayscale: 0.925}, {name: 'Moccasin', grayscale: 0.867}, {name: 'NavajoWhite', grayscale: 0.849}, {name: 'Navy', grayscale: 0.1673}, {name: 'OldLace', grayscale: 0.951}, {name: 'Olive', grayscale: 0.3346}, {name: 'OliveDrab', grayscale: 0.371}, {name: 'Orange', grayscale: 0.549}, {name: 'OrangeRed', grayscale: 0.423}, {name: 'Orchid', grayscale: 0.711}, {name: 'PaleGoldenRod', grayscale: 0.836}, {name: 'PaleGreen', grayscale: 0.725}, {name: 'PaleTurquoise', grayscale: 0.850}, {name: 'PaleVioletRed', grayscale: 0.624}, {name: 'PapayaWhip', grayscale: 0.924}, {name: 'PeachPuff', grayscale: 0.860}, {name: 'Peru', grayscale: 0.524}, {name: 'Pink', grayscale: 0.849}, {name: 'Plum', grayscale: 0.786}, {name: 'PowderBlue', grayscale: 0.823}, {name: 'Purple', grayscale: 0.3346}, {name: 'RebeccaPurple', grayscale: 0.4}, {name: 'Red', grayscale: 0.333}, {name: 'RosyBrown', grayscale: 0.619}, {name: 'RoyalBlue', grayscale: 0.516}, {name: 'SaddleBrown', grayscale: 0.2967}, {name: 'Salmon', grayscale: 0.643}, {name: 'SandyBrown', grayscale: 0.658}, {name: 'SeaGreen', grayscale: 0.3555}, {name: 'SeaShell', grayscale: 0.964}, {name: 'Sienna', grayscale: 0.3751}, {name: 'Silver', grayscale: 0.752}, {name: 'SkyBlue', grayscale: 0.752}, {name: 'SlateBlue', grayscale: 0.524}, {name: 'SlateGray', grayscale: 0.501}, {name: 'SlateGrey', grayscale: 0.501}, {name: 'Snow', grayscale: 0.986}, {name: 'SpringGreen', grayscale: 0.499}, {name: 'SteelBlue', grayscale: 0.4967}, {name: 'Tan', grayscale: 0.692}, {name: 'Teal', grayscale: 0.3346}, {name: 'Thistle', grayscale: 0.814}, {name: 'Tomato', grayscale: 0.555}, {name: 'Turquoise', grayscale: 0.648}, {name: 'Violet', grayscale: 0.79}, {name: 'Wheat', grayscale: 0.844}, {name: 'White', grayscale: 1.0}, {name: 'WhiteSmoke', grayscale: 0.960}, {name: 'Yellow', grayscale: 0.666}, {name: 'YellowGreen', grayscale: 0.53}];
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
      this.trips = [{tripName: '', color: '', flights: []}]
      this.addFlight(0); // start with one flight
    }else{
      // get trip data
      this.flightsService.getTrips().subscribe(
        tripsObj => {
            this.trips = tripsObj['trips'];
            // MAKING ARRIVAL AND DEPARTURE INFO MATERIAL-FRIENDLY
            this.trips.forEach(x => {
              let flights = x['flights'];
              flights.forEach(flight => {

                let originalArrDate = flight['arrival_date'];
                let originalArrYear = originalArrDate.substring(0,4);
                let originalArrMonth = originalArrDate.substring(4,6);
                let originalArrDay = originalArrDate.substring(6,8);

                flight['arrival_date'] = new Date(originalArrYear, originalArrMonth, originalArrDay)

                let originalDeptDate = flight['depart_date'];
                let originalDeptYear = originalDeptDate.substring(0,4);
                let originalDeptMonth = originalDeptDate.substring(4,6);
                let originalDeptDay = originalDeptDate.substring(6,8);

                flight['depart_date'] = new Date(originalDeptYear, originalDeptMonth, originalDeptDay)

              })
            })

            console.log('trips are', this.trips)
          });
    }
  }

  addFlight(tripIndex: number): void{
    this.trips[tripIndex].flights.push({dep: {}, arr: {}});
    this.lastAddedTo = tripIndex;
  }

  getColorSuggestions(s: string): any[] {
    s = s.toLowerCase();
    return this.colors.filter(color => color.name.toLowerCase().startsWith(s));
  }

  getAirportSuggestions(flight: any, isDep: boolean): any {
    const depAirport = (flight['depart_airport'] || '').toLowerCase(),
          arrAirport = (flight['arrival_airport'] || '').toLowerCase();

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
    console.log('addtrip', this.isAddTrip)

    if(this.isAddTrip){
      // add trip
      this.flightsService.addTrip(trip.tripName, trip.color, trip.flights).subscribe(result => {

        if(result['success'] == 'true'){
          const uid = this.loginService.getUID().toString();
          this.router.navigateByUrl('').then(() => {
            this.router.navigate([uid]);
          });

          } else{
          console.log(result['error']); //TODO: deal with this case
        }
        this.showSpinner = false;
      })
    }else{
      console.log('got here')
      this.flightsService.updateTrip(trip.tripid, trip.tripName, trip.color, trip.flights).subscribe(result => {
        if(result['success'] == 'true'){
          const uid = this.loginService.getUID().toString();
          this.router.navigateByUrl('').then(() => {
            this.router.navigate([uid]);
          });
        } else{
          console.log('Modifying trip failed'); //TODO: deal with this case
        }
        this.showSpinner = false;
      })
    }
  }

  hasErrors(trip: any): boolean{
    // console.log(trip);
    var hasFlightError = false;
    trip.flights.forEach(flight => {
      hasFlightError = hasFlightError || 
        flight['departAirport'] == undefined || flight['departAirport'] == null ||
        flight['arrivalAirport'] == undefined || flight['arrivalAirport'] == null ||
        flight['depart_date'] == undefined || flight['depart_date'] == null ||
        flight['arrival_date'] == undefined || flight['arrival_date'] == null ||
        flight['depart_time'] == undefined || flight['depart_time'] == null || 
        flight['arrival_time'] == undefined || flight['arrival_time'] == null
    });

    return hasFlightError || trip.tripName == '' || trip.color == '';
  }
}
