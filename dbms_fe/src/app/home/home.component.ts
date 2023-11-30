import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { StoreService } from '../services/store.service';
import { performRequest } from '../utils';
import { Subject, takeUntil } from 'rxjs';
import { NzNotificationService } from 'ng-zorro-antd/notification';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy{

  private ngUnsubscribe$: Subject<boolean> = new Subject()
  
  constructor(public authService: AuthService,private nzNotificationService: NzNotificationService, private storeService: StoreService){
    
  }

  componentState: any = {isStoresLoading: false, currentStores:[]};
  ngOnDestroy(): void {
    this.ngUnsubscribe$.next(true);
    this.ngUnsubscribe$.complete();
  }

  async ngOnInit() {
    console.log(this.authService.getLoginInfo(), "LOGIN INFO");
    
    this.getStores();
    this.authService.regionChanges().pipe(takeUntil(this.ngUnsubscribe$)).subscribe((isChanged) => {
      if(!isChanged) return;

      this.getStores();
    })
      
  }
  async getStores(){
    this.componentState.isStoresLoading = true;
    const resp = await performRequest(this.storeService.getStores().pipe(takeUntil(this.ngUnsubscribe$)))
    if(!Array.isArray(resp)){
      this.nzNotificationService.error("An Error occurred", "Please Try After Sometime");
      return;
    }
    console.log(resp)
    this.componentState.currentStores = resp;
    setTimeout(() => {
      this.componentState.isStoresLoading = false;
    }, 1000)
    
  }
  viewStoreInfo(store: any){
    this.componentState.isStoreInfoModalVisible = true;
    this.componentState.clickedStore = store;
  }
}
