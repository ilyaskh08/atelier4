"""Commande en ligne pour prédire le risque de retard d'une livraison."""
import argparse
import json
import sys
from pathlib import Path

from logiai.predict import Predictor


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="logiai-predict")
    parser.add_argument("livraison", type=Path, help="Fichier JSON de la livraison")
    args = parser.parse_args(argv)

    if not args.livraison.is_file():
        print(f"Fichier introuvable : {args.livraison}", file=sys.stderr)
        return 1

    features = json.loads(args.livraison.read_text(encoding="utf-8"))
    prediction = Predictor().predict(features)
    alerte = " (ALERTE)" if prediction["alerte"] else ""
    probabilite = prediction["probabilite_retard"] * 100
    print(f"Probabilité de retard : {probabilite:.0f} %{alerte}")
    return 0
