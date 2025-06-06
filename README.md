# Holbertonschool-HBNB
# Business Logic Layer – Class Diagram 

This document presents the **class diagram** for the Business Logic Layer of the **HBnB project**, modeled using **Mermaid.js** syntax. It defines the key entities, their attributes, methods, and the relationships between them, providing a clear abstraction of the core business logic.

---

## UML Class Diagram

```mermaid
classDiagram
direction TB
    class User {
        +UUID id
        +string first_name
        +string last_name
        +string email
        +string password
        +datetime created_at
        +datetime updated_at
        +save()
        +register()
        +delete()
    }

    class Place {
        +UUID id
        +string name
        +string description
        +float price
        +float latitude
        +float longitude
        +save()
        +create()
        +list()
        +delete()
    }

    class Review {
        +UUID id
        +string text
        +int rating
        +datetime created_at
        +datetime updated_at
        +save()
        +delete()
    }

    class Amenity {
        +UUID id
        +string name
        +string description
        +save()
        +list()
        +delete()
    }

    note "This is a sample note"
    User "1" --> "*" Place : owns
    Place "1" --> "*" Review : has
    User "1" --> "*" Review : writes
    Place "1" o-- "*" Amenity : includes
```
 **Overview** 

User
Represents a platform user.

Attribute	Type	Description
id	UUID	Unique ID
first_name	string	First name
last_name	string	Last name
email	string	Unique email address
password	string	Hashed password
created_at	datetime	When user was created
updated_at	datetime	Last update time
Main methods: save(), register(), delete()

Place
Represents a property to rent or book.

Attribute	Type	Description
id	UUID	Unique ID
name	string	Property name
description	string	Description of place
price	float	Price per night
latitude	float	Location latitude
longitude	float	Location longitude
Main methods: save(), create(), list(), delete()

Review
Represents feedback by users on places.

Attribute	Type	Description
id	UUID	Unique ID
text	string	Review content
rating	int	Rating (e.g., 1 to 5)
created_at	datetime	Creation date
updated_at	datetime	Last update date
Main methods: save(), delete()

Amenity
Represents features offered at a place (Wi-Fi, pool, etc.).

Attribute	Type	Description
id	UUID	Unique ID
name	string	Amenity name
description	string	Details about amenity
Main methods: save(), list(), delete()

🔗 Relationships

Relationship	Description
User → Place	A user can own many places
Place → Review	A place can have many reviews
User → Review	A user can write many reviews
Place o-- Amenity	A place includes many amenities
📌 Notes

All entities use UUID for unique IDs.
Timestamp fields track creation and updates.
Methods like save() and delete() manage persistence.
Relationships use UML notation for clarity.
🛠 How to View

Use a Mermaid-compatible viewer (GitHub, VS Code extension).
Paste the Mermaid code in your Markdown .md file.
Or try online Mermaid editors.
📁 Project Location

This diagram corresponds to the Business Logic Layer
Found in part1/ folder of the holbertonschool-hbnb repo.



# Sequence Diagrams for API Calls 

## User Registration Sequence Diagram

This document describes the flow of the user registration process in the HBnB project using a **Mermaid.js sequence diagram**. It captures both frontend interactions and backend business logic processing, including validation, error handling, and data persistence.

---

```mermaid
sequenceDiagram
    participant User as Frontend User
    participant APIService as API (UserAPI)
    participant UserLogic as Business Logic (UserService)
    participant UserRepository as Persistence (UserRepository)

    User->>User: Fill out registration form\n{ email, password, first_name, last_name }
    User->>APIService: Click "Register" → POST /register\n{ email, password, first_name, last_name }
    APIService->>UserLogic: register_user(data)

    alt Email already exists
        UserLogic-->>APIService: raise EmailAlreadyUsedError
        APIService-->>User: HTTP 409 Conflict { "error": "Email already in use" }

    else Invalid email format
        UserLogic-->>APIService: raise InvalidEmailError
        APIService-->>User: HTTP 400 Bad Request { "error": "Invalid email address" }

    else Password too short
        UserLogic-->>APIService: raise WeakPasswordError
        APIService-->>User: HTTP 400 Bad Request { "error": "Password must be at least 8 characters" }

    else Missing required fields
        UserLogic-->>APIService: raise ValidationError
        APIService-->>User: HTTP 400 Bad Request { "error": "Missing required fields" }

    else Invalid characters in name
        UserLogic-->>APIService: raise InvalidNameError
        APIService-->>User: HTTP 400 Bad Request { "error": "First and last name must contain only letters" }

    else Success
        UserLogic->>UserRepository: save_user(user)
        UserRepository-->>UserLogic: user_saved
        UserLogic-->>APIService: return created_user
        APIService-->>User: HTTP 201 Created\n{ id, email, first_name, last_name, is_admin, created_at }
    end
```
 Legend

| Participant        | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| **User**           | The frontend user interacting with the registration form.                   |
| **APIService**     | The backend API receiving and routing requests (e.g., Flask, FastAPI).      |
| **UserLogic**      | The business logic validating data and applying registration rules.         |
| **UserRepository** | Handles saving and retrieving user data from the database or storage layer. |

