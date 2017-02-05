import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    moduleId: module.id,
    selector: 'my-app',
    templateUrl: 'app.component.html'
})
export class AppComponent {
  searchString: string;
  
  constructor(
    private router: Router
  ) {}
  
  onSubmit(): void {
    var filtered = this.searchString.replace(/\s+/, '');
    if (filtered.match(/^[a-zA-Z]+[0-9]+$/)){
      this.router.navigate(['/course', filtered]);
    }
  }
}
