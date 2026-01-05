package com.largebeb.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;
import com.largebeb.model.Room;
import com.largebeb.model.Review;
import com.largebeb.model.RatingStats;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "properties")
public class Property {

    @Id
    private String id; // Maps to MongoDB "_id"

    private String name;
    private String address;
    private String description;

    // List of strings (e.g., "WiFi", "Pool", "AC")
    private List<String> amenities;
    
    // List of Image URLs
    private List<String> photos; 

    private String email;
    private String country;
    private String region;
    private String city;

    // IMPORTANT: Maps the JSON field "manager_id" to Java field "managerId"
    @Field("manager_id")
    private String managerId;

    // Array(2): [Longitude, Latitude]
    // MongoDB expects [x, y], so Longitude first!
    private List<Double> coordinates;

    // Lists of complex objects (Classes defined below)
    private List<Room> rooms;
    private List<Review> latestReviews;

    // Single complex object
    private RatingStats ratingStats;
}