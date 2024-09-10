import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'http://localhost:8000/api';  // Adjust this to your Django backend URL

  constructor(private http: HttpClient) { }

  getProducts(): Observable<any> {
    return this.http.get(`${this.apiUrl}/products/`);
  }

  getProduct(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/product/${id}/`);
  }

  calculatePrice(productId: number, selectedOptions: number[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/calculate-price/`, { product_id: productId, selected_options: selectedOptions });
  }
}