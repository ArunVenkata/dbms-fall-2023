import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/envrionment';

@Injectable({
  providedIn: 'root'
})
export class StoreService {

  constructor(private httpClient: HttpClient) { }


  getStores(){
    return this.httpClient.get(`${environment.API_URL}/shop/store/`)
  }
}
