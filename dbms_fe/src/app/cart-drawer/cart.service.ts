import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface CartItemObj{
  quantity: number,
  name: string,
  cost: number
}

export interface Cart{
  [key: string]: CartItemObj
}

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private _isDrawerOpenSubject: BehaviorSubject<boolean> = new BehaviorSubject(false);

  constructor() { }

  getCart(): Cart{
    const cart = JSON.parse(localStorage.getItem("user_cart") || "{}");
    return cart
  }
  private _saveCart(cart: Cart){
    localStorage.setItem("user_cart", JSON.stringify(cart));
  }
  addToCart({productId, cost=undefined, name}: {productId: string, cost: number|undefined, name?: string}){
    const cart: Cart = this.getCart();
    if(cart.hasOwnProperty(productId)){
      cart[productId].quantity+=1;
      if(cost!==undefined){
        cart[productId].cost = cost;
      }
      this._saveCart(cart)
      return cart;
    }
    if(!cost || !name){
      throw Error("An Error Occurred");
    }
    
    cart[productId] = {quantity: 1, cost, name};
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
      total+=cartItemData.cost;
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
