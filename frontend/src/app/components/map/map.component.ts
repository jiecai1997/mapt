import { Component, OnInit } from '@angular/core';
import { FlightsService } from '@app/services/flights.service';
import { Flight } from '@app/models/Flight';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']

})
export class MapComponent implements OnInit {

  constructor(private flightsService:FlightsService) { }

  ngOnInit() {
    this.getFlights();

  }

  // on init, set lat/long to user's current location?

  lat:number = 32.2226;
  lng:number = -110.9747;

  flights:Flight[]

  getFlights(): void{
      this.flightsService.getFlights().subscribe(
          flights => {
              this.flights = flights;
            });
  }


  options = 
    {
      streetViewControl: "false"
    }
  

  styles = [
    {
      "elementType": "labels.text.stroke",
        "stylers": [{
          "weight": "0.5"
        }]
    },
    {
      "elementType": "labels.icon",
        "stylers": [{
          "visibility":"off"
        }]
    },
    {
    "featureType": "administrative",
        "stylers": [{
          "color": "#bbbbbb"
        }]
    },
    {
      "featureType": "administrative",
      "elementType": "labels.text",
          "stylers": [{
            "visibility": "off"
          }]
    },
    {
      "featureType": "administrative.country",
      "elementType": "labels.text",
          "stylers": [{
            "visibility": "on",
          }]
      },
    {
    "featureType": "administrative.country",
        "stylers": [{
          "color": "#ffffff",
        }]
    },
    {
    "featureType": "administrative.land_parcel",
        "stylers": [{
            "visibility":"off"
        }]
    },
            {
    "featureType": "administrative.locality",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "administrative.neighborhood",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "administrative.province",
        "stylers": [{
            "color":"#777777"
        }]
    },
    {
      "featureType": "administrative.province",
      "elementType": 'labels.text',
          "stylers": [{
              "visibility":"on",
              "color":"#777777"
          }]
    },
    {
    "featureType": "landscape",
        "stylers": [{
            "color": "#ffffff",
            "visibility":"on"
        }]
    },
    {
    "featureType": "landscape.man_made",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "landscape.natural",
        "stylers": [{
            "color":"#bbbbbb"
        }]
    },
            {
    "featureType": "landscape.natural.landcover",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "landscape.natural.terrain",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "poi",
        "stylers": [{
            "visibility":"off"
        }]
    },
            {
    "featureType": "poi.attraction",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "poi.business",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "poi.government",
        "stylers": [{
            "visibility":"off"
        }]
    },
            {
    "featureType": "poi.medical",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "poi.park",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "poi.place_of_worship",
        "stylers": [{
            "visibility":"off"
        }]
    },
            {
    "featureType": "poi.school",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "poi.sports_complex",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
    "featureType": "road",
        "stylers": [{
            "visibility":"off"
        }]
    },
    {
        "featureType": "road",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "road.arterial",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "road.highway",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "road.highway.controlled_access",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "road.local",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "transit",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "transit.line",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "transit.station",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "transit.station.airport",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "transit.station.bus",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "transit.station.rail",
        "stylers": [{
            "visibility":"off"
            }]
    },
    {
        "featureType": "water",
        "stylers": [{
            "color": "#303030"
            }]
    }];
}
