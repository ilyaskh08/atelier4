# Compte rendu : tester, sécuriser et appeler l'API LogiAI

**Noms :** à compléter  **Groupe :** à compléter

## 1. Casser son API (activité 1)

| Cas | Requête (corps ou URL) | Prévu | Obtenu |
|---|---|---:|---:|
| champ manquant | `POST /v1/predict`, sans `poids_kg` | 422 | 422 |
| valeur absurde | `POST /v1/predict`, `poids_kg=99999` | 422 | 422 |
| texte au lieu d'un nombre | `POST /v1/predict`, `distance_km="loin"` | 422 | 422 |
| champ en trop | `POST /v1/predict`, champ supplémentaire `couleur` | 422 | 422 |
| mauvaise route | `POST /route-inconnue` | 404 | 404 |

- Une requête acceptée alors qu'elle devait être refusée ? Oui : une heure de
  départ à 24 et un nombre négatif d'arrêts étaient acceptés avant correction.

## 2. Les 2 bugs (activité 2)

| Bug | Test qui l'a révélé | Comportement avant | Correction |
|---|---|---|---|
| `heure_depart` autorisait 24 | `test_valeurs_limites`, `heure_depart=24` | 200 au lieu de 422 | borne maximale fixée à 23 |
| `nb_arrets` acceptait une valeur négative | `test_valeurs_limites`, `nb_arrets=-1` | 200 au lieu de 422 | ajout de la borne minimale `ge=0` |

- Sortie finale de `python -m pytest -q` : **53 passed**.

## 3. La clé API (sprint 1)

Fonction `verify_api_key()` :

```python
def verify_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """Authentification : renvoie le rôle ('user' ou 'admin') ou lève une 401."""
    if _egal(x_api_key, config.ADMIN_KEY):
        return "admin"
    if _egal(x_api_key, config.API_KEY):
        return "user"

    detail = "Clé API manquante" if x_api_key is None else "Clé API invalide"
    raise HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "ApiKey"},
    )
```

| Requête | Code obtenu |
|---|---:|
| `/v1/predict` sans clé | 401 |
| `/v1/predict` fausse clé | 401 |
| `/v1/predict` clé utilisateur | 200 |
| `/v1/model-info` clé utilisateur | 403 |
| `/v1/model-info` clé administrateur | 200 |
| `/health` sans clé | 200 |

- `.env` est ignoré par Git via `.gitignore` et ne doit pas être ajouté à un
  commit. Les tests utilisent uniquement des clés fictives.

## 4. Le client web (sprint 2)

- Le `fetch` envoie la livraison en `POST` JSON et transmet la clé dans
  l'en-tête `X-API-Key`. La page n'enregistre pas la clé.
- Résultats attendus : une livraison valide affiche la probabilité et son état
  d'alerte ; une pluie de 500 mm affiche l'erreur de validation 422 ; une
  mauvaise clé affiche une erreur d'authentification 401.
- Vérification CORS automatisée avec une requête preflight : l'origine
  `http://localhost:5500` reçoit 200 et l'en-tête
  `Access-Control-Allow-Origin`; `http://localhost:5501` reçoit 400 sans cet
  en-tête. Dans un navigateur, l'échec de `fetch` sur le port 5501 est signalé
  dans la console comme une erreur CORS; `curl` fonctionne car il n'applique
  pas la politique CORS du navigateur.
- La clé transmise est visible dans les outils de développement, onglet
  Network, en-têtes de la requête `predict` (`X-API-Key`). Une clé écrite dans
  le JavaScript serait également visible à tous les visiteurs du site.

## 5. Questions de compréhension

1. **Quelle différence entre 401, 403 et 422 ?**
   401 signifie que l'appelant n'est pas authentifié; 403 signifie qu'il est
   authentifié mais n'a pas le rôle autorisé; 422 signifie que les données
   envoyées ne respectent pas le schéma de validation.

2. **Pourquoi la clé n'est-elle ni dans le code ni dans Git ?**
   Une clé intégrée au code ou à l'historique Git peut être copiée et utilisée
   par d'autres personnes. Elle est configurée dans `.env`, qui est ignoré par
   Git.

3. **Pourquoi comparer avec `compare_digest` plutôt qu'avec `==` ?**
   `secrets.compare_digest` évite une comparaison dont le temps varierait selon
   la longueur du préfixe correct, ce qui réduit les fuites d'information par
   mesure du temps.

4. **Pourquoi `curl` fonctionne-t-il alors que la page du port 5501 est bloquée ?**
   CORS est une restriction appliquée par les navigateurs aux requêtes initiées
   par une page web. `curl` n'applique pas cette politique.

5. **Pourquoi la validation faite par le navigateur ne remplace-t-elle pas celle de l'API ?**
   Le client peut être modifié ou contourné et une requête peut être envoyée
   sans passer par le formulaire. L'API doit donc valider elle-même chaque
   entrée reçue.

## 6. Lien de la pull request

À compléter après la publication de la branche sur GitHub.
