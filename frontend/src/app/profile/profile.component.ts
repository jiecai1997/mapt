import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FlightsService } from '@app/services/flights.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})

export class ProfileComponent implements OnInit {
  username: string;
  isPublic: boolean;

  origUsername: string;
  origIsPublic: boolean;

  usernameFormControl = new FormControl('', [
    Validators.required
  ]);

  constructor(private router: Router, private flightsService: FlightsService) { }

  ngOnInit() {
    const profile = this.flightsService.getProfileInfo();
    if(profile != null){
      // this.origUsername = this.username = profile.username;
      // this.origIsPublic = this.isPublic = profile.isPublic;
    }


    this.cancel();
  }

  save(): void {
    console.log(this.username, this.isPublic);
    this.router.navigate([this.username]);
  }

  cancel(): void {
    this.username = this.origUsername;
    this.isPublic = this.origIsPublic;
  }

  has_errors(): boolean {
    return this.usernameFormControl.hasError('required');
  }

  data_changed(): boolean {
    return this.username != this.origUsername || this.isPublic != this.origIsPublic;
  }
}
