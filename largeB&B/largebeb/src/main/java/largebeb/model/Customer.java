package com.largebeb.model;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import com.largebeb.model.RegisteredUser;
import com.largebeb.model.MethodPayment;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true) // Includes parent fields in comparison
public class Customer extends RegisteredUser {

    // Specific field only for Customers
    private MethodPayment methodPayment; 
}