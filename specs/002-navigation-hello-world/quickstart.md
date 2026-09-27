# Quickstart de validation : navigation Family Power Access

Ce guide valide les scénarios de [spec.md](spec.md) et le [contrat UI](contracts/navigation.md)
après implémentation. La spec 001 fournit déjà le capteur `Hello World` et le parcours HACS.

## Prérequis

- Home Assistant Container 2026.9.3 avec Family Power Access installé et configuré.
- Une instance de développement où `custom_components/` du dépôt est monté dans `/config`,
  ou une instance HACS de validation après publication d'une release contenant cette page.
- Un navigateur connecté à Home Assistant avec accès à sa navigation.

## 1. Vérifier l'entrée et la page

1. Démarrer l'instance de développement (`container start homeassistant` si elle existe déjà),
   puis ouvrir `http://127.0.0.1:8123/`.
2. Ajouter Family Power Access depuis **Paramètres → Appareils et services** si l'intégration
   n'est pas encore configurée.
3. Vérifier qu'une seule entrée **Family Power Access** figure dans la barre latérale.
4. La sélectionner et chronométrer le délai jusqu'à l'affichage de `Hello World` : le résultat
   attendu est inférieur à 2 secondes.
5. Replier puis rouvrir la navigation, ainsi que réduire la largeur de la fenêtre; l'entrée
   et le texte doivent rester accessibles et lisibles.

## 2. Vérifier le cycle de vie

1. Ouvrir une autre page Home Assistant, puis revenir par l'entrée Family Power Access :
   `Hello World` doit toujours s'afficher.
2. Recharger le navigateur puis l'entrée de configuration; vérifier qu'il n'y a toujours
   qu'une entrée de navigation et qu'une page fonctionnelle.
3. Redémarrer l'instance de validation; vérifier que la page et le capteur `Hello World`
   existant reviennent.
4. Dans l'instance de validation, décharger ou supprimer l'entrée de configuration : l'entrée
   de navigation doit disparaître. La réajouter pour restaurer le parcours.

## 3. Contrôles de qualité

Après implémentation, depuis la racine du dépôt :

```sh
.venv/bin/python -m pytest tests -q
.venv/bin/python -m ruff check custom_components tests
.venv/bin/python -m ruff format --check custom_components tests
.venv/bin/python -m pyright --pythonpath .venv/bin/python custom_components
```

Vérifier notamment l'enregistrement unique du panneau, son retrait au déchargement, le
contenu du module et le maintien des tests de la spec 001. Dans le conteneur, exécuter
`python3 -m homeassistant --script check_config --config /config` pour contrôler la
configuration.

## 4. Vérifier la distribution HACS

Après publication de la release stable prévue pour cette spec, actualiser le dépôt Family
Power Access dans HACS sur l'instance isolée (`http://127.0.0.1:8125/`), télécharger la
nouvelle version et redémarrer Home Assistant au moment choisi. Vérifier que l'entrée de
navigation et la page sont disponibles et que la version active correspond au manifeste de
la release. La configuration et le capteur existants doivent rester présents.

## Résultats

Validation locale effectuée le 27 septembre 2026 avec le code du panneau et l'instance
Home Assistant Container `family-power-release` (port 8125) :

- L'entrée **Family Power Access** s'affiche dans la navigation et ouvre `/family-power-access`;
  `Hello World` est visible en moins de 2 secondes après le clic.
- En émulation responsive à 400 px, le titre reste lisible dans la page. La barre latérale
  repliée affiche toujours l'entrée avec son icône.
- L'action **Recharger** de l'entrée confirme le rechargement; la page reste accessible.
- Après l'arrêt puis le redémarrage du conteneur, la page et l'entrée reviennent. Le capteur
  `Hello World` est toujours présent (1 entité dans l'entrée de l'intégration).
- **Désactiver** retire l'entrée de la navigation; **Activer** la restaure avec l'entité.
- `check_config` dans le conteneur se termine sans erreur.
- Tests : `18 passed`; Ruff lint et format réussis; Pyright `0 errors, 0 warnings`.
- `uv lock --check --offline` réussit. La résolution en ligne de `uv lock` n'était pas
  disponible (DNS vers PyPI bloqué); seule la version du paquet racine a été ajustée dans
  `uv.lock`.

Validation HACS de la release `0.2.0` : à consigner après publication et installation sur
l'instance isolée.
