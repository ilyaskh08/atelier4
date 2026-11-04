# ADR 003 : sécurité de l'API LogiAI

## Décision 1 : où transmettre la clé (en-tête, URL ou corps) ?
- Choix : l'en-tête HTTP `X-API-Key`.
- Une clé dans l'URL apparaîtrait dans l'historique du navigateur, les journaux
  du serveur et les outils d'analyse. Une clé dans le corps serait moins
  pratique à appliquer uniformément aux routes et ne conviendrait pas aux
  requêtes qui n'ont pas de corps. En HTTPS, l'en-tête permet aux différents
  clients de transmettre la clé sans l'intégrer à l'URL.

## Décision 2 : quelles origines autoriser (CORS) ? Une liste précise ou « * » ?
- Choix : une liste précise définie dans `config.ALLOWED_ORIGINS`.
- Autoriser `*` ouvrirait l'accès navigateur à toute origine et retirerait la
  restriction attendue pour l'interface servie sur `localhost:5500`. Une liste
  précise demande une mise à jour si l'interface change d'origine, mais limite
  les sites pouvant appeler l'API depuis un navigateur.
