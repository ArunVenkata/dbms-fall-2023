import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Subject, takeUntil } from 'rxjs';
import { performRequest } from '../utils';
import { RegionService } from '../services/region.service';
import { Cart, CartService } from '../cart-drawer/cart.service';
import { NzModalService } from 'ng-zorro-antd/modal';
import { StoreService } from '../services/store.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit, OnDestroy {
  private ngUnsubscribe$: Subject<boolean> = new Subject();
  isLoggedIn: boolean = false;  

  constructor(private authService: AuthService, private storeService: StoreService, private nzModalService: NzModalService ,private cartService: CartService, private regionService: RegionService){
    this.isLoggedIn = authService.isUserLoggedIn();
  }
  userInfo: any = {};
  regionsData: any = [];
  cart: Cart ={};
  totalCartQty: number = 0;
  currentRegion!: any;
  ngOnDestroy(): void {
    this.ngUnsubscribe$.next(true);
    this.ngUnsubscribe$.complete();
  }

  async ngOnInit(){
    this.cart = this.cartService.getCart();
    this.totalCartQty = this.cartService.getTotalItemQuantity();
    if(this.isLoggedIn){
      this.userInfo = await performRequest(this.authService.getUserDetails().pipe(takeUntil(this.ngUnsubscribe$)), {defaultValue: 0});
      this.regionsData = await performRequest(this.regionService.getRegions().pipe(takeUntil(this.ngUnsubscribe$)), {defaultValue: []})      
      this.cartService.cartChangesEvent().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((cart) =>{
          this.cart = cart;
          this.totalCartQty = this.cartService.getTotalItemQuantity();
      })
    }
    
  }
  
  async changeRegion(region: any){
    // if(!this.cartService.isCartEmpty()){
    //   this.nzModalService.confirm({
    //     nzTitle: '<i>Delete Cart Items?</i>',
    //     nzContent: '<br>You are trying to change region. Adding products from multiple regions is not allowed>',
    //     nzOnOk: () => console.log('OK')
    //   });
    // }
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
  openTransactionHistory(){
    this.storeService.triggerTransactionHistoryModal();
  }
}
