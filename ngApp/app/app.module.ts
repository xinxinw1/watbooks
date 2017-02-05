import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule }    from '@angular/http';

import { AppComponent }  from './app.component';
import { HomeComponent } from './home.component';
import { CourseComponent } from './course.component';
import { LoginComponent } from "./login.component";

import { CourseService } from './course.service';
import { CourseParamService } from './course-param.service';
import { AuthService } from './auth.service';

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
    CourseComponent,
    LoginComponent
  ],
  providers: [
    CourseService,
    CourseParamService,
    AuthService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }

