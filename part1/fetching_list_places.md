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