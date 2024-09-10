import { Component, OnInit } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { CartService } from '../cart.service';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, CurrencyPipe],
  template: `
    <h2>Your Cart</h2>
    <ul>
      <li *ngFor="let item of cartItems">
        {{ item.product.name }} - {{ item.price | currency }}
      </li>
    </ul>
    <p>Total: {{ total | currency }}</p>
    <button (click)="checkout()">Checkout</button>
  `,
})
export class CartComponent implements OnInit {
  cartItems: any[] = [];
  total: number = 0;

  constructor(private cartService: CartService) {}

  ngOnInit() {
    this.loadCart();
  }

  loadCart() {
    this.cartService.getCart().subscribe({
      next: (data) => {
        this.cartItems = data.items;
        this.total = data.items.reduce(
          (sum: number, item: any) => sum + item.price,
          0
        );
      },
      error: (error) => console.error('Error fetching cart:', error),
    });
  }

  checkout() {
    this.cartService.createOrder().subscribe({
      next: () => {
        console.log('Order created');
        this.loadCart(); // Refresh cart after order creation
      },
      error: (error) => console.error('Error creating order:', error),
    });
  }
}
