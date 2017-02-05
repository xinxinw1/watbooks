import { RouterModule, Routes } from '@angular/router';
import { ModuleWithProviders } from '@angular/core';

import { HomeComponent } from "./home.component";
import { CourseComponent } from "./course.component";

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'course/:courseString', component: CourseComponent}
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes, {useHash: true});