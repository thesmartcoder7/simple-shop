import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api';
  private _isLoggedIn = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this._isLoggedIn.asObservable();

  constructor(private http: HttpClient) {
    this._isLoggedIn.next(!!localStorage.getItem('token'));
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login/`, { username, password }).pipe(
      tap((response: any) => {
        localStorage.setItem('token', response.token);
        this._isLoggedIn.next(true);
      })
    );
  }

  signup(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup/`, {
      username,
      email,
      password,
    });
  }

  logout() {
    localStorage.removeItem('token');
    this._isLoggedIn.next(false);
  }
}
