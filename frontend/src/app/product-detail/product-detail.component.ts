import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../product.service';
import { CartService } from '../cart.service';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div *ngIf="product">
      <h2>{{ product.name }}</h2>
      <p>Base Price: {{ product.base_price | currency }}</p>
      <div *ngFor="let partType of product.part_types">
        <h3>{{ partType.name }}</h3>
        <select [(ngModel)]="selectedOptions[partType.id]" (change)="updatePrice()">
          <option *ngFor="let option of partType.options" [value]="option.id">
            {{ option.name }} ({{ option.price | currency }})
          </option>
        </select>
      </div>
      <p>Total Price: {{ totalPrice | currency }}</p>
      <button (click)="addToCart()">Add to Cart</button>
    </div>
  `
})
export class ProductDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private productService = inject(ProductService);
  private cartService = inject(CartService);

  product: any;
  selectedOptions: { [key: number]: number } = {};
  totalPrice: number = 0;

  ngOnInit() {
    const productId = Number(this.route.snapshot.paramMap.get('id'));
    this.productService.getProduct(productId).subscribe({
      next: (data) => {
        this.product = data;
        this.updatePrice();
      },
      error: (error) => console.error('Error fetching product:', error)
    });
  }

  updatePrice() {
    const selectedOptionIds = Object.values(this.selectedOptions);
    this.productService.calculatePrice(this.product.id, selectedOptionIds).subscribe({
      next: (data) => this.totalPrice = data.price,
      error: (error) => console.error('Error calculating price:', error)
    });
  }

  addToCart() {
    this.cartService.addToCart(this.product.id, Object.values(this.selectedOptions)).subscribe({
      next: () => console.log('Added to cart'),
      error: (error) => console.error('Error adding to cart:', error)
    });
  }
}