import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/envrionment';
import { Cart } from '../cart-drawer/cart.service';
import { Subject, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StoreService {

  constructor(private httpClient: HttpClient) { }

  private reloadStores$: Subject<boolean> = new Subject()
  private showTransactionModal$: Subject<boolean> = new Subject();
  getStores(product_name:any=undefined){
    return this.httpClient.get(`${environment.API_URL}/shop/store/`, {
      params: {
        ...(product_name && {product_name})
      }
    })
  }

  storeReloadEvent(){
    return this.reloadStores$.asObservable()
  }

  transactionModalEvent(){
    return this.showTransactionModal$.asObservable()
  }
  triggerTransactionHistoryModal(){
    this.showTransactionModal$.next(true);
  }

  
  private triggerStoresReload(){
    this.reloadStores$.next(true);
  }
  
  checkoutTransaction({cart, salesperson_id=undefined}: {salesperson_id?: any, cart: Cart}){
    return this.httpClient.post(`${environment.API_URL}/shop/transact/`, {
      cart,...(salesperson_id && {salesperson_id})
    }).pipe(tap((resp:any) => {
      if(resp?.success){
        this.triggerStoresReload();
      }
      return resp
    }))
  }
  getTransactionHistory(){
    return this.httpClient.get(`${environment.API_URL}/shop/transaction-history/`)
  }
}
