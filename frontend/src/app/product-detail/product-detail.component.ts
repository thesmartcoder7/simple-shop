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
  templateUrl: './product-detail.component.html',
  styleUrls: ['./product-detail.component.scss'],
})
export class ProductDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private productService = inject(ProductService);
  private cartService = inject(CartService);

  data: any;
  selectedOptions: { [key: number]: number } = {};
  totalPrice: number = 0;

  ngOnInit() {
    const productId = Number(this.route.snapshot.paramMap.get('id'));
    this.productService.getProduct(productId).subscribe({
      next: (data) => {
        this.data = data;
        console.log(this.data);
        this.updatePrice();
      },
      error: (error) => console.error('Error fetching product:', error),
    });
  }

  updatePrice() {
    const selectedOptionIds = Object.values(this.selectedOptions);
    this.productService
      .calculatePrice(this.data.product.id, selectedOptionIds)
      .subscribe({
        next: (data) => (this.totalPrice = data.price),
        error: (error) => console.error('Error calculating price:', error),
      });
  }

  addToCart() {
    this.cartService
      .addToCart(this.data.product.id, Object.values(this.selectedOptions))
      .subscribe({
        next: () => console.log('Added to cart'),
        error: (error) => console.error('Error adding to cart:', error),
      });
  }
}
