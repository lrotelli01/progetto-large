package com.largebeb.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDate;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "reviews") // Saved in the 'reviews' collection
public class Review {

    @Id
    private String id;
    
    // Links this review to a specific stay/booking
    // Unique index might be useful here to ensure 1 review per reservation
    private String reservationId; 

    private LocalDate creationDate;
    
    private String text;
    
    // Rating from 1 to 5
    @Min(1)
    @Max(5) 
    private Long rating; 
    
    // Optional: The manager can reply to the review
    private String managerReply; 

    @Min(1)
    @Max(5)
    private Double cleanliness;   // Cleanliness
    @Min(1)
    @Max(5)
    private Double communication; // Communication with manager
    @Min(1)
    @Max(5)
    private Double location;      // Location
    @Min(1)
    @Max(5)
    private Double value;         // Value (Value for money)
}