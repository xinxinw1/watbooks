import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from '@angular/router';

import { AuthService } from './auth.service';
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
    private authService: AuthService,
    private route: ActivatedRoute,
    private courseService: CourseService
  ) { }
  
  ngOnInit(): void {
    var obs = this.route.params.map((params: Params) => {
      if (!params['courseString']) return null;
      var courseString = params['courseString'];
      var arr = courseString.match(/^([a-zA-Z]+)([0-9]+[a-zA-Z]*)$/);
      var subject = arr[1].toUpperCase();
      var catalogNumber = arr[2].toUpperCase();
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
  
  getExactPercent(book: any) {
    if (!this.hasRatings(book)) return 0;
    return book.usefulness.up / (book.usefulness.up + book.usefulness.down) * 100;
  }
  
  getExactPercentFail(book: any) {
    if (!this.hasRatings(book)) return 0;
    return book.usefulness.down / (book.usefulness.up + book.usefulness.down) * 100;
  }
  
  getPercent(book: any) {
    return Math.round(this.getExactPercent(book));
  }
  
  hasRatings(book: any) {
    return book.usefulness.up + book.usefulness.down > 0;
  }
  
  toggleUp(book: any) {
    if (this.authService.loggedIn()) {
      var changed;
      if (book.user_rating == "up") {
        changed = "none";
        book.usefulness.up--;
      } else if (book.user_rating == "down") {
        changed = "up";
        book.usefulness.up++;
        book.usefulness.down--;
      } else {
        changed = "up";
        book.usefulness.up++;
      }
      book.user_rating = changed;
      return this.courseService.rate(book.sku as string, this.data.subject as string, Number(this.data.catalogNumber), changed)
        .then(console.log);
    } else {
      book.rate_error = "You must be logged in to rate";
    }
  }
  
  toggleDown(book: any) {
    if (this.authService.loggedIn()) {
      var changed;
      if (book.user_rating == "down") {
        changed = "none";
        book.usefulness.down--;
      } else if (book.user_rating == "up") {
        changed = "down";
        book.usefulness.up--;
        book.usefulness.down++;
      } else {
        changed = "down";
        book.usefulness.down++;
      }
      book.user_rating = changed;
      return this.courseService.rate(book.sku as string, this.data.subject as string, Number(this.data.catalogNumber), changed)
        .then(console.log);
    } else {
      book.rate_error = "You must be logged in to rate";
    }
  }
  
}
