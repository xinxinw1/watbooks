import { Injectable } from '@angular/core';
import { Headers, RequestOptions, Http, URLSearchParams } from '@angular/http';

import { AuthService } from './auth.service';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class CourseService {
  
  constructor(
    private http: Http,
    private authService: AuthService
  ) { }

  get(subject: string, catalogNumber: number): Promise<any> {
    let headers = new Headers({ 'Authorization': 'Token ' + this.authService.token });
    let options = new RequestOptions({ headers: headers });
    return this.http.get('/api/v1/course/' + subject + '/' + catalogNumber + '/', options)
      .toPromise()
      .then(response => response.json())
      .catch(this.handleError);
  }
  
  /*get(subject: string, catalogNumber: number): Promise<any> {
    return Promise.resolve({
      "meta": {},
      "data": {
        "latest": [
          {
            "title": "LINEAR CIRCUITS (1ST CUSTOM ED FOR ECE 140/240)",
            "author": "An Author",
            "sku": "235343875924",
            "new_price": "$80.00",
            "used_price": "$20.00",
            "usefulness": {
              "up": 5,
              "down": 3
            },
            "user_rating": "up"
          },
          {
            "title": "A Random book",
            "author": "An Author",
            "sku": "235343875924",
            "new_price": "$80.00",
            "used_price": "$20.00",
            "usefulness": {
              "up": 1,
              "down": 3
            }
          }
        ]
      }
    });
  }*/
  
  rate(sku: string, subject: string, catalogNumber: number, isUseful: string): Promise<any> {
    let headers = new Headers({ 'Authorization': 'Token ' + this.authService.token });
    let options = new RequestOptions({ headers: headers });
    return this.http.post('/api/v1/rate/', JSON.stringify({
        sku: sku,
        subject: subject,
        catalog_number: catalogNumber,
        user_rating: isUseful
      }), options)
      .toPromise()
      .then(response => {
        console.log(response);
        return true;
      })
      .catch(this.handleError);
  }
  
  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
