import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProductService } from '../product.service';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <h2>Products</h2>
    <ul>
      <li *ngFor="let product of products">
        <a [routerLink]="['/product', product.id]">{{ product.name }}</a>
      </li>
    </ul>
  `,
})
export class ProductListComponent implements OnInit {
  products: any[] = [];

  constructor(private productService: ProductService) {}

  ngOnInit() {
    this.productService.getProducts().subscribe({
      next: (data) => (this.products = data),
      error: (error) => console.error('Error fetching products:', error),
    });
  }
}
