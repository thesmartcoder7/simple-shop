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
        <strong>{{ item.product.name }}</strong> - {{ item.price | currency }}
        <br />
        <em>Category: {{ item.product.category.name }}</em>
        <br />
        Base Price: {{ item.product.base_price | currency }}
        <ul>
          <li *ngFor="let option of item.selected_options">
            {{ option.name }} - {{ option.price | currency }}
          </li>
        </ul>
        <p>Quantity: {{ item.quantity }}</p>
      </li>
    </ul>

    <p>Total:{{ cartItems[0].price | currency }}</p>
    <button (click)="checkout()">Checkout</button>
  `,
})
export class CartComponent implements OnInit {
  cartItems: any[] = [];
  total: number = 0;

  constructor(private cartService: CartService) {}

  ngOnInit() {
    this.cartService.getCart().subscribe(
      (cart) => {
        this.cartItems = cart.items;
        console.log(this.cartItems);
      },
      (error) => {
        console.error('Error fetching cart:', error);
        // Handle error
      }
    );
  }

  checkout() {
    this.cartService.createOrder().subscribe({
      next: () => {
        console.log('Order created');
      },
      error: (error) => console.error('Error creating order:', error),
    });
  }
}
