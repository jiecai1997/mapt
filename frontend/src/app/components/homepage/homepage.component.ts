import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {
  showTabs: boolean = true; // TODO: calculate this value

  constructor(private router: Router) { }

  ngOnInit() {
  }

  logout(): void {
    this.router.navigate([''])
  }
}
