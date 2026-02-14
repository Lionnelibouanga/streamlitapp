import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import os

# Configuration de la page
st.set_page_config(page_title="Jeu de données de Vente d'Amazon avec DuckDB", layout="wide")

# Titre de l'application
st.title("Analyse du Jeu de données de vente d'Amazon avec DuckDB et Streamlit")
st.write("Cette application analyse les données de vente d'Amazon en utilisant DuckDB et Streamlit.")

# Fonction pour charger les données de vente d'Amazon
def charger_donnees_Amazon_demo():
    # URL des données Amazon
    url = "https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset?resource=download&select=amazon.csv?raw=true"
    return pd.read_csv(url)


# Sidebar pour le chargement des données
st.sidebar.title("Source de données")
source_option = st.sidebar.radio(
    "Choisir la source de données:",
    ["Données amazon", "Télécharger un fichier CSV"]
)

# Initialiser la connexion DuckDB
conn = duckdb.connect(database=':memory:', read_only=False)


# Obtenir les données
if source_option == "Données amazon":
    df = charger_donnees_Amazon_demo()
    st.sidebar.success("Données amazon de démonstration chargées!")
    
    # Enregistrer les données dans DuckDB
    conn.execute("CREATE TABLE IF NOT EXISTS amazon AS SELECT * FROM df")
    
else:
    uploaded_file = st.sidebar.file_uploader("Télécharger un fichier CSV", type=["csv"])
    if uploaded_file is not None:
        # Sauvegarder temporairement le fichier
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

 # Créer une table à partir du CSV avec DuckDB
        conn.execute(f"CREATE TABLE IF NOT EXISTS amazon  AS SELECT * FROM read_csv_auto('{tmp_path}')")
        
        # Charger les données pour affichage
        df = conn.execute("SELECT * FROM amazon").fetchdf()
        st.sidebar.success(f"{len(df)} Ventes amazon!")

          # Supprimer le fichier temporaire
        os.unlink(tmp_path)
    else:
        st.info("Veuillez télécharger un fichier CSV ou utiliser les données de démonstration.")
        st.stop()

# Afficher un aperçu des données
st.subheader("Aperçu des données de ventes")
st.dataframe(df.head(10))
