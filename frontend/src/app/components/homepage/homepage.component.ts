import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { LoginService } from '@app/services/login.service';
import { FlightsService } from '@app/services/flights.service';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {
  loggedIn: boolean = false;

  constructor(private route: ActivatedRoute, private router: Router, private loginService: LoginService, private flightService: FlightsService) { }

  ngOnInit() {
    // set uid based on url
    const uid: number = parseInt(this.route.snapshot.paramMap.get('id'));
    console.log('uid', uid);

    if(isNaN(uid)){
      this.router.navigate(['']);
    }else{
      this.loginService.setUID(uid);

      // determine if user is logged in
      this.flightService.verifyLogin().subscribe(result => {
        this.loggedIn = result['loggedIn'] == 'true';
      });
    }
  }

  logout(): void {
    this.loginService.setSessionToken('SESSIONTOKEN');
    this.loginService.setUID(0);
    this.router.navigate([''])
  }
}
