import sqlite3
import pandas as pd

# 1. Charger le fichier CSV dans un DataFrame pandas
df = pd.read_csv('all_apqc.csv')

# 2. Se connecter à la base de données SQLite (crée le fichier s'il n'existe pas)
conn = sqlite3.connect('all_apqc.db')

# 3. Écrire les données dans la table SQLite
# if_exists='replace' remplace la table si elle existe déjà (vous pouvez mettre 'append' pour l'ajouter)
df.to_sql('all_apqc', conn, if_exists='replace', index=False)

# 4. Fermer la connexion
conn.close()

print("Importation réussie !")
