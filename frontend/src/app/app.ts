import { Component, signal, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FEATURE_FIELDS, FeatureField } from './feature-schema';
import { PredictionService, PredictionResponse } from './prediction.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  fields: FeatureField[] = FEATURE_FIELDS;
  values: Record<string, any> = {};
  result: PredictionResponse | null = null;
  error: string | null = null;
  loading = false;
  deployedStatic = false;

  constructor(private api: PredictionService, private cdr: ChangeDetectorRef) {
    for (const field of this.fields) {
      this.values[field.name] = field.defaultValue;
    }
  }

  submit() {
    this.error = null;
    this.result = null;

    const payload: Record<string, any> = {};

    for (const field of this.fields) {
      const value = this.values[field.name];

      if (value === null || value === undefined || value === '') {
        this.error = `Missing value for ${field.label}`;
        return;
      }

      if (field.kind === 'number') {
        const numeric = Number(value);
        if (Number.isNaN(numeric)) {
          this.error = `Invalid number for ${field.label}`;
          return;
        }
        if ((field.min !== undefined && numeric < field.min) ||
            (field.max !== undefined && numeric > field.max)) {
          this.error = `Out-of-range value for ${field.label}`;
          return;
        }
        payload[field.name] = numeric;
      } else {
        payload[field.name] = String(value);
      }
    }

    this.loading = true;
    this.api.predict(payload).subscribe({
      next: (result) => {
        this.result = result;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = `API error ${err.status || ''}: ` +
          (err.error?.error || err.message || 'Check Flask terminal');
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
  }
}