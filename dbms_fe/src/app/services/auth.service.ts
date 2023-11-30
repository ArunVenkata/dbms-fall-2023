import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { map, tap } from 'rxjs';
import { environment } from 'src/environments/envrionment';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private accessToken!:any;
  private userInfo: {[key: string]: any} = {};
  
  constructor(private httpClient: HttpClient, private router: Router) {
  }

  getAccessToken(){
    if(!this.isUserLoggedIn()){
      return null
    }
    const login_data = this.getLoginInfo();
    return login_data['access_token']
  }
  isUserLoggedIn(){
    const login_data = this.getLoginInfo();
    if(Object.keys(login_data).length){
      return true;
    }
    return false;
  }

  logOutUser(){
    this.clearLoginInfo();
    this.router.navigate(['/login']);
  }
  private clearLoginInfo(){
    localStorage.removeItem("user_info")
    this.accessToken = "";
    this.userInfo = {};
  }
  private setLoginInfo(accessToken: string, userInfo:any = {}){
    this.userInfo = JSON.parse(JSON.stringify(userInfo));
    userInfo["access_token"] = accessToken;
    localStorage.setItem("user_info", JSON.stringify(userInfo));
    this.accessToken = accessToken;
  }
  getLoginInfo(){
    return JSON.parse(localStorage.getItem("user_info") || "{}");
  }
  private updateRegion(region: any){
    let loginInfo = this.getLoginInfo();
    loginInfo["current_region"] = region;
    this.setLoginInfo(loginInfo['access_token'], loginInfo);
  }
  removeAccessToken(){
    this.logOutUser();
  }


  getUserDetails(){
    let userId = "";
    if(this.isUserLoggedIn()){
      let userInfo = this.getLoginInfo()
      userId = userInfo?.id || "";
      if(userId.length){
        userId+="/"
      }
    }
    return this.httpClient.get(`${environment.API_URL}/user/users/${userId}`)
  }

  loginWithPassword({email, password}: {[key:string]: string}){
    return this.httpClient.post(`${environment.API_URL}/user/login/`, {
      email,password
    }).pipe(map((resp: any) => {
      if(resp?.success){
        this.setLoginInfo(resp.data.token_info.access_token, resp.data);
      }
      return resp;
    }));
  }

  changeRegion(newRegionName: string){
    return this.httpClient.post(`${environment.API_URL}/shop/change-region/`, {
      region: newRegionName
    }).pipe(tap((resp: any) => {
      if(resp && resp.success){
        this.updateRegion(resp.data);
      }
      return resp
    }))
  }
  signUpUser(data:any){
    return this.httpClient.post(`${environment.API_URL}/user/signup/`, {
      ...data
    })
  }
  getSalesPersons(storeId:string){
    // TODO
  }



}
