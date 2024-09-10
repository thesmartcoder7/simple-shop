import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <nav>
      <a routerLink="/products">Products</a> |
      <a routerLink="/cart">Cart</a>
    </nav>
    <router-outlet></router-outlet>
  `
})
export class AppComponent { }