package com.largebeb.model;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import com.largebeb.model.RegisteredUser;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class Manager extends RegisteredUser {

    // Specific field only for Managers
    private String iban;
}