import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpParams,
  HttpParameterCodec,
  HttpErrorResponse,
  HttpHeaders
} from '@angular/common/http';
import { Observable, throwError, forkJoin, of, iif } from 'rxjs';
import { catchError, concatMap } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AuthService } from './app/services/auth.service';

@Injectable()
export class HttpConfigInterceptor implements HttpInterceptor {
  constructor(
    private router: Router,
    private authService: AuthService
  ) { }


  getAccessToken() {
    return of(this.authService.getAccessToken());
  }


  private handleAuthError(err: HttpErrorResponse): Observable<any> {
    const routeExclusions = ['signup', "login"];
    const apiDomainExclusions: string[] = [];
    if (routeExclusions.some(item => this.router.url.includes(item))) {
      console.log("RETURNING ERR")
      return throwError(() => err);

    }
    if (err.url) {
      const apiUrlObject = new URL(err.url)
      if (apiDomainExclusions.some(item => apiUrlObject.host.toLowerCase().includes(item))) {
        return throwError(() => err);
      }
      if (err.url) {
        const apiUrlObject = new URL(err.url);
        if (apiDomainExclusions.some(item => apiUrlObject.host.toLowerCase().includes(item))) {
          return throwError(() => err);
        }
      }
      // this.authService.removeAccessToken();
      // this.router.navigate([
      //   '/',
      //   'login',
      // ]);
    }
    return throwError(() => err);
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return forkJoin({
      token: iif(() => true, this.getAccessToken(), of(null))
    }).pipe(
      concatMap(({ token }) => {

        if (token && !request.headers.hasOwnProperty("Authorization")) {
          const headers = new HttpHeaders({
            'Authorization': 'Bearer ' + token
          });
          const params = new HttpParams({ encoder: new CustomEncoder(), fromString: request.params.toString() });
          request = request.clone({ headers, params });

        }

        return next.handle(request).pipe(catchError(err => this.handleAuthError(err)));
      })
    );
  }
}



class CustomEncoder implements HttpParameterCodec {
  encodeKey(key: string): string {
    return encodeURIComponent(key);
  }

  encodeValue(value: string): string {
    return encodeURIComponent(value);
  }

  decodeKey(key: string): string {
    return decodeURIComponent(key);
  }

  decodeValue(value: string): string {
    return decodeURIComponent(value);
  }
}
