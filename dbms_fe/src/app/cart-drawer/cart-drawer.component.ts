import { Component, OnDestroy, OnInit } from '@angular/core';
import { CartService } from './cart.service';
import { BehaviorSubject, Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-cart-drawer',
  templateUrl: './cart-drawer.component.html',
  styleUrls: ['./cart-drawer.component.scss'],
})
export class CartDrawerComponent implements OnInit, OnDestroy {
  isDrawerOpen: boolean = false;
  private ngUnsubscribe$: Subject<boolean> = new Subject();
  cart: {[key:string]: any} ={}; 
  constructor(private cartService: CartService) {
  }
  ngOnInit(): void {
    this.cartService.getCartDrawerObservable().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((openState: boolean) => {
      this.cart = this.cartService.getCart();
      this.isDrawerOpen = openState;
    });
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



}
