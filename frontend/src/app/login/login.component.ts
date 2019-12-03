import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from '@app/services/login.service';


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

  constructor(private router: Router, private loginService: LoginService) { }

  ngOnInit() {
  }

  submitNewUser() : void {
    if(this.isCreateAccount){
      this.loginService.newUser(this.username, this.email, this.password).subscribe(result => {
        if(result['success'] == 'true'){
          // account created succesfully so log them in
          this.submitLogin();
        } else{
          console.log('UNSUCCESSFUL'); //TODO: deal with this case
        }
      });
    }
  }
  
  submitLogin(): void {
    this.loginService.attemptLogin(this.email, this.password).subscribe(result => {
      if(result['success'] == 'true'){
        this.loginService.setUID(result['userid']);
        this.loginService.setSessionToken(result['sessionToken']);
        this.router.navigate([result['username']]);
      } else{
        console.log('UNSUCCESSFUL'); //TODO: deal with this case
      }
    });
  }

  has_errors(): boolean {
    return this.passwordFormControl.hasError('required') || 
      this.passwordFormControl.hasError('minlength') || 
      this.emailFormControl.hasError('required') || 
      this.emailFormControl.hasError('email') || 
      (this.isCreateAccount && this.usernameFormControl.hasError('required'));
  }
}
