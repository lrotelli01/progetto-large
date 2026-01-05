package com.largebeb.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.List;

import com.largebeb.model.RoomStatus;
import com.largebeb.model.BedType;
import com.largebeb.model.Property;


@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "rooms") // Saved in a separate collection, linked by propertyId
public class Room {

    @Id
    private String id;

    // Foreign Key: Links this room to a specific Property (B&B/Hotel)
    private String propertyId; 
    
    private String roomType; // e.g., "Single", "Double", "Suite"
    
    private String name;     // e.g., "Blue Room with Sea View"
    
    // Uses the Enum defined above
    private BedType bed; 
    
    private List<String> amenities;
    private List<String> photos;
    
    // Uses the Enum defined above
    private RoomStatus status; 
    
    // Capacity
    private Long capacityAdults;
    private Long capacityChildren;
    
    // Pricing
    private Float pricePerNightAdults;
    private Float pricePerNightChildren;
}