import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Anime Recommender",
    page_icon="⛩️",
    layout="wide"
)

# --- 1. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df = pd.read_csv('animes_final_clean.csv')
    
    # On recrée la matrice des genres pour le moteur
    genres_split = df['Genre_Tags'].str.get_dummies(sep=' / ')
    
    # 1. Extraction du Genre Principal (pour l'emoji)
    # On prend le premier mot avant le "/" (ex: "Action / Shonen" -> "Action")
    df['Genre_Principal'] = df['Genre_Tags'].apply(lambda x: x.split('/')[0].strip() if isinstance(x, str) else 'Autre')
    
    # 2. Le Dictionnaire Magique des Emojis
    emoji_map = {
        "Action": "⚔️",
        "Adventure": "🧭",
        "Comedy": "🤣",
        "Drama": "🎭",
        "Sci-Fi": "🤖",
        "Fantasy": "🐉",
        "Horror": "🧟",
        "Mystery": "🕵️",
        "Romance": "💌",
        "Sports": "🏀",
        "Supernatural": "👻",
        "Slice of Life": "🍵",
        "Suspense": "💣",
        "Award Winning": "🏆"
    }
    
    # 3. On applique l'emoji (avec une télé 📺 par défaut si le genre n'est pas trouvé)
    df['Emoji'] = df['Genre_Principal'].map(emoji_map).fillna("📺")
        
    return df, genres_split

df, genres_split = load_data()

# --- 2. LE MOTEUR DE RECOMMANDATION (Ton Algo) ---
def get_recommendations(titre_cible, top_n=4):
    # Logique identique à ton notebook
    idx = df[df['Anime'] == titre_cible].index[0]
    vecteur_cible = genres_split.iloc[idx]
    
    # Calcul similarité
    scores = genres_split.dot(vecteur_cible)
    
    candidats = df.copy()
    candidats['Genres_Communs'] = scores
    
    # Ton Score Hybride
    col_score = 'Score_Complexe' if 'Score_Complexe' in df.columns else 'Score_Expert'
    candidats['Score_Final'] = candidats['Genres_Communs'] + candidats[col_score]
    
    # Filtres (Pas lui-même + Pas "À éviter")
    filtre = (
        (candidats['Anime'] != titre_cible) & 
        (candidats['Genres_Communs'] > 0) & 
        (~candidats['Segment_Editorial'].str.contains('éviter', case=False, na=False))
    )
    
    return candidats[filtre].sort_values('Score_Final', ascending=False).head(top_n)

# --- 3. L'INTERFACE WEB ---

st.title("⛩️ Le Moteur de Recommandation Ultime")
st.markdown("Bienvenue sur l'outil d'analyse et de recommandation basé sur notre **Score Éditorial Complexe**.")

# Création des onglets
tab1, tab2 = st.tabs(["🔍 Recommandation", "📊 Analyse du Marché"])

# --- ONGLET 1 : RECOMMANDATION ---
with tab1:
    st.header("Trouvez votre prochaine pépite")
    
    col_select, col_display = st.columns([1, 2])
    
    with col_select:
        # Liste déroulante pour choisir l'animé
        choix = st.selectbox("Quel animé avez-vous aimé ?", df['Anime'].unique())
        
        # Affichage de l'animé choisi
        infos_choix = df[df['Anime'] == choix].iloc[0]
        
        # --- CORRECTION ICI : On affiche l'EMOJI au lieu de l'IMAGE ---
        st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{infos_choix['Emoji']}</h1>", unsafe_allow_html=True)
        
        st.write(f"**Studio :** {infos_choix['Studio']}")
        st.write(f"**Note Globale :** {infos_choix['Note_Globale']}/10")
        
        btn = st.button("Lancer la recommandation 🚀", type="primary")

    with col_display:
        if btn:
            recos = get_recommendations(choix)
            
            st.subheader(f"Parce que vous avez aimé *{choix}*, nous vous conseillons :")
            st.write("") # Espace
            
            # Affichage en colonnes (Cartes)
            cols = st.columns(4)
            
            for i, (_, row) in enumerate(recos.iterrows()):
                with cols[i]:
                    # --- REMPLACEMENT DE L'IMAGE PAR L'EMOJI ---
                    # On affiche l'emoji en TRES GROS (taille titre h1)
                    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{row['Emoji']}</h1>", unsafe_allow_html=True)
                    
                    # Le Titre (Centré)
                    st.markdown(f"<h4 style='text-align: center;'>{row['Anime']}</h4>", unsafe_allow_html=True)
                    
                    # Le Score avec couleur
                    score = row['Score_Complexe'] if 'Score_Complexe' in row else row['Score_Expert']
                    st.metric(label="Score Qualité", value=f"{score:.2f}/10")
                    
                    # Le petit badge Verdict
                    verdict = row['Segment_Editorial']
                    if "Chef" in verdict:
                        st.success(f"💎 {verdict}")
                    elif "Très bon" in verdict:
                        st.info(f"✅ {verdict}")
                    elif "Risqué" in verdict:
                        st.warning(f"⚠️ {verdict}")
                    else:
                        st.error(f"⛔ {verdict}")
                    
                    st.caption(f"Studio : {row['Studio']}")

# --- ONGLET 2 : ANALYSE (Ton Scatter Plot Interactif) ---
with tab2:
    st.header("Pourquoi notre Score est meilleur ?")
    
    # Scatter Plot Interactif avec Plotly
    fig = px.scatter(
        df,
        x="Note_Globale",
        y="Score_Expert" if "Score_Expert" in df.columns else "Score_Complexe",
        color="Segment_Editorial",
        size="Nb_Episodes",
        hover_data=["Anime", "Studio"],
        color_discrete_map={
            "Chef-d'œuvre": "#27ae60",
            "Très bon": "#f1c40f",
            "Risqué / Inégal": "#e67e22",
            "À éviter": "#c0392b"
        },
        title="La Matrice de Qualité : Note Publique vs Notre Score"
    )
    # Ligne de neutralité
    fig.add_shape(type="line", x0=0, y0=0, x1=10, y1=10, line=dict(color="Red", width=1, dash="dash"))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Comment lire ce graphique ?**
    * Les points **au-dessus de la ligne rouge** sont valorisés par notre algorithme (Fiables).
    * Les points **en-dessous** sont pénalisés (Trop longs, irréguliers, ou non finis).
    """)