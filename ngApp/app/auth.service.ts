import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class AuthService {
  token: any;
  
  constructor(private http: Http) {
    var token;
    try {
      token = JSON.parse(localStorage.getItem('token'));
    } catch (e) {
      console.log(e);
      this.logout();
    }
    if (token) this.token = token;
  }
  
  login(loginData: any): Promise<any> {
    return this.http.post('/api/v1/login/', JSON.stringify(loginData))
      .toPromise()
      .then(response => {
        this.setToken(response.json().data.token);
        return true;
      })
      .catch(this.handleError);
  }
  
  signup(signupData: any): Promise<any> {
    return this.http.post('/api/v1/register/', JSON.stringify(signupData))
      .toPromise()
      .then(response => {
        this.setToken(response.json().data.token);
        return true;
      })
      .catch(this.handleError);
  }
  
  setToken(token: any) {
    this.token = token;
    localStorage.setItem('token', JSON.stringify(token));
  }
  
  loggedIn(): boolean {
    return !!this.token;
  }
  
  logout(): void {
    this.setToken(false);
  }
  
  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.json());
  }
}
