import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  isCreateAccount: boolean = false;

  minPassLen: number = 6;

  email: string;
  username: string;
  password: string;

  emailFormControl = new FormControl('', [
    Validators.required,
    Validators.email,
  ]);

  usernameFormControl = new FormControl('', [
    Validators.required
  ]);

  passwordFormControl = new FormControl('', [
    Validators.required,
    Validators.minLength(this.minPassLen),
  ]);

  constructor(private router: Router) { }

  ngOnInit() {
  }

  submit() : void {
    if(this.isCreateAccount){
      console.log(this.email, this.username, this.password);
    }else{
      console.log(this.email, this.password);
    }
  }

  has_errors(): boolean {
    return this.passwordFormControl.hasError('required') || 
      this.passwordFormControl.hasError('minlength') || 
      this.emailFormControl.hasError('required') || 
      this.emailFormControl.hasError('email') || 
      (this.isCreateAccount && this.usernameFormControl.hasError('required'));
  }
}
