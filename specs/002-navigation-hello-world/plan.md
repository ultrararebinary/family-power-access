# Implementation Plan: Navigation Family Power Access

**Branch**: `main` (identifiant SpecKit : `002-navigation-hello-world`) | **Date**: 2026-09-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-navigation-hello-world/spec.md`

## Summary

Ajouter à l'intégration existante une entrée « Family Power Access » dans la navigation Home
Assistant. Elle ouvre une page locale contenant uniquement « Hello World ». L'intégration
enregistre le panneau lorsque son entrée de configuration est chargée et le retire au
déchargement. Un petit module frontend livré dans le dossier HACS fournit la page, sans
nouvelle donnée utilisateur ni dépendance externe. Les choix et alternatives sont détaillés
dans [research.md](research.md).

## Technical Context

**Language/Version**: Python 3.14.2+ pour l'intégration, Home Assistant 2026.9.3 pour la
validation, JavaScript ES2015+ natif pour le panneau. Version actuelle du paquet `0.1.1`;
release mineure `0.2.0` prévue lorsque cette fonctionnalité sera implémentée et vérifiée.

**Primary Dependencies**: Composants Home Assistant `panel_custom`, `frontend` et `http`;
`panel_custom` sera déclaré comme dépendance et entraîne les deux autres. Le groupe de
développement utilisera aussi le paquet officiel `home-assistant-frontend==20260826.7` pour
charger le frontend pendant les tests; il ne s'agit pas d'une exigence d'exécution de
l'intégration. HACS reste le canal de distribution.

**Storage**: Aucune nouvelle donnée persistante. L'entrée de configuration unique de la
spec 001 reste la source du cycle de vie. Le panneau et la route statique sont enregistrés
en mémoire dans Home Assistant.

**Testing**: Fixtures pytest Home Assistant existantes pour l'enregistrement unique du
panneau, sa configuration, le chemin statique, le déchargement/rechargement et le maintien du
capteur. Parcours navigateur réel dans Home Assistant Container pour le clic, le texte, la
fenêtre étroite et le redémarrage. Ruff, Pyright et `check_config` restent les contrôles de
qualité du projet.

**Target Platform**: Home Assistant Container 2026.9.3 sur Apple silicon avec Apple
`container`, installation sous `custom_components/family_power_access/`, navigation dans le
frontend Home Assistant sur ordinateur et appareil mobile.

**Project Type**: Intégration personnalisée Home Assistant avec panneau frontend local.

**Performance Goals**: Le texte « Hello World » est visible moins de 2 secondes après la
sélection de l'entrée dans l'instance de validation. Le module ne fait aucun appel externe
pour afficher son contenu.

**Constraints**: Une seule entrée de navigation au chemin `/family-power-access`; retrait au
déchargement; utilisateurs Home Assistant connectés sans privilège administrateur additionnel;
aucun contrôle Zigbee ou traitement de données enfant; capteur actuel inchangé; pas de
modification de Home Assistant Core, de configuration YAML utilisateur ni de redémarrage
automatique.

**Scale/Scope**: Une entrée de configuration, un panneau, un module JavaScript statique et le
capteur déjà existant. Aucun tableau de bord ou stockage nouveau.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe ou contrainte | Décision vérifiable | Avant recherche | Après conception |
| --- | --- | --- | --- |
| I. Integration-First | Le panneau est livré dans `custom_components/family_power_access/` sans modifier Core; pilotage Zigbee différé dans l'[exception de la spec](spec.md#exception-de-portée-constitutionnelle--jalon-dinterface) | Exception documentée | Exception revue |
| II. Native Home Assistant and Zigbee APIs | Enregistrement du panneau par les composants `panel_custom`/`frontend` et du module par l'API HTTP asynchrone; aucun accès Zigbee | Pass | Pass |
| III. Parent-Controlled Authorization and Quotas | Aucun appareil n'est alimenté; calendrier, quotas et modèles Zigbee sont différés selon la spec | Exception documentée | Exception revue |
| IV. Secure Handling and Child Privacy | Le module est statique et ne contient ni code personnel ni donnée enfant; les droits de la page suivent Home Assistant | Pass | Pass |
| V. Parent Auditability and Verified Behavior | Aucun journal enfant dans ce jalon; tests du panneau, de son retrait, des doublons et de l'erreur de chargement, plus validation navigateur | Exception documentée | Exception revue |
| VI. Minimal and Maintainable | Un module JavaScript natif sans nouvelle dépendance; capteur actuel conservé; version et compatibilité annoncées dans la release | Pass | Pass |
| Architecture and Runtime Constraints | Validation dans Home Assistant Container et distribution depuis une release GitHub stable HACS; données de test hors dépôt | Pass | Pass |
| Development Workflow | Spec, recherche, modèle, contrat, plan et tâches précèdent l'implémentation; exception limitée explicitée dans la spec | Pass | Pass |

L'exception de portée est nécessaire uniquement parce que ce jalon vérifie la navigation et
ne pilote aucune prise. La spec 001 conserve le parcours HACS stable; cette conception ne
change pas le mécanisme de mise à jour. La recherche confirme le modèle de panneau Home
Assistant et l'exposition asynchrone de la ressource locale.

## Project Structure

### Documentation (this feature)

```text
specs/002-navigation-hello-world/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── navigation.md
├── checklists/
│   └── requirements.md
└── tasks.md                 # À créer avec speckit-tasks
```

### Source Code (repository root)

```text
custom_components/family_power_access/
├── __init__.py              # Cycle de vie de l'entrée et du panneau
├── const.py                  # Domaine et chemin de panneau
├── manifest.json            # Version et dépendance Home Assistant
├── frontend/
│   └── panel.js             # Élément personnalisé affichant Hello World
├── sensor.py                # Capteur existant, comportement conservé
└── translations/            # Traductions existantes
tests/
├── test_panel.py            # Contrat du panneau et cycle de vie
├── test_sensor.py           # Régression du capteur existant
└── test_package.py          # Contrôle de version et du paquet HACS
README.md                   # Installation, accès par la navigation et release
pyproject.toml              # Version du projet synchronisée avec le manifeste
uv.lock                     # Verrou de développement synchronisé
```

**Structure Decision**: La page est distribuée avec l'unique intégration HACS existante.
`async_setup` enregistrera le chemin statique une fois par processus; `async_setup_entry`
enregistrera le panneau après chargement de l'entrée, et `async_unload_entry` le retirera.
Le chemin `/family-power-access` est réservé au projet; une collision doit échouer clairement
plutôt que remplacer un autre panneau. Le contrat est dans [navigation.md](contracts/navigation.md)
et la validation prévue dans [quickstart.md](quickstart.md).

Le slug passé à Home Assistant pour ce panneau est `family-power-access`, sans barre initiale;
son URL visible dans le navigateur est `/family-power-access`.
