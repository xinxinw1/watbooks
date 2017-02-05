import { Component, OnInit } from "@angular/core";
import { Router, ActivatedRoute, Params } from '@angular/router';

import { AuthService } from './auth.service';

import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';

@Component({
  moduleId: module.id,
  templateUrl: 'login.component.html'
})
export class LoginComponent implements OnInit {
  
  loginData: any
  signupData: any;
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) { }
  
  ngOnInit(): void {
    this.loginData = {};
    this.signupData = {};
  }
  
  onLoginSubmit() {
    this.authService.login(this.loginData)
      .then(_ => {
          this.router.navigate(['/']);
      });
  }
  
  onSignupSubmit() {
    this.authService.signup(this.signupData)
      .then(_ => {
          this.router.navigate(['/']);
      });
  }
  
  
}
