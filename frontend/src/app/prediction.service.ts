import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PredictionResponse {
  prediction: string;
  risk_probability: number;
  risk_level: string;
  threshold_used: number;
  recommendations: string[];
  disclaimer: string;
}

@Injectable({ providedIn: 'root' })
export class PredictionService {
  constructor(private http: HttpClient) {}

  predict(payload: Record<string, any>): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>('/api/predict', payload);
  }

  health(): Observable<any> {
    return this.http.get('/api/health');
  }
}