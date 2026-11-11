# LogiAI : starter de la séance « Tester, sécuriser et appeler l'API »

Suite du TP précédent : l'API LogiAI existe. Aujourd'hui vous la testez pour la casser, vous la protégez par une clé, puis une page web l'appelle.

## Installation (une fois)

    python -m venv .venv
    .venv\Scripts\activate.bat        # Windows cmd  (PowerShell : .venv\Scripts\Activate.ps1)
    source .venv/bin/activate         # macOS / Linux
    pip install -r requirements.txt
    python -m logiai.dataset
    python -m logiai.train

## Vos clés (fichier .env, jamais dans Git)

    copy .env.example .env            # macOS / Linux : cp .env.example .env
    # puis ouvrez .env et choisissez vos deux clés

## Lancer

    python -m uvicorn logiai.api.main:app --reload          # l'API, port 8000
    python -m http.server 5500 --directory web              # la page web, dans un 2e terminal
    # ouvrez http://localhost:5500

### Avec Docker Compose

Depuis `starter2`, copiez `.env.example` vers `.env`, remplacez les deux clés
par vos propres valeurs, puis lancez :

    docker compose up -d --build

Ouvrez http://localhost:8080. Le modèle est généré pendant la construction de
l'image API. Pour arrêter les services :

    docker compose down

## Tester

    python -m pytest

## Sécurité et tests

L'API protège `/v1/predict` par une clé utilisateur ou administrateur et
réserve `/v1/model-info` à l'administrateur. `/health` reste publique. La page
web envoie la clé dans l'en-tête `X-API-Key` ; le CORS est limité aux origines
déclarées dans `logiai/config.py` (par défaut `localhost:5500` et
`127.0.0.1:5500`).

Les tests couvrent les entrées invalides, les bornes des livraisons et les
règles d'authentification :

    python -m pytest

Les clés réelles sont lues depuis `.env` et ne doivent jamais être ajoutées à
Git. `COMPTE_RENDU.md` contient les résultats et réponses de l'atelier.
