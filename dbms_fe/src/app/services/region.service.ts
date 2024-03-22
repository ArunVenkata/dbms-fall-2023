import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { environment } from 'src/environments/envrionment';
@Injectable({
  providedIn: 'root'
})
export class RegionService {

  constructor(private httpClient: HttpClient) {
    
  }

  getRegions(){
      return this.httpClient.get(`${environment.API_URL}/shop/region/`)
   }
}
