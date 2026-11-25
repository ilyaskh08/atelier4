# ADR 005 : empaquetage de LogiAI

## Versions des dépendances
Le projet accepte des versions compatibles avec `>=` plutôt que de figer
chaque version avec `==`. Cela facilite les correctifs et mises à jour, au prix
d'une reproductibilité stricte moindre; `==` imposerait des mises à jour
manuelles pour profiter des corrections et compatibilités futures.

## Emplacement du modèle
Le modèle reste hors du package, dans `models/` sous `LOGIAI_HOME`. Le wheel
reste léger et le modèle peut être remplacé sans republier le code, mais
l'installation seule ne suffit pas : il faut fournir le modèle et configurer
son emplacement. L'inclure rendrait l'installation autonome, mais alourdirait
le wheel et lierait la mise à jour du modèle à une nouvelle version du package.
