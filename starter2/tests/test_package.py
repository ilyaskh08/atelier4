from importlib.metadata import entry_points, version

from logiai.cli import main


def test_package_installe():
    assert version("logiai") == "0.1.0"


def test_commande_declaree():
    commandes = entry_points(group="console_scripts")
    assert any(
        commande.name == "logiai-predict"
        and commande.value == "logiai.cli:main"
        for commande in commandes
    )


def test_cli_fichier_absent(tmp_path, capsys):
    livraison = tmp_path / "absente.json"

    assert main([str(livraison)]) == 1
    assert "Fichier introuvable" in capsys.readouterr().err
