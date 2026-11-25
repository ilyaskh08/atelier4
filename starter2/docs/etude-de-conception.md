# Étude de conception — LogiAI

## Besoin

## Données

## Modèle et métriques

## Critères d'acceptation

## Cycle de vie

## Architecture

```text
data/livraisons.csv
        |
        v
logiai.dataset / logiai.train ---> models/model.joblib + model_info.json
                                              |
                         LOGIAI_HOME --------+
                            |
        +-------------------+---------------------+
        |                                         |
        v                                         v
Commande logiai-predict                    Package logiai
        |                                  (Predictor, config)
        +-------------------> package              ^
                                                  |
Page web ---> Nginx (conteneur web) ---> API FastAPI (conteneur API)
                                                  |
                                      package logiai / Predictor
```

Le code installé (package `logiai`) est partagé par la commande et l'API.
Les conteneurs web et API sont orchestrés par Docker Compose; les données et le
modèle restent dans `LOGIAI_HOME`, hors du package.

## Choix technologiques

## Risques et éthique

## Limites
