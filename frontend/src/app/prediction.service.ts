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

const RENDER_API_URL = 'https://lendingclub-api.onrender.com';

function getApiBase(): string {
  // When running locally via `ng serve`, use the relative path so the
  // dev proxy (proxy.conf.json) forwards it to local Flask.
  // When running on GitHub Pages (or any other static host), call
  // Render's live URL directly, since there is no proxy there.
  if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    return '';
  }
  return RENDER_API_URL;
}

@Injectable({ providedIn: 'root' })
export class PredictionService {
  constructor(private http: HttpClient) {}

  predict(payload: Record<string, any>): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>(`${getApiBase()}/api/predict`, payload);
  }

  health(): Observable<any> {
    return this.http.get(`${getApiBase()}/api/health`);
  }
}