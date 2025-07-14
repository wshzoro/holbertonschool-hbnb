```mermaid
erDiagram
    User ||--o{ Place : "owns"
    User ||--o{ Review : "writes"
    Place ||--o{ Review : "receives"
    Place }|--|| User : "owned by"
    Place }o--o{ Amenity : "has"
    Amenity }o--o{ Place : "belongs to"
    Place_Amenity }|--|| Place : "references"
    Place_Amenity }|--|| Amenity : "references"

    User {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    Place {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    Review {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    Amenity {
        string id PK
        string name
    }

    Place_Amenity {
        string place_id PK, FK
        string amenity_id PK, FK
    }
