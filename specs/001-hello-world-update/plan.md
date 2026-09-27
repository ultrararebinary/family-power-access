# Implementation Plan: Intégration personnalisée Hello World et mises à jour GitHub

**Branch**: `main` (identifiant SpecKit : `001-hello-world-update`) | **Date**: 2026-09-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-hello-world-update/spec.md`

## Summary

Créer un jalon exploratoire d'intégration personnalisée Home Assistant, ajoutable depuis
l'interface, qui expose un
capteur « Hello World » indépendant du réseau. Distribuer la version `0.1.0` dans un dépôt
GitHub public compatible HACS. HACS suit les releases stables et expose son entité de mise à
jour; un blueprint Home Assistant, importé et activé par le parent, installe les mises à jour à
une heure choisie. Home Assistant indique quand un redémarrage est nécessaire et ne le lance
pas automatiquement. Les décisions et leurs sources sont dans [research.md](research.md).

## Technical Context

**Language/Version**: Python 3.14.2 ou ultérieur, livré avec Home Assistant 2026.9.3; version
initiale de l'intégration `0.1.0`.

**Primary Dependencies**: Home Assistant Core pour l'intégration; HACS pour installer et suivre
les releases. Aucune dépendance Python supplémentaire à l'exécution. Dépendances de développement
limitées à pytest, ses fixtures Home Assistant compatibles, Ruff et un vérificateur de types.

**Storage**: Une entrée de configuration Home Assistant sans secret ni donnée d'enfant. L'état
de l'installation et de l'automatisation reste géré par Home Assistant et HACS.

**Testing**: Vérifications ciblées du flux de configuration, de l'entité et de sa persistance au
redémarrage avec les fixtures Home Assistant; contrôle du blueprint lorsque `update.install`
réussit, n'est pas appelé ou échoue; lint et types. Validation réelle du chemin HACS
0.1.0 → 0.1.1 dans une seconde configuration Container dédiée aux releases.

**Target Platform**: Home Assistant Container 2026.9.3 sur Apple silicon avec Apple `container`;
distribution sous `custom_components/family_power_access/`.

**Project Type**: Intégration personnalisée Home Assistant, un dépôt GitHub public et un
blueprint d'automatisation facultatif.

**Performance Goals**: Installation et ajout en moins de 5 minutes une fois HACS configuré;
capteur visible au plus tard 2 minutes après l'ajout; nouvelle release stable proposée après
l'actualisation réussie des métadonnées HACS lorsque GitHub est accessible. La cadence des
contrôles HACS n'est pas sous le contrôle de cette intégration.

**Constraints**: Le capteur reste disponible hors ligne. Les préversions sont ignorées. Le
réglage automatique est désactivé par défaut. Aucun redémarrage automatique de Home Assistant,
aucune modification de Home Assistant Core ni accès à un appareil Zigbee. Une interruption
pendant le téléchargement HACS nécessite une réinstallation avant redémarrage.

**Scale/Scope**: Une entrée de configuration, une entité capteur, un dépôt HACS, une entité de
mise à jour HACS et au plus une automatisation facultative. Aucun profil enfant, calendrier,
quota ou historique d'utilisation dans cette phase.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe ou contrainte | Décision vérifiable | Avant recherche | Après conception |
| --- | --- | --- | --- |
| I. Integration-First | Emballage conforme; demande enfant/clavier différée car aucune prise n'est pilotée | Exception documentée | Exception revue |
| II. Native Home Assistant and Zigbee APIs | Flux de configuration et capteur natifs; aucun accès Zigbee dans cette phase; HACS gère les releases | Pass | Pass |
| III. Parent-Controlled Authorization and Quotas | Calendrier, quota et choix Zigbee différés; aucune prise énergisée dans ce jalon | Exception documentée | Exception revue |
| IV. Secure Handling and Child Privacy | Aucun code ou donnée d'enfant dans ce jalon; protection future différée | Exception documentée | Exception revue |
| V. Parent Auditability and Verified Behavior | Audit enfant différé; couverture automatisée des chemins normaux et d'erreur du comportement livré | Exception documentée | Exception revue |
| VI. Minimal and Maintainable | Réutilisation de HACS et des automatisations Home Assistant; aucune logique de mise à jour autonome dans l'intégration | Pass | Pass |
| Architecture and Runtime Constraints | Image officielle Container, source sous `/config/custom_components`, état hors Git, releases GitHub stables | Pass | Pass |
| Development Workflow | Spec, recherche, plan, modèle, contrats et tâches précèdent le code; l'exception de jalon est motivée dans la spec et revue | Exception documentée | Exception revue |

L'[exception de portée](spec.md) du jalon Hello World est limitée à une version qui ne pilote
aucune prise; les obligations finales restent en vigueur avant toute fonction Zigbee. La
recherche a montré que HACS supprime le dossier local avant un téléchargement. La spec et le
guide décrivent donc une réinstallation de la dernière release stable avant tout redémarrage,
sans promettre de restauration automatique. Les erreurs d'automatisation restent consultables
dans Home Assistant; elles ne sont pas transformées en notification propre à l'intégration.

## Project Structure

### Documentation (this feature)

```text
specs/001-hello-world-update/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── home-assistant.md
│   └── github-releases.md
├── checklists/
│   └── requirements.md
└── tasks.md                 # Créé lors de la phase speckit-tasks
```

### Source Code (repository root)

```text
custom_components/
└── family_power_access/
    ├── __init__.py
    ├── manifest.json
    ├── const.py
    ├── config_flow.py
    ├── sensor.py
    ├── strings.json
    └── translations/
        ├── en.json
        └── fr.json
brand/
└── icon.png
blueprints/
└── automation/
    └── family_power_access_auto_update.yaml
hacs.json
README.md
pyproject.toml
tests/
├── conftest.py
├── test_config_flow.py
├── test_sensor.py
├── test_package.py
└── test_auto_update_blueprint.py
```

**Structure Decision**: La racine du dépôt contient les métadonnées HACS, la documentation,
l'icône et le blueprint importable par URL. Tous les fichiers nécessaires à l'exécution de
l'intégration se trouvent dans un seul dossier sous `custom_components`, conformément à HACS.
Les tests restent dans le dépôt et ne sont pas livrés comme code de l'intégration. Les
interfaces prévues sont décrites dans [contracts/home-assistant.md](contracts/home-assistant.md)
et [contracts/github-releases.md](contracts/github-releases.md).
