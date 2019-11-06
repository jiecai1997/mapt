import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-tripname',
  templateUrl: './tripname.component.html',
  styleUrls: ['./tripname.component.css']
})
export class TripnameComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  submit(): void {
    console.log('submitting');
  }
}
