import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class SearchService {
  
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
  
  search(subject: string, catalogNumber: number): Promise<any> {
    return Promise.resolve({
      "meta": {},
      "data": {
        "latest": [
          {
            "title": "LINEAR CIRCUITS (1ST CUSTOM ED FOR ECE 140/240)",
            "author": "An Author",
            "sku": "235343875924",
            "new-price": "$80.00",
            "used-price": "$20.00",
            "usefulness": {
              "up": 5,
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
