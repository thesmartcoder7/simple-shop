import { Injectable } from '@angular/core';
import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class CartService {
  private apiUrl = 'http://localhost:8000/api';
  private sessionKey: string | null = null;
  router: any;

  constructor(private http: HttpClient) {
    this.sessionKey = localStorage.getItem('sessionKey');
  }

  private getHeaders(): HttpHeaders {
    let headers = new HttpHeaders();
    if (this.sessionKey) {
      headers = headers.set('X-Session-Key', this.sessionKey);
    }
    return headers;
  }

  addToCart(
    productId: number,
    selectedOptions: number[],
    quantity: number
  ): Observable<any> {
    const url = `${this.apiUrl}/add-to-cart/`;
    const body = {
      product_id: productId,
      selected_options: selectedOptions,
      quantity,
    };
    return this.http.post(url, body, { headers: this.getHeaders() }).pipe(
      tap((response: any) => {
        if (response.session_key) {
          this.sessionKey = response.session_key;
          localStorage.setItem('sessionKey', response.session_key);
        }
      })
    );
  }

  getCart(): Observable<any> {
    const url = `${this.apiUrl}/cart/`;
    return this.http.get(url, { headers: this.getHeaders() });
  }

  createOrder(): Observable<any> {
    return this.http
      .post(`${this.apiUrl}/create-order/`, {}, { headers: this.getHeaders() })
      .pipe(
        tap((response: any) => {
          if (response.session_key) {
            this.sessionKey = response.session_key;
            localStorage.setItem('sessionKey', response.session_key);
          }
        })
      );
  }

  private handleError(error: HttpErrorResponse): Observable<any> {
    if (error.status === 401 || error.status === 403) {
      // Redirect to login page for authentication errors or forbidden access
      console.log('Please log in to access this feature');
      this.router.navigate(['/login']);
    } else {
      // Log other errors
      console.error('An error occurred:', error.error);
    }
    return of(null); // Return an empty observable
  }
}
