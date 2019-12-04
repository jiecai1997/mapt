import { Component, OnInit } from '@angular/core';
import { LoginService } from '@app/services/login.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {
  loggedIn: boolean = true;

  constructor(private route: ActivatedRoute, private router: Router, private loginService: LoginService) { }

  ngOnInit() {
    // set uid based on url
    const uid = this.route.snapshot.paramMap.get('id');
    this.loginService.setUID(parseInt(uid));
    console.log('uid', uid);

    // determine if user is logged in
    // this.loginService.verifyLoggedIn().subscribe(result => {
    //   if(result['loggedin'])
    // });
  }

  logout(): void {
    this.loginService.setSessionToken('SESSIONTOKEN');
    this.loginService.setUID(0);
    this.router.navigate([''])
  }
}
