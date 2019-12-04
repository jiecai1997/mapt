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

  error: string = '';
  showSpinner: boolean = false;

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
    this.showSpinner = true;

    if(this.isCreateAccount){
      this.loginService.newUser(this.username, this.email, this.password).subscribe(
        result => {
          if(result['success'] == 'true'){
            // account created succesfully so log them in
            this.submitLogin();
          } else{
            console.log('account creation unsuccessful'); //TODO: deal with this case
            this.error = 'username already taken';
            this.username = undefined;
          }
          this.showSpinner = false;
        }, error => {
          this.error = 'account creation failed - please try again';
          this.showSpinner = false;
        });
    }
  }
  
  submitLogin(): void {
    this.showSpinner = true;

    this.loginService.attemptLogin(this.email, this.password).subscribe(result => {
      if(result['success'] == 'true'){
        this.loginService.setSessionToken(result['sessionToken']);

        console.log('got here');
        console.log('result', result);
        this.router.navigate([result['userid']]);
      } else{
        console.log('UNSUCCESSFUL'); //TODO: deal with this case
        this.error = 'username or password is incorrect';
        this.email = this.username = this.password = undefined;
      }
      this.showSpinner = false;
    }, error => {
      this.error = 'login failed - please try again';
      this.showSpinner = false;
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
