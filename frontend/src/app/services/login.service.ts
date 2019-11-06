import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Md5 } from 'ts-md5/dist/md5';

@Injectable({
  providedIn: 'root'
})

export class LoginService {

  private uid:number;

  private serverURL = 'http://localhost:5000';

  constructor(private http:HttpClient) { }

  newUser(username:string, email:string, password:string){
    // put request to make new user, make a salt-generating function to write to db
    // write to DB salted password - see how to work with request bodies
    
    const hashedSalty:string = this.generatePassword(email, password);

    const reqBody = {'username':username, 'email': email, 'hashedPassword': hashedSalty};

    return this.http.post(this.serverURL + '/user/register', reqBody).subscribe( result => {
      return result;
    });
    
  }

  attemptLogin(email:string, password:string){
    const hashedSalty:string = this.generatePassword(email, password);
    const reqBody = {'email': email, 'hashedPassword': hashedSalty}

    return this.http.post(this.serverURL + '/loginattempt', reqBody).subscribe( result => {
      if(result['success'] == 'true'){
        this.uid = result['uid'];
        return this.uid;
      }
      else{
        return 'UNSUCCESSFUL';
      }

    })
    

  }

  private generatePassword(email:string, password:string):string{
    const md5 = new Md5();
    const salt = md5.appendStr(email).end();
    
    const salty = password + salt;
    const hashed = md5.appendStr(salty);

    return String(hashed);
  }
}


