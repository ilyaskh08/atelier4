"""Authentification par clé d'API : qui êtes-vous ? et avez-vous le droit ?"""
import secrets

from fastapi import Depends, Header, HTTPException

from logiai import config


def _egal(a: str | None, b: str | None) -> bool:
    """Comparaison en temps constant. Une clé non configurée n'est jamais valide."""
    if not a or not b:
        return False
    return secrets.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def verify_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """Authentification : renvoie le rôle ('user' ou 'admin') ou lève une 401.

    Une clé non configurée ne peut pas authentifier un utilisateur.
    """
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


def require_admin(role: str = Depends(verify_api_key)) -> str:
    """Autorisation : réservé aux administrateurs.

    L'authentification est faite par verify_api_key ; cette dépendance vérifie le rôle.
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé à l'administrateur")
    return role
