import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Subject, takeUntil } from 'rxjs';
import { performRequest } from '../utils';
import { RegionService } from '../services/region.service';
import { CartService } from '../cart-drawer/cart.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit, OnDestroy {
  private ngUnsubscribe$: Subject<boolean> = new Subject();
  isLoggedIn: boolean = false;  

  constructor(private authService: AuthService ,private cartService: CartService, private regionService: RegionService){
    this.isLoggedIn = authService.isUserLoggedIn();
  }
  userInfo: any = {};
  regionsData: any = [];
  currentRegion!: any;
  ngOnDestroy(): void {
    this.ngUnsubscribe$.next(true);
    this.ngUnsubscribe$.complete();
  }

  async ngOnInit(){

    if(this.isLoggedIn){
      this.userInfo = await performRequest(this.authService.getUserDetails().pipe(takeUntil(this.ngUnsubscribe$)), {defaultValue: 0});
      this.regionsData = await performRequest(this.regionService.getRegions().pipe(takeUntil(this.ngUnsubscribe$)), {defaultValue: []})      
    }
    
  }
  async changeRegion(region: any){
    console.log(region)
    const resp = await performRequest(this.authService.changeRegion(region).pipe(takeUntil(this.ngUnsubscribe$)));
    console.log(resp, "CHANGE REG RESp");
    this.userInfo = await performRequest(this.authService.getUserDetails().pipe(takeUntil(this.ngUnsubscribe$)), {defaultValue: 0});
    console.log(this.userInfo);
  }
  logOut(){
    this.authService.logOutUser();
    this.isLoggedIn = this.authService.isUserLoggedIn();
  }
  showCartDrawer(){
    this.cartService.setCartDrawerOpen();
  }
}
