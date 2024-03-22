import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

export interface CartItemObj{
  quantity: number,
  name: string,
  cost: number,
  storeId:string
}

export interface Cart{
  [key: string]: CartItemObj
}

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private _isDrawerOpenSubject: BehaviorSubject<boolean> = new BehaviorSubject(false);
  private _cartChanged: Subject<Cart> = new Subject();
  constructor() { }

  private recordCartChange(newCart: Cart){
    this._cartChanged.next(newCart);
  }
  cartChangesEvent(){
    return this._cartChanged.asObservable();
  }
  getTotalItemQuantity(){
    const cart = this.getCart();
    if(!Object.keys(cart).length){
      return 0
    }
    let totalQty = 0;
    for(let [productId, productObj] of Object.entries(cart)){
      totalQty += productObj.quantity;
    }
    return totalQty;
  }
  
  getCart(): Cart{
    const cart = JSON.parse(localStorage.getItem("user_cart") || "{}");
    return cart;
  }

  isCartEmpty(){
    const cart = JSON.parse(localStorage.getItem("user_cart") || "{}");
    return Object.keys(cart).length === 0;
  }

  clearCart(): Cart{
    localStorage.setItem("user_cart", "{}")
    this.recordCartChange({});
    return {}
  }
  private _saveCart(cart: Cart){
    localStorage.setItem("user_cart", JSON.stringify(cart));
    this.recordCartChange(cart)
  }
  addToCart({productId, cost=undefined, name, storeId}: {productId: string, cost: number|undefined, name?: string, storeId?:string}){
    const cart: Cart = this.getCart();
    if(cart.hasOwnProperty(productId)){
      cart[productId].quantity+=1;
      if(cost!==undefined){
        cart[productId].cost = parseFloat((<any>cost));
      }
      this._saveCart(cart)
      return cart;
    }
    if(!cost || !name || !storeId){
      throw Error("An Error Occurred");
    }
    cart[productId] = {quantity: 1, cost: parseFloat((<any>cost)), name, storeId};
    this._saveCart(cart);
    return cart
  }
  reduceItemQuantity(productId: string){
    const cart: Cart = this.getCart();
    if(!cart.hasOwnProperty(productId)){
      // do nothing
      return;
    }
    cart[productId].quantity -=1;
    if(cart[productId].quantity <=0){
      delete cart[productId]
    }
    this._saveCart(cart)
    return cart
  }
  removeFromCart(productId: string){
    const cart: Cart = this.getCart();
    if(!cart.hasOwnProperty(productId)){
      // do nothing
      return;
    }
    delete cart[productId];
    this._saveCart(cart);
    return cart
  }
  
  getCartTotal(){
    const cart: Cart = this.getCart();
    let total = 0;
    if(!Object.keys(cart).length){
      return total;
    }
    for(let [productId, cartItemData] of Object.entries(cart)){
      total+=(cartItemData.cost *cartItemData.quantity);
    }
    const round_places = 2;
    return Math.round((total + Number.EPSILON) * Math.pow(10,round_places)) / Math.pow(10,round_places);
  }


  setCartDrawerOpen() {
    this._isDrawerOpenSubject.next(true);
  }
  setCartDrawerClosed() {
    this._isDrawerOpenSubject.next(false);
  }
  getCartDrawerObservable() {
    return this._isDrawerOpenSubject.asObservable()
  }
  
}
