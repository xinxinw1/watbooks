import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { CourseParamService } from './course-param.service';
import { AuthService } from './auth.service';

import 'rxjs/add/operator/switchMap';

@Component({
    moduleId: module.id,
    selector: 'my-app',
    templateUrl: 'app.component.html'
})
export class AppComponent implements OnInit {
  searchString: string;
  
  constructor(
    private courseParamService: CourseParamService,
    private router: Router
  ) {}
  
  ngOnInit(): void {
    this.courseParamService.courseData$.subscribe((data: any) => {
      if (data) this.searchString = data.string;
    });
  }
  
  onSubmit(): void {
    var filtered = this.searchString.replace(/\s+/, '')
    if (filtered.match(/^[a-zA-Z]+[0-9]+$/)){
      this.router.navigate(['/course', filtered.toLowerCase()]);
    }
  }
}
