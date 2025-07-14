-- Index sur les clés étrangères
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_place_amenity_place_id ON place_amenity(place_id);
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);

-- Index de recherche
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_places_title ON places(title);
CREATE INDEX idx_places_price ON places(price);
CREATE INDEX idx_places_location ON places(latitude, longitude);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_amenities_name ON amenities(name);

-- Index composés
CREATE INDEX idx_reviews_place_user ON reviews(place_id, user_id);
CREATE INDEX idx_places_title_price ON places(title, price);
