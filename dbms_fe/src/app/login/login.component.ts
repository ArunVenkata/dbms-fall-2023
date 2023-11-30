import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, NonNullableFormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { Subject, lastValueFrom, takeUntil } from 'rxjs';
import { performRequest } from '../utils';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {
  loginForm: FormGroup<{
    email: FormControl<string>;
    password: FormControl<string>;
  }>;
  isLoginBtnLoading: boolean = false;
  isShowLoginForm: boolean = false;
  private ngUnsubscribe$: Subject<boolean> = new Subject();
  componentState: any = {};

  constructor(private fb: NonNullableFormBuilder,private activatedRoute: ActivatedRoute, private authService: AuthService, private router: Router, private nzNotificationService: NzNotificationService) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.email, Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe$.next(true);
    this.ngUnsubscribe$.complete();
  }
  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe((params) => {
      console.log(params);
      if(params.get("userType")){
        this.componentState.currentUserType = params.get("userType");
        this.isShowLoginForm=true;
      }
    })
  }

  submitLoginForm(): void {
    if (!this.loginForm.valid) {
      Object.values(this.loginForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
      return;
    }
    console.log('submit Login', this.loginForm.value);
    this.logInUser({ ...this.loginForm.value })
  }
  async logInUser({ email, password }: { [key: string]: string }) {
    this.isLoginBtnLoading = true;
    const resp = await performRequest(this.authService.loginWithPassword({ email, password }).pipe(takeUntil(this.ngUnsubscribe$)));
    console.log(resp, "IN LOGIN COMP");
    this.isLoginBtnLoading = false;
    if (resp?.error) {
      this.nzNotificationService.error("An Error Occurred", resp.error.errors.non_field_errors[0]);
      return;
    }
    if (resp.success && this.authService.isUserLoggedIn()) {
      this.router.navigate(['/']);
    }
  }
}
