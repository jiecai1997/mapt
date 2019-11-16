import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';

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

  constructor(private router: Router) { }

  ngOnInit() {
    this.origUsername = 'helloworld';
    this.isPublic = false;
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
