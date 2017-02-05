import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from '@angular/router';
import { CourseService } from './course.service';

import 'rxjs/add/operator/switchMap';

@Component({
  moduleId: module.id,
  templateUrl: 'course.component.html'
})
export class CourseComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private courseService: CourseService
  ) { }
  
  ngOnInit(): void {
    this.getCourse();
  }
  
  getCourse(): void {
    this.route.params.switchMap((params: Params) => {
      var courseString = params['courseString'];
      var arr = courseString.match(/^([a-zA-Z]+)([0-9]+)$/);
      var subject = arr[1];
      var catalogNumber = arr[2];
      return this.courseService.get(subject, catalogNumber);
    }).subscribe(console.log);
  }
}
