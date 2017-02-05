import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class CourseService {
  
  constructor(private http: Http) { }

  /*search(subject: string, catalogNumber: number): Promise<any> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('subject', subject.toUpperCase());
    params.set('catalog_number', String(catalogNumber));

    return this.http.get('/api/search', {
        search: params
      })
      .toPromise()
      .then(response => response.json().data)
      .catch(this.handleError);
  }*/
  
  get(subject: string, catalogNumber: number): Promise<any> {
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
            }
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
  }
  
  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
