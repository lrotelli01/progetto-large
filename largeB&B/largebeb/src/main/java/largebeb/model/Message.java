package largebeb.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Document(collection = "messages") // Matches the MongoDB collection name
public class Message {

    @Id
    private String id; // Maps to "_id" automatically

    @Field("sender_id") // Maps JSON "sender_id" to Java "senderId"
    private String senderId;

    @Field("recipient_id") // Maps JSON "recipient_id" to Java "recipientId"
    private String recipientId;

    private LocalDateTime timestamp; // Spring automatically parses ISO dates

    private String content;

    @Field("is_read") // Maps JSON "is_read" to Java "isRead"
    private Boolean isRead;
}