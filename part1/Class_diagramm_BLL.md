classDiagram
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
        +datetime created_at
        +datetime updated_at
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

    %% Relations

    User "1" -- "0..*" Place : owns >
    Place "1" -- "0..*" Review : has >
    User "1" -- "0..*" Review : writes >
    Place "1" o-- "0..*" Amenity : includes >
