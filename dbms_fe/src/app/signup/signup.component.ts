import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, NonNullableFormBuilder, ValidatorFn, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Subject, takeUntil } from 'rxjs';
import { performRequest } from '../utils';
import { NzNotificationService } from 'ng-zorro-antd/notification';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {

  private ngUnsubscribe$: Subject<boolean> = new Subject();
  componentState: any = {};
  homeCustomerForm: FormGroup<{
    name: FormControl<string>;
    email: FormControl<string>;
    password: FormControl<string>;
    checkPassword: FormControl<string>;
    marital_status: FormControl<string>;
    gender: FormControl<string>;
    age: FormControl<number>;
    street: FormControl<string>;
    city: FormControl<string>;
    state: FormControl<string>;
    zipcode: FormControl<string>;
    income: FormControl<number>
  }>;
  businessCustomerForm: FormGroup<{
    name: FormControl<string>;
    email: FormControl<string>;
    password: FormControl<string>;
    checkPassword: FormControl<string>;
    street: FormControl<string>;
    city: FormControl<string>;
    state: FormControl<string>;
    zipcode: FormControl<string>;
    business_category: FormControl<string>;
    gross_annual_income: FormControl<number>;
  }>;
  salesPersonForm: FormGroup<{
    name: FormControl<string>;
    email: FormControl<string>;
    password: FormControl<string>;
    checkPassword: FormControl<string>;
    job_title: FormControl<string>;
    income: FormControl<number>;
  }>;

  constructor(private fb: NonNullableFormBuilder,private nzNotificationService: NzNotificationService, private activatedRoute: ActivatedRoute, private authService: AuthService, private router: Router) {
    this.homeCustomerForm = this.fb.group({
      name: ['', [Validators.required]],
      email: ['', [Validators.email, Validators.required]],
      password: ['', [Validators.required]],
      checkPassword: ['', [Validators.required]],
      marital_status: ['', [Validators.required]],
      street: ['', [Validators.required]],
      zipcode: ['', [Validators.required]],
      city: ['', [Validators.required]],
      state: ['', [Validators.required]],
      gender: ['', [Validators.required]],
      age: [18, [Validators.required]],
      income: [0, [Validators.required]]
    });
    this.businessCustomerForm = this.fb.group({
      name: ['', [Validators.required]],
      email: ['', [Validators.email, Validators.required]],
      password: ['', [Validators.required]],
      checkPassword: ['', [Validators.required]],
      street: ['', [Validators.required]],
      city: ['', [Validators.required]],
      state: ['', [Validators.required]],
      zipcode: ['', [Validators.required]],
      business_category: ['', [Validators.required]],
      gross_annual_income: [0, [Validators.required]],
    });
    this.salesPersonForm = this.fb.group({
      name: ['', [Validators.required]],
      email: ['', [Validators.email, Validators.required]],
      password: ['', [Validators.required]],
      checkPassword: ['', [Validators.required]],
      job_title: ['', [Validators.required]],
      income: [0, [Validators.required]],
    });
  }


  ngOnInit() {
  }

  updateConfirmValidator(form: any): void {
    /** wait for refresh value */
    Promise.resolve().then(() => form.controls.checkPassword.updateValueAndValidity());
  }
  async submitHomeCustomerForm() {
    if (!this.homeCustomerForm.valid) {
      Object.values(this.homeCustomerForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
      return;
    }
    const { name, email, password, marital_status, street, city, state, zipcode,gender, age, income} = this.homeCustomerForm.value;
    console.log('submit', this.homeCustomerForm.value);
    let first_name: any = (name || "").split(" ");
    let last_name = first_name[1] || "";
    first_name = first_name[0] || "";
    let resp = await performRequest(this.authService.signUpUser({ first_name, last_name, email, gender, password,age, income, marital_status, address : {street, city, state, zip_code:zipcode}, user_type: "home"}).pipe(takeUntil(this.ngUnsubscribe$)));
    console.log(resp, "RESP ");
    if(!resp?.success){
      this.nzNotificationService.error("An Error Occurred", resp.message);
      return;
    }
    this.nzNotificationService.success("Account Created Successfully!", "You will be taken to the login page in few seconds");
    setTimeout(()=> {
      this.router.navigate(['/login/home']);
    }, 4_000);
  }
  async submitBusinessCustomerForm() {
    if (!this.businessCustomerForm.valid) {
      Object.values(this.businessCustomerForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
      return;
    }
    const { name, email, password, gross_annual_income, business_category, street, city, state, zipcode,} = this.businessCustomerForm.value;
    console.log('submit BUSINESSS', this.businessCustomerForm.value);


    let first_name: any = (name || "").split(" ");
    let last_name = first_name[1] || "";
    first_name = first_name[0] || "";
    let resp = await performRequest(this.authService.signUpUser({ first_name, last_name, email,business_category, password, address : {street, city, state, zip_code:zipcode}, gross_annual_income, user_type: "business"}).pipe(takeUntil(this.ngUnsubscribe$)));
    console.log(resp, "RESP ");
    if(!resp?.success){
      this.nzNotificationService.error("An Error Occurred", resp.message);
      return;
    }
    this.nzNotificationService.success("Account Created Successfully!", "You will be taken to the login page in few seconds");
    setTimeout(()=> {
      this.router.navigate(['/login']);
    }, 4_000);
  }
  async submitSalesPersonForm() {
    if (!this.salesPersonForm.valid) {
      Object.values(this.salesPersonForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
      return;
    }
    const { name, email, password, job_title, income } = this.salesPersonForm.value;
    console.log('submit Sales', this.salesPersonForm.value);

    let first_name: any = (name || "").split(" ");
    let last_name = first_name[1] || "";
    first_name = first_name[0] || "";
    let resp = await performRequest(this.authService.signUpUser({ first_name, last_name, email, password, job_title, income, user_type: "salesperson"}).pipe(takeUntil(this.ngUnsubscribe$)));
    console.log(resp, "RESP ")

    if(!resp?.success){
      this.nzNotificationService.error("An Error Occurred", resp.message);
      return;
    }
    this.nzNotificationService.success("Account Created Successfully!", "You will be taken to the login page in few seconds");
    setTimeout(()=> {
      this.router.navigate(['/login']);
    }, 4_000);
  }
}
