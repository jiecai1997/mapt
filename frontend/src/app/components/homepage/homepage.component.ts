import { Component, OnInit } from '@angular/core';
import { LoginService } from '@app/services/login.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {
  showTabs: boolean = true; // TODO: calculate this value

  constructor(private router: Router, private loginService: LoginService) { }

  ngOnInit() {
  }

  logout(): void {
    this.loginService.setSessionToken('');
    this.loginService.setUID(0);
    this.router.navigate([''])
  }
}
