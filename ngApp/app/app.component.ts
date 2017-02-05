import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { SearchService } from './search.service';

@Component({
    moduleId: module.id,
    selector: 'my-app',
    templateUrl: 'app.component.html'
})
export class AppComponent {
  searchString: string;
  
  constructor(
    private router: Router,
    private searchService: SearchService
  ) {}
  
  search(courseString: string): void {
    var arr = courseString.split(/\s+/);
    this.searchService.search(arr[0], Number(arr[1]))
      .then(console.log);
  }
  
  onSubmit(): void {
    this.search(this.searchString);
  }
}
