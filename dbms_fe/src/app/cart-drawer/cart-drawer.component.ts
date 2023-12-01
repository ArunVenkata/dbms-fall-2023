import { Component, OnDestroy, OnInit } from '@angular/core';
import { Cart, CartService } from './cart.service';
import { BehaviorSubject, Subject, takeUntil } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { performRequest } from '../utils';
import { StoreService } from '../services/store.service';
import { NzNotificationService } from 'ng-zorro-antd/notification';

@Component({
  selector: 'app-cart-drawer',
  templateUrl: './cart-drawer.component.html',
  styleUrls: ['./cart-drawer.component.scss'],
})
export class CartDrawerComponent implements OnInit, OnDestroy {
  isDrawerOpen: boolean = false;
  private ngUnsubscribe$: Subject<boolean> = new Subject();
  cart: Cart ={}; 
  selectedSalesPerson!: any; 
  checkoutLoading: boolean = false;
  Object: any = Object;
  salesPersons: any = []
  componentState:any = {isCheckoutSuccessModalVisible: false}

  constructor(private cartService: CartService, private nzNotificationService: NzNotificationService, private authService: AuthService, private storeService: StoreService) {
  }
  ngOnInit(): void {
    this.cartService.getCartDrawerObservable().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((openState: boolean) => {
      this.cart = this.cartService.getCart();
      this.isDrawerOpen = openState;
      if(this.isDrawerOpen){
        // if cart is not empty load salespersons for store
        this.loadSalesPersons();
      }
    });
    
    this.cartService.cartChangesEvent().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((updatedCart)=>{
      this.cart = updatedCart;
    })
  }

  async loadSalesPersons(){
    if(!Object.keys(this.cart).length){
      return
    }
    const firstProduct = Object.values(this.cart)[0];

    const resp = await performRequest(this.authService.getSalesPersons(firstProduct.storeId).pipe(takeUntil(this.ngUnsubscribe$)));
    console.log(resp, "SALESPERSONS")
    if(Object.keys(resp).length){
      this.selectedSalesPerson = resp[0];
    }
    this.salesPersons = resp;
  }
  ngOnDestroy(): void {
    this.ngUnsubscribe$.next(true);
    this.ngUnsubscribe$.complete();
  }
  
  getItemCost(productId: string){
    const round_places = 2;
    return (Math.round(((this.cart[productId].cost * this.cart[productId].quantity) + Number.EPSILON) * Math.pow(10,round_places)) / Math.pow(10,round_places)).toFixed(2)
  }
  getCartTotal(){
    return this.cartService.getCartTotal().toFixed(2);
  }
  closeDrawer(){
    this.cartService.setCartDrawerClosed();
    console.log(this.cartService.getCart());
  }

  clearCart(){
    this.cartService.clearCart();
  }
  removeItemFromCart(productId: string){
    this.cartService.removeFromCart(productId);
  }

  async checkoutCart(){
    this.checkoutLoading = true;
    const resp = await performRequest(this.storeService.checkoutTransaction({cart: this.cart, 
    ...(this.selectedSalesPerson && {salesperson_id: this.selectedSalesPerson.user.id})
    }).pipe(takeUntil(this.ngUnsubscribe$)))
    console.log(resp)
    if(!resp?.success){
      this.nzNotificationService.info("Cart Items are invalid", "Add them back to your cart again");
      this.cartService.clearCart();
      this.closeDrawer();
      return
    }
    this.showPurchaseSuccessfulModal()
    this.cartService.clearCart();
    this.closeDrawer()
    
    
  }
  showPurchaseSuccessfulModal(){
    this.componentState.isCheckoutSuccessModalVisible = true;
    
  }

}
