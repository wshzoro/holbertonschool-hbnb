import bcrypt

# Mot de passe à hacher
password = "admin1234"

# Générer le hachage
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Afficher le hachage en format hexadécimal
print(hashed_password.hex())
