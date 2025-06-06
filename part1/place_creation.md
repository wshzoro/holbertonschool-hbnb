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