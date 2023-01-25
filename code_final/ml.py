import warnings
import sqlite3
import pickle
import pandas as pd
import mysql.connector
warnings.filterwarnings("ignore")

# Connexion au BDD MySQL et SQLite
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="azerty",
  database="web"
)
conn = sqlite3.connect('/Users/lulu/Desktop/Ynov/M2/Ydays/webservices/db.sqlite3', timeout=10)

# Récupération des datas depuis la fonction read_sql de pandas pour insert automatiquement les données dans un DataFrame
data = pd.read_sql("SELECT patient_id, JSON_UNQUOTE(json_extract(data_json, '$.MIMAT0005898')) AS 'MIMAT0005898', JSON_UNQUOTE(json_extract(data_json, '$.MIMAT0005951')) AS 'MIMAT0005951', JSON_UNQUOTE(json_extract(data_json, '$.MIMAT0019691')) AS 'MIMAT0019691', JSON_UNQUOTE(json_extract(data_json, '$.MIMAT0027623')) AS 'MIMAT0027623', JSON_UNQUOTE(json_extract(data_json, '$.MIMAT0027650')) AS 'MIMAT0027650' FROM PersonalData", mydb)

# Chargement du modèle en .pkl
P = pickle.load(open('/Users/lulu/Desktop/Ynov/M2/Ydays/webservices/Python/model_breast_cancer.pkl', 'rb'))

# Récupération des données en x pour les MIMAT, le patient_id en string pour le patient_id (utile pour l'insert dans la bdd)
x = data.iloc[:, 1:].values
patient_id = data.iloc[:, 0].values
patient_id = str(patient_id[0])

# Lancement de la prediction avec les données récupérées au-dessus, modification du type pour l'avoir en str
x_predict = P.predict(x)
x_predict = str(x_predict[0])

# Insertion des données dans la table webapp_result de SQLite et commit puis fermeture de la connexion
conn.execute("INSERT INTO webapp_result (Id_Patient, Prediction, Type) VALUES ('"+patient_id+"',"+x_predict+", 'ML')")
conn.commit()
conn.close()
