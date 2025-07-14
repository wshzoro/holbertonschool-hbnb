-- Procédure pour créer un nouvel utilisateur
CREATE OR REPLACE FUNCTION create_user(
    _first_name VARCHAR(255),
    _last_name VARCHAR(255),
    _email VARCHAR(255),
    _password VARCHAR(255)
) RETURNS users AS $$
BEGIN
    INSERT INTO users (first_name, last_name, email, password)
    VALUES (_first_name, _last_name, _email, _password)
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Procédure pour créer un nouveau lieu
CREATE OR REPLACE FUNCTION create_place(
    _title VARCHAR(255),
    _description TEXT,
    _price DECIMAL(10, 2),
    _latitude FLOAT,
    _longitude FLOAT,
    _owner_id CHAR(36)
) RETURNS places AS $$
BEGIN
    INSERT INTO places (title, description, price, latitude, longitude, owner_id)
    VALUES (_title, _description, _price, _latitude, _longitude, _owner_id)
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Procédure pour ajouter un avis
CREATE OR REPLACE FUNCTION add_review(
    _text TEXT,
    _rating INTEGER,
    _user_id CHAR(36),
    _place_id CHAR(36)
) RETURNS reviews AS $$
BEGIN
    INSERT INTO reviews (text, rating, user_id, place_id)
    VALUES (_text, _rating, _user_id, _place_id)
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Procédure pour ajouter un équipement à un lieu
CREATE OR REPLACE FUNCTION add_amenity_to_place(
    _place_id CHAR(36),
    _amenity_id CHAR(36)
) RETURNS void AS $$
BEGIN
    INSERT INTO place_amenity (place_id, amenity_id)
    VALUES (_place_id, _amenity_id)
    ON CONFLICT (place_id, amenity_id) DO NOTHING;
END;
$$ LANGUAGE plpgsql;

-- Procédure pour mettre à jour la note moyenne d'un lieu
CREATE OR REPLACE FUNCTION update_place_average_rating(
    _place_id CHAR(36)
) RETURNS void AS $$
BEGIN
    UPDATE places
    SET average_rating = (
        SELECT AVG(rating)
        FROM reviews
        WHERE place_id = _place_id
    )
    WHERE id = _place_id;
END;
$$ LANGUAGE plpgsql;
