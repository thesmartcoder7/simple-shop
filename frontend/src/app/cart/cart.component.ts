import { Component, OnInit } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { CartService } from '../cart.service';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, CurrencyPipe],
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss'],
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
