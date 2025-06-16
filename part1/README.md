# Holbertonschool-HBNB

# High-Level Package Diagram

<img width="209" alt="Capture d’écran 2025-06-06 à 19 10 41" src="https://github.com/user-attachments/assets/ea647f1d-55dd-4b69-bae6-e7745eb1113f" />

this diagram that illustrates the three-layer architecture of the HBnB application and the communication between these layers via the facade pattern

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

## Overview

### User  
Represents an individual using the platform.

| Attribute   | Type     | Description                |
|-------------|----------|----------------------------|
| id          | UUID     | Unique identifier           |
| first_name  | string   | User's first name           |
| last_name   | string   | User's last name            |
| email       | string   | Email address (unique)      |
| password    | string   | Hashed password             |
| created_at  | datetime | Record creation timestamp   |
| updated_at  | datetime | Last update timestamp       |

**Key Methods:** `save()`, `register()`, `delete()`

---

### Place  
Represents a property available for booking or rental.

| Attribute   | Type     | Description                |
|-------------|----------|----------------------------|
| id          | UUID     | Unique identifier           |
| name        | string   | Property name               |
| description | string   | Property description        |
| price       | float    | Price per night             |
| latitude    | float    | Geographic latitude         |
| longitude   | float    | Geographic longitude        |

**Key Methods:** `save()`, `create()`, `list()`, `delete()`

---

### Review  
Represents user feedback for a place.

| Attribute   | Type     | Description                   |
|-------------|----------|-------------------------------|
| id          | UUID     | Unique identifier              |
| text        | string   | Review content                 |
| rating      | int      | Numeric rating (e.g., 1-5)    |
| created_at  | datetime | Timestamp of review creation   |
| updated_at  | datetime | Timestamp of last update       |

**Key Methods:** `save()`, `delete()`

---

### Amenity  
Represents a feature or facility provided at a place (e.g., Wi-Fi, pool).

| Attribute   | Type     | Description                  |
|-------------|----------|------------------------------|
| id          | UUID     | Unique identifier             |
| name        | string   | Name of the amenity           |
| description | string   | Amenity details               |

**Key Methods:** `save()`, `list()`, `delete()`


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
| User           | The frontend user interacting with the registration form.                   |
| APIService     | The backend API receiving and routing requests (e.g., Flask, FastAPI).      |
| UserLogic      | The business logic validating data and applying registration rules.         |
| UserRepository | Handles saving and retrieving user data from the database or storage layer. |

## Review Submission Flow – Sequence Diagram

This diagram shows how a user submits a review in the HBnB project.
It includes what the user does on the frontend, how the API handles it, and how the backend checks and saves the review.


```mermaid
sequenceDiagram
    participant User as Frontend User
    participant APIService as API (ReviewAPI)
    participant ReviewLogic as Business Logic (ReviewService)
    participant PlaceRepository as Persistence (PlaceRepository)
    participant ReviewRepository as Persistence (ReviewRepository)
    participant AuthService as AuthService

    User->>User: Fill out review form { rating, comment, place_id }
    User->>APIService: Click "Submit Review" → POST /reviews { rating, comment, place_id, token }
    APIService->>AuthService: verify_token(token)

    alt Invalid or expired token
        AuthService-->>APIService: raise AuthorizationError
        APIService-->>User: HTTP 401 Unauthorized { "error": "You must be logged in" }

    else Valid token
        AuthService-->>APIService: user_authenticated
        APIService->>ReviewLogic: submit_review(data, user_id)
        ReviewLogic->>PlaceRepository: check_place_exists(place_id)

        alt Place does not exist
            PlaceRepository-->>ReviewLogic: raise NotFoundError
            ReviewLogic-->>APIService: raise NotFoundError
            APIService-->>User: HTTP 404 Not Found { "error": "Place not found" }

        else Place exists
            PlaceRepository-->>ReviewLogic: place_ok
            ReviewLogic->>ReviewRepository: check_duplicate_review(user_id, place_id)

            alt Review already submitted
                ReviewRepository-->>ReviewLogic: raise DuplicateReviewError
                ReviewLogic-->>APIService: raise DuplicateReviewError
                APIService-->>User: HTTP 409 Conflict { "error": "Review already submitted for this place" }

            else Not duplicate
                ReviewRepository-->>ReviewLogic: OK

                alt Invalid input (e.g., empty comment or rating out of bounds)
                    ReviewLogic-->>APIService: raise ValidationError
                    APIService-->>User: HTTP 400 Bad Request { "error": "Invalid rating or comment" }

                else Success
                    ReviewLogic->>ReviewRepository: save_review(review)
                    ReviewRepository-->>ReviewLogic: review_saved
                    ReviewLogic-->>APIService: return created_review
                    APIService-->>User: HTTP 201 Created { id, rating, comment, created_at, place_id, user_id }
                end
            end
        end
    end

```
## Overview

| Component        | Role                                                      |
|------------------|-----------------------------------------------------------|
| Frontend User    | Fills and submits the review form                         |
| APIService       | Entry point for handling `/reviews` POST requests         |
| AuthService      | Verifies and validates the user's access token            |
| ReviewLogic      | Core logic: validation, duplication check, save           |
| PlaceRepository  | Checks if the place to review exists                      |
| ReviewRepository | Detects duplicate reviews and saves review data           |

## Place Creation – Sequence Diagram

This diagram show **Place creation flow** in the HBnB project. It describes how the system processes a user request to create a new place, covering frontend interaction, backend logic, and error handling.


```mermaid
sequenceDiagram
    participant User
    participant APIService
    participant PlaceLogic
    participant PlaceRepository

    User->>APIService: POST /places (place data)
    APIService->>PlaceLogic: create_place(data)

    alt Missing required fields
        PlaceLogic-->>APIService: raise ValidationError
        APIService-->>User: HTTP 400 Bad Request (Missing or invalid fields)

    else Unauthorized access
        PlaceLogic-->>APIService: raise AuthorizationError
        APIService-->>User: HTTP 401 Unauthorized (Authentication required)

    else Success
        PlaceLogic->>PlaceRepository: save_place(place)
        PlaceRepository-->>PlaceLogic: place_saved
        PlaceLogic-->>APIService: return created_place
        APIService-->>User: HTTP 201 Created
    end
```

## Overview

| Component         | Role                                                             |
|------------------|------------------------------------------------------------------|
| Frontend User     | Fills and submits the review form                                |
| Display           | Shows UI messages or errors to the user                          |
| APIService        | Entry point for handling `/reviews` POST requests                |
| AuthService       | Verifies and validates the user's access token                   |
| ReviewLogic       | Core logic: validation, duplication check, save                  |
| PlaceRepository   | Checks if the place to review exists                             |
| ReviewRepository  | Detects duplicate and saves review data                          |

## List Places - Sequence Diagram 

This digram describes the flow of retrieving a list of places through the HBnB API, including error handling.


```mermaid
sequenceDiagram
participant User
participant APIService
participant PlaceLogic
participant PlaceRepository

User->>APIService: GET /places?city=Paris
APIService->>PlaceLogic: get_places(filters)

alt Invalid filters
    PlaceLogic-->>APIService: raise ValidationError
    APIService-->>User: HTTP 400 Bad Request

else Database error
    PlaceLogic-->>APIService: raise DatabaseError
    APIService-->>User: HTTP 500 Internal Server Error

else Success
    PlaceLogic->>PlaceRepository: fetch_places(filters)
    PlaceRepository-->>PlaceLogic: list_of_places
    PlaceLogic-->>APIService: return list_of_places
    APIService-->>User: HTTP 200 OK (JSON)
end
```
## Overview 

| Component       | Role                                              |
|-----------------|---------------------------------------------------|
| User       | The user making the request                        |
| APIService  | API entry point handling the request              |
| PlaceLogic  | Business logic: validation, error handling, filtering |
| PlaceRepository | Data access layer retrieving places from the database |

## documentation 
https://docs.google.com/document/d/1setrbs93z5_2LNSnfRO_MrhQFYcA0MgyF7hTyRmvdKw/edit?usp=sharing
