package com.largebeb.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "users") // Both Customers and Managers are saved here
public abstract class RegisteredUser {

    @Id
    private String id; // Maps to MongoDB "_id"

    private String username;
    private String email;
    private String password;
    private String name;
    private String surname;
    private String phone;
    
    private String role; // e.g., "CUSTOMER" or "MANAGER"

    // Embedded object for user preferences
    private OptionPreference optionPreference;
}