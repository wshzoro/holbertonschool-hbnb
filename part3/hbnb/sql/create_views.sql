-- Vue pour les statistiques des lieux
CREATE VIEW place_stats AS
SELECT 
    p.id as place_id,
    p.title,
    p.price,
    COUNT(r.id) as review_count,
    AVG(r.rating) as average_rating,
    COUNT(DISTINCT a.id) as amenity_count
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
LEFT JOIN place_amenity pa ON p.id = pa.place_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
GROUP BY p.id, p.title, p.price;

-- Vue pour les statistiques des utilisateurs
CREATE VIEW user_stats AS
SELECT 
    u.id as user_id,
    u.first_name,
    u.last_name,
    COUNT(DISTINCT p.id) as place_count,
    COUNT(DISTINCT r.id) as review_count,
    AVG(r.rating) as average_rating
FROM users u
LEFT JOIN places p ON u.id = p.owner_id
LEFT JOIN reviews r ON u.id = r.user_id
GROUP BY u.id, u.first_name, u.last_name;

-- Vue pour les équipements populaires
CREATE VIEW popular_amenities AS
SELECT 
    a.id as amenity_id,
    a.name,
    COUNT(DISTINCT p.id) as place_count
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
JOIN places p ON pa.place_id = p.id
GROUP BY a.id, a.name
ORDER BY place_count DESC;
