import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { StoreService } from '../services/store.service';
import { performRequest } from '../utils';
import { Subject, debounceTime, takeUntil } from 'rxjs';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { Cart, CartService } from '../cart-drawer/cart.service';
import { NzModalService } from 'ng-zorro-antd/modal';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy{

  private ngUnsubscribe$: Subject<boolean> = new Subject()
  
  constructor(public authService: AuthService,private cartService: CartService, private nzNotificationService: NzNotificationService, private storeService: StoreService, private nzModalService: NzModalService){
  }

  private onSearchChange: Subject<string> = new Subject(); 

  componentState: any = {isStoresLoading: false, currentStores:[], transactionHistory: [], isTransactionHistoryModalVisible: false};
  cart: Cart = {};
  userInfo!: any;
  ngOnDestroy(): void {
    this.ngUnsubscribe$.next(true);
    this.ngUnsubscribe$.complete();
  }
  
  async ngOnInit() {
    this.cart = this.cartService.getCart();
    this.cartService.cartChangesEvent().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((newCart) => {
      this.cart = newCart;
      console.log("cart changed", newCart)
    })
    this.userInfo = this.authService.getLoginInfo();
    console.log(this.authService.getLoginInfo(), "LOGIN INFO");
    console.log("CART", this.cartService.getCart())

    this.loadTransactionHistory()
    
    
    this.getStores();
    
    this.storeService.storeReloadEvent().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((toReload) => {
      this.getStores();
    })
    this.authService.regionChanges().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((isChanged) => {
      if(!isChanged) return;
      this.getStores();
    });


    this.storeService.transactionModalEvent().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((toShow) => {
      this.showTransactionHistoryModal();
    });

    this.onSearchChange.asObservable().pipe(debounceTime(200)).pipe(takeUntil(this.ngUnsubscribe$)).subscribe((val) => {
      console.log("HERE EVERY 200", val)
      if(val==""){
        this.getStores()
      }else{
        this.getStores(val)
      }
    })
  }
  async getStores(productName:any=undefined){
    this.componentState.isStoresLoading = true;
    const resp = await performRequest(this.storeService.getStores(productName).pipe(takeUntil(this.ngUnsubscribe$)))
    if(!Array.isArray(resp)){
      this.nzNotificationService.error("An Error occurred", "Please Try After Sometime");
      return;
    }
    console.log(resp)
    this.componentState.currentStores = resp;
    setTimeout(() => {
      this.componentState.isStoresLoading = false;
    }, 1000);
  }
  async loadTransactionHistory(){
    const resp = await performRequest(this.storeService.getTransactionHistory().pipe(takeUntil(this.ngUnsubscribe$)));
    console.log(resp, "TRANSACT HIST");
    this.componentState.transactionHistory = resp;
    return resp;
  }


  
  askConfirmAddDifferentStoreProduct(differentProduct: any){
    this.nzModalService.confirm({
        nzTitle: 'Clear Your Cart?',
        nzContent: 'You must clear your cart to add items from another store',
        nzOkText: "Clear Cart and Add",
        nzCancelText: "Nevermind",
        nzOnOk: () => {
          this.cartService.clearCart();
          this.addProductToCart(differentProduct);
        },
    });
  }

  addProductToCart(product: any){
    if(Object.keys(this.cart).length){
      const firstProduct = Object.values(this.cart)[0];
      if(firstProduct.storeId != product.store){
        this.askConfirmAddDifferentStoreProduct(product);
        return;
      }
    }
    if(!!this.cart[product.id] && this.cart[product.id].quantity+1> product.inventory){
      this.nzNotificationService.warning("No more pieces available", "There are no more pieces of this item available");
      return;
    }
    if(!this.cart[product.id]){
      this.nzNotificationService.info("Added to Cart", `${product.name} was added to your cart`);
    }
    this.cartService.addToCart({productId: product.id, cost: product.price, name: product.name, storeId:product.store});
  }
  removeProductFromCart(product:any){
    if(!!this.cart[product.id]){
      if(this.cart[product.id].quantity-1 < 0)
        return;
      if(this.cart[product.id].quantity-1===0){
        this.nzNotificationService.info("Removed from Cart", `${product.name} was removed from your cart`);
      }
    }

    this.cartService.reduceItemQuantity(product.id);
  }
  viewStoreInfo(store: any){
    this.componentState.isStoreInfoModalVisible = true;
    this.componentState.clickedStore = store;
  }
  async showTransactionHistoryModal(){
    await this.loadTransactionHistory();
    this.componentState.isTransactionHistoryModalVisible = true;
  }
  onSearch(productName: string){
    // console.log(productName, "TEST")
    this.onSearchChange.next(productName)
  }
}
