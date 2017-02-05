import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule }    from '@angular/http';

import { AppComponent }  from './app.component';
import { HomeComponent } from './home.component';
import { CourseComponent } from './course.component';

import { CourseService } from './course.service';
import { CourseParamService } from './course-param.service';

import { routing } from './app.route';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    routing
  ],
  declarations: [
    AppComponent,
    HomeComponent,
    CourseComponent
  ],
  providers: [
    CourseService,
    CourseParamService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }

