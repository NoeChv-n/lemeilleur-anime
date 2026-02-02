# Analyse Quantitative et Système de Recommandation d'Animes

## 1. Contexte et Objectif
La critique d'œuvres culturelles, et particulièrement celle des animes, souffre souvent d'un biais de subjectivité important. Ce projet vise à rationaliser cette approche en construisant un **Score Complexe pondéré**, capable de distinguer les œuvres techniquement irréprochables des simples succès populaires.

L'objectif est double :
1.  **Établir un classement rigoureux** prenant en compte non seulement la note globale, mais aussi la régularité de la production et la capacité de l'œuvre à engager son audience sur la durée.
2.  **Déployer une interface de recommandation** (via Streamlit) permettant d'explorer ce catalogue selon une segmentation éditoriale précise.

## 2. Méthodologie de Notation (L'Algorithme)

Pour pallier les limites des moyennes arithmétiques classiques, un algorithme de scoring propriétaire a été développé. Il agrège quatre dimensions fondamentales :

### A. La Formule du Score Complexe
La note finale (/10) est calculée selon la pondération suivante :

| Dimension | Poids | Description de la métrique |
| :--- | :--- | :--- |
| **Qualité Intrinsèque** | **55%** | Basée sur la `Note_Globale` (agrégation critique/public). |
| **Fiabilité Technique** | **30%** | Mesure de la régularité (`10 - EcartType`). Punit sévèrement les animes ayant des épisodes "fillers" ou des chutes drastiques d'animation. |
| **Engagement** | **10%** | Basé sur le `Nb_Episodes` normalisé. Valorise la capacité d'une œuvre à maintenir un récit cohérent sur une longue durée. |
| **Statut de l'œuvre** | **5%** | Bonus attribué aux séries terminées (`Fini`) par rapport aux séries en cours, privilégiant les récits ayant une conclusion. |

### B. Segmentation Éditoriale
Les œuvres sont ensuite classées automatiquement selon des seuils statistiques :
* **Chef-d'œuvre** : Score exceptionnel, alliant qualité technique et narration.
* **Très bon** : Valeurs sûres du catalogue.
* **Risqué / Inégal** : Œuvres pouvant atteindre des sommets (ex: *Attack on Titan*) mais pénalisées par une irrégularité ou un format inachevé.
* **A éviter** : Œuvres ne répondant pas aux standards de qualité fixés.

## 3. Analyse Prédictive (Machine Learning)

Une composante d'Intelligence Artificielle a été intégrée pour comprendre les facteurs de succès d'un anime.

* **Modèle utilisé :** Random Forest Classifier (Forêt Aléatoire).
* **Objectif :** Prédire si un anime sera un "Hit" (Note supérieure à la médiane du marché) en se basant uniquement sur ses métadonnées, sans connaître sa note.
* **Variables analysées (Features) :**
    * **Studio d'animation** (ex: Madhouse, MAPPA, Kyoto Animation).
    * **Source originale** (Manga, Light Novel, Original).
    * **Genres** et **Nombre d'épisodes**.
* **Résultat :** Le modèle permet d'identifier l'importance critique du Studio et du format (Long vs Court) dans la probabilité de succès critique d'une œuvre.

## 4. Structure du Projet

Le dépôt est organisé comme suit :

* `app.py` : Application Web interactive (Streamlit). Moteur de recherche et affichage des fiches animes.
* `lemeilleuranime.ipynb` : Notebook de recherche. Contient l'ETL (Extract, Transform, Load), l'analyse exploratoire (EDA), la définition des algorithmes de scoring et l'entraînement du modèle ML.
* `animes_final_clean.csv` : Jeu de données traité, contenant les métriques calculées (`Regularite`, `Score_Complexe`, `Segment_Editorial`).
* `requirements.txt` : Liste des dépendances nécessaires à l'exécution.

## 5. Installation et Utilisation

Prérequis : Python 3.8 ou supérieur.

```bash
# 1. Cloner le dépôt
git clone [https://github.com/VOTRE_PSEUDO/recommandation-anime.git](https://github.com/VOTRE_PSEUDO/recommandation-anime.git)
cd recommandation-anime

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Mac/Linux
# venv\Scripts\activate   # Sur Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py