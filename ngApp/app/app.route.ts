import { RouterModule, Routes } from '@angular/router';
import { ModuleWithProviders } from '@angular/core';

import { HomeComponent } from "./home.component";

const routes: Routes = [
  {path: '', component: HomeComponent},
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes, {useHash: true});