sequenceDiagram
participant User
participant APIService
participant UserLogic
participant UserRepository

User->>APIService: POST /register (email, password)
APIService->>UserLogic: register_user(email, password)

alt Email already exists
    UserLogic-->>APIService: raise EmailAlreadyUsedError
    APIService-->>User: HTTP 409 Conflict (Email already in use)

else Invalid data
    UserLogic-->>APIService: raise ValidationError
    APIService-->>User: HTTP 400 Bad Request (Invalid input)

else Success
    UserLogic->>UserRepository: save_user(user)
    UserRepository-->>UserLogic: user_saved
    UserLogic-->>APIService: return created_user
    APIService-->>User: HTTP 201 Created
end
