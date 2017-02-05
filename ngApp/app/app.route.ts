import { RouterModule, Routes } from '@angular/router';
import { ModuleWithProviders } from '@angular/core';

import { HomeComponent } from "./home.component";
import { CourseComponent } from "./course.component";
import { LoginComponent } from "./login.component";

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'course/:courseString', component: CourseComponent},
  {path: 'login', component: LoginComponent},
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes, {useHash: true});