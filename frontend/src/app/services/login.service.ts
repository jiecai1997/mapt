import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private serverURL = 'http://localhost:5000';

  constructor(private http:HttpClient) { }

  private newUser(){
    // put request to make new user, make a salt-generating function to write to db
  }

  private attemptLogin():string{
    this.http.get(this.serverURL + '/login/salt/:user').subscribe( salt => {
      // hash password with salt in it ==> 
      // make a post request to see if user and password + salt combo is valid
      // result: {success: true, userid: userid} or {success: false}
    })
    

    return 'Success';
  }
}


