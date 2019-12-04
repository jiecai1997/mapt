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

  showSpinner: boolean = false;

  constructor(private router: Router, private flightsService: FlightsService) { }

  ngOnInit() {
    this.flightsService.getProfileInfo().subscribe(result => {
      if(result['success'] == 'true'){
        this.origUsername = this.username = result['username'];
        this.origIsPublic = this.isPublic = result['isPublic'];
      }
      else{
        console.log('GETTING PROFILE INFO FAILED'); //TODO: deal with this case
      }
    });
  }

  save(): void {
    console.log(this.username, this.isPublic);
    this.showSpinner = true;
    
    this.flightsService.updateProfileInfo(this.username, this.isPublic).subscribe(result => {
      if(result['success'] == 'true'){
        this.router.navigate([this.username]);
      }
      else{
        console.log('FAILED TO UPDATE ACCOUNT INFO'); //TODO: deal with this case
        this.cancel();
      }
      this.showSpinner = false;
    })
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
