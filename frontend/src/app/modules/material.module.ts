import {NgModule} from "@angular/core";
import { CommonModule } from '@angular/common';
import {
  MatButtonModule, MatCardModule, MatDialogModule, MatInputModule, MatTableModule,
  MatToolbarModule, MatMenuModule,MatIconModule, MatProgressSpinnerModule, 
  MatNativeDateModule, MatListModule, MatSlideToggleModule
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
   MatProgressSpinnerModule
   ],
})
export class CustomMaterialModule { }