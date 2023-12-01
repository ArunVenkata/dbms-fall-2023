import { Component, OnDestroy, OnInit } from '@angular/core';
import { StoreService } from '../services/store.service';
import { Subject, takeUntil } from 'rxjs';
import { performRequest } from '../utils';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit, OnDestroy {
  
  private ngUnsubscribe$: Subject<boolean> = new Subject();
  isAnalyticsLoading: boolean = false;
  analyticsData: any = {};
  constructor(private storeService: StoreService){

  }


  ngOnDestroy(){
      this.ngUnsubscribe$.next(true);
      this.ngUnsubscribe$.complete();
  }
  ngOnInit(){
    this.loadAnalytics();
  }

  async loadAnalytics(){
    this.isAnalyticsLoading = true;

    const resp = await performRequest(this.storeService.getAnalytics().pipe(takeUntil(this.ngUnsubscribe$)))

    console.log(resp)
    if(resp?.data){
      this.analyticsData = resp.data;
    }
    setTimeout(() => {
      this.isAnalyticsLoading = false;
    }, 700)
  }
}
