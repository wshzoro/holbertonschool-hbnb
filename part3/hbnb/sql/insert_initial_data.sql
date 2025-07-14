-- Insérer l'utilisateur administrateur
INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$V4Q6JqY7Jz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8Gz8', -- Hachage généré précédemment
    TRUE
);

-- Insérer les équipements initiaux
-- UUID générés aléatoirement
INSERT INTO amenities (id, name)
VALUES 
    ('1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p', 'Wi-Fi'),
    ('2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q', 'Piscine'),
    ('3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', 'Climatisation');
