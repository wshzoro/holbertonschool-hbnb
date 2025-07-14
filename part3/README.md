# 🏠 HBnB - Database & SQL Storage

Welcome to the technical documentation for the **HBnB (HolbertonBnB)** project database. This part thoroughly explains the **relational database structure**, the **entity relationships**, and how storage is handled using **SQLAlchemy** in Python.

---

## 📌 Objective

- Design a robust and consistent relational database schema
- Visualize all key entities and their relationships with an **ER diagram**
- Understand how different entities like users, places, reviews, and amenities are linked
- Use **SQLAlchemy ORM** to manage storage in the database seamlessly

---

## 🗃️ Database Architecture Overview

The project uses a relational schema consisting of the following **tables/entities**:

| Table           | Description                                     |
|------------------|-------------------------------------------------|
| `User`           | Stores user information                         |
| `Place`          | Stores places/homes owned by users              |
| `Review`         | User-generated reviews for places               |
| `Amenity`        | Features/services available in places           |
| `Place_Amenity`  | Association table linking places to amenities   |

---

## 🔗 Entity Relationships

Below is a full overview of the **logical relationships** between tables:

- 🔹 **User → Place**: A user can own multiple places (1:N)
- 🔹 **User → Review**: A user can write multiple reviews (1:N)
- 🔹 **Place → Review**: A place can receive multiple reviews (1:N)
- 🔹 **Place ↔ Amenity**: Many-to-Many via `Place_Amenity`
- 🔹 **Place_Amenity**: Association table to manage many-to-many relationship

---

## 🔍 ER Diagram (Mermaid.js)

Use this to visualize the schema structure:

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
