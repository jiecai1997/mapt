import {NgModule} from "@angular/core";
import { CommonModule } from '@angular/common';
import {
  MatButtonModule, MatCardModule, MatDialogModule, MatDatepickerModule, 
  MatToolbarModule, MatMenuModule, MatIconModule, MatProgressSpinnerModule, 
  MatNativeDateModule, MatListModule, MatSlideToggleModule, MatExpansionModule,
  MatDividerModule, MatGridListModule, MatTabsModule, MatAutocompleteModule,
  MatFormFieldModule, MatTableModule, MatInputModule   
} from '@angular/material';

@NgModule({
  imports: [],
  exports: [
    CommonModule,
    MatToolbarModule, 
    MatButtonModule, 
    MatCardModule, 
    MatInputModule, 
    MatDialogModule, 
    MatTableModule, 
    MatMenuModule,
    MatIconModule,
    MatNativeDateModule,
    MatListModule,
    MatSlideToggleModule,
    MatExpansionModule,
    MatDividerModule,
    MatGridListModule,
    MatTabsModule,
    MatFormFieldModule,
    MatDatepickerModule,
    MatAutocompleteModule,
    MatProgressSpinnerModule
  ]
})
export class CustomMaterialModule { }