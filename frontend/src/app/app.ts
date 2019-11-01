import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None //needed to hide controlling tabs
})

export class AppComponent {
  selectedTab: number = 2;
}

// eventually gonna want to use routing to switch views between components - see https://angular.io/tutorial/toh-pt5 