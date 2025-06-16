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
