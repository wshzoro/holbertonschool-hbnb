-- Contraintes sur les lieux
ALTER TABLE places
    ADD CONSTRAINT check_price_positive CHECK (price > 0),
    ADD CONSTRAINT check_latitude_range CHECK (latitude BETWEEN -90 AND 90),
    ADD CONSTRAINT check_longitude_range CHECK (longitude BETWEEN -180 AND 180);

-- Contraintes sur les avis
ALTER TABLE reviews
    ADD CONSTRAINT check_rating_range CHECK (rating BETWEEN 1 AND 5);

-- Contraintes sur les équipements
ALTER TABLE amenities
    ADD CONSTRAINT check_name_length CHECK (LENGTH(name) >= 2);

-- Contraintes sur les noms
ALTER TABLE users
    ADD CONSTRAINT check_names_not_empty CHECK (LENGTH(TRIM(first_name)) > 0 AND LENGTH(TRIM(last_name)) > 0);

ALTER TABLE places
    ADD CONSTRAINT check_title_not_empty CHECK (LENGTH(TRIM(title)) > 0),
    ADD CONSTRAINT check_description_not_empty CHECK (LENGTH(TRIM(description)) > 0);

ALTER TABLE reviews
    ADD CONSTRAINT check_text_not_empty CHECK (LENGTH(TRIM(text)) > 0);

-- Contrainte sur la taille des mots de passe
ALTER TABLE users
    ADD CONSTRAINT check_password_length CHECK (LENGTH(password) >= 8);
