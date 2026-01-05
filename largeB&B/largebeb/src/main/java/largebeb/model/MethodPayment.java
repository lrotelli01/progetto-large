package com.largebeb.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MethodPayment {

    private String type;      // e.g., "paypal", "credit_card"
    private String provider;  // e.g., "Mastercard", "Visa"
    
}