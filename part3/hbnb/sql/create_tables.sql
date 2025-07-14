-- Création de la table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table des lieux
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Création de la table des avis
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE (user_id, place_id)
);

-- Création de la table des équipements
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table de liaison Place-Amenity
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Fonction pour générer un UUID v4
CREATE OR REPLACE FUNCTION generate_uuid_v4()
RETURNS CHAR(36) AS $$
SELECT uuid_in(md5(random()::text || clock_timestamp()::text)::cstring);
$$ LANGUAGE SQL;

-- Déclencheur pour générer automatiquement les UUID
CREATE OR REPLACE FUNCTION generate_uuid()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id IS NULL THEN
        NEW.id = generate_uuid_v4();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Création des déclencheurs pour générer les UUID
CREATE TRIGGER generate_user_uuid
    BEFORE INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION generate_uuid();

CREATE TRIGGER generate_place_uuid
    BEFORE INSERT ON places
    FOR EACH ROW
    EXECUTE FUNCTION generate_uuid();

CREATE TRIGGER generate_review_uuid
    BEFORE INSERT ON reviews
    FOR EACH ROW
    EXECUTE FUNCTION generate_uuid();

CREATE TRIGGER generate_amenity_uuid
    BEFORE INSERT ON amenities
    FOR EACH ROW
    EXECUTE FUNCTION generate_uuid();

CREATE TRIGGER generate_place_amenity_uuid
    BEFORE INSERT ON place_amenity
    FOR EACH ROW
    EXECUTE FUNCTION generate_uuid();
