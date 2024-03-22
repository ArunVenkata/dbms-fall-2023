import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LayoutComponent } from './layout/layout.component';
import { AuthGuard } from './auth.guard';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { HomeComponent } from './home/home.component';
import { AnalyticsComponent } from './analytics/analytics.component';

const routes: Routes = [
  {
    path:"",
    component: LayoutComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path:"",
        component: HomeComponent
      },
      {
        path: "analytics",
        component: AnalyticsComponent
      }
    ]
  },
  {
    path: "login",
    component: LoginComponent
  },
  {
    path: "login/:userType",
    component: LoginComponent
  },
  {
    path: "signup",
    component: SignupComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
