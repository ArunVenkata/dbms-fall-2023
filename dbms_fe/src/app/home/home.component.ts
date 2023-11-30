import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { StoreService } from '../services/store.service';
import { performRequest } from '../utils';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy{

  private ngUnsubscribe$: Subject<boolean> = new Subject()
  
  constructor(public authService: AuthService, private storeService: StoreService){
    
  }
  ngOnDestroy(): void {
    this.ngUnsubscribe$.next(true);
    this.ngUnsubscribe$.complete();
  }

  async ngOnInit() {
    console.log(this.authService.getLoginInfo(), "LOGIN INFO");
    
    this.getStores();

      
  }
  async getStores(){
    const resp = await performRequest(this.storeService.getStores().pipe(takeUntil(this.ngUnsubscribe$)))
    console.log("STORES", resp)
  }
}
