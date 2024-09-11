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
  quantity: number = 1; // Default quantity
  totalPrice: number = 0; // Default total price

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

  getSelectedOptions(): number[] {
    const selectedOptionsArray: number[] = [];
    for (const partTypeId in this.selectedOptions) {
      if (this.selectedOptions.hasOwnProperty(partTypeId)) {
        selectedOptionsArray.push(this.selectedOptions[partTypeId]);
      }
    }
    return selectedOptionsArray;
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

  addToCart(productId: number, selectedOptions: number[], quantity: number) {
    this.cartService.addToCart(productId, selectedOptions, quantity).subscribe({
      next: () => console.log('Added to cart'),
      error: (error) => console.error('Error adding to cart:', error),
    });
  }
}
