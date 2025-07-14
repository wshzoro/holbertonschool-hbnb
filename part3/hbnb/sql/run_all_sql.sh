#!/bin/bash

# Script pour exécuter tous les scripts SQL dans l'ordre correct

# Vérifier si psql est installé
if ! command -v psql &> /dev/null; then
    echo "Erreur: psql n'est pas installé. Veuillez installer PostgreSQL."
    exit 1
fi

# Vérifier si le fichier de configuration existe
if [ ! -f "db_config.txt" ]; then
    echo "Erreur: fichier de configuration db_config.txt manquant."
    echo "Créez un fichier db_config.txt avec le format suivant :"
    echo "host=localhost"
    echo "port=5432"
    echo "dbname=hbndb"
    echo "user=postgres"
    echo "password=votre_mot_de_passe"
    exit 1
fi

# Lire les paramètres de connexion
source db_config.txt

# Fonction pour exécuter un script SQL
execute_sql() {
    echo "Exécution de $1..."
    psql -h "$host" -p "$port" -d "$dbname" -U "$user" -f "$1"
    if [ $? -ne 0 ]; then
        echo "Erreur lors de l'exécution de $1"
        exit 1
    fi
}

# Exécuter les scripts dans l'ordre correct
execute_sql "sql/create_tables.sql"
execute_sql "sql/update_timestamps.sql"
execute_sql "sql/create_indexes.sql"
execute_sql "sql/add_constraints.sql"
execute_sql "sql/create_views.sql"
execute_sql "sql/create_procedures.sql"
execute_sql "sql/insert_initial_data.sql"

# Afficher un message de succès
echo "Tous les scripts SQL ont été exécutés avec succès !"
