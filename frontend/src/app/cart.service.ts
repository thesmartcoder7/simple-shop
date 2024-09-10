import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private apiUrl = 'http://localhost:8000/api';  // Adjust this to your Django backend URL

  constructor(private http: HttpClient) { }

  getCart(): Observable<any> {
    return this.http.get(`${this.apiUrl}/cart/`);
  }

  addToCart(productId: number, selectedOptions: number[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/add-to-cart/`, { product_id: productId, selected_options: selectedOptions });
  }

  createOrder(): Observable<any> {
    return this.http.post(`${this.apiUrl}/create-order/`, {});
  }
}