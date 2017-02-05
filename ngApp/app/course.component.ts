import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from '@angular/router';

import { CourseService } from './course.service';
import { CourseParamService } from './course-param.service';

import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';

@Component({
  moduleId: module.id,
  templateUrl: 'course.component.html'
})
export class CourseComponent implements OnInit {
  data: any;
  latestBooks: any;
  
  constructor(
    private courseParamService: CourseParamService,
    private route: ActivatedRoute,
    private courseService: CourseService
  ) { }
  
  ngOnInit(): void {
    var obs = this.route.params.map((params: Params) => {
      if (!params['courseString']) return null;
      var courseString = params['courseString'];
      var arr = courseString.match(/^([a-zA-Z]+)([0-9]+)$/);
      var subject = arr[1].toUpperCase();
      var catalogNumber = arr[2];
      return {
        subject: subject,
        catalogNumber: catalogNumber,
        string: subject + ' ' + catalogNumber
      };
    });
    
    obs.subscribe((data: any) => {
      this.data = data;
      this.courseParamService.updateCourseData(data);
    });
    
    obs.switchMap((data: any) => {
      return this.courseService.get(data.subject, data.catalogNumber);
    }).subscribe((res: any) => {
      this.latestBooks = res.data.latest;
    });
  }
}
