import { Injectable, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Subject }    from 'rxjs/Subject';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';

@Injectable()
export class CourseParamService {
  private courseDataSource = new Subject<any>();
  courseData$ = this.courseDataSource.asObservable();
  
  updateCourseData(data: any): void {
    this.courseDataSource.next(data);
  }
}
