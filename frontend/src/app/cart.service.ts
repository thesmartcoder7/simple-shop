import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient, private router: Router) { }

  addToCart(productId: number, selectedOptions: number[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/add-to-cart/`, { product_id: productId, selected_options: selectedOptions })
      .pipe(catchError(this.handleError.bind(this)));
  }

  getCart(): Observable<any> {
    return this.http.get(`${this.apiUrl}/cart/`)
      .pipe(catchError(this.handleError.bind(this)));
  }

  createOrder(): Observable<any> {
    return this.http.post(`${this.apiUrl}/create-order/`, {})
      .pipe(catchError(this.handleError.bind(this)));
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