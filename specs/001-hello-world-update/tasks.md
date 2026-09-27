# Tasks: Intégration personnalisée Hello World et mises à jour GitHub

**Input**: Documents de `specs/001-hello-world-update/` : [plan.md](plan.md),
[spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md),
[contracts/](contracts/) et [quickstart.md](quickstart.md).

**Tests**: Inclus car la constitution du projet exige une couverture automatisée pour chaque
comportement nouveau. Les tâches de test précèdent le code qu'elles vérifient.

**Organization**: Deux phases de récit utilisateur : US1 fournit une intégration installable
depuis GitHub; US2 ajoute les mises à jour automatiques facultatives. Ce jalon exploratoire ne
pilote aucune prise; l'exception de portée est motivée et revue dans `spec.md`.

## Format: `[ID] [P?] [Story] Description`

- **[P]** : exécutable en parallèle après ses prérequis, sur des fichiers distincts.
- **[US1] / [US2]** : rattachement au récit utilisateur de la spec.
- Tous les chemins ci-dessous sont relatifs à la racine du dépôt.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Préparer le paquet et l'environnement de développement sans ajouter de comportement.

- [X] T001 Créer l'arborescence de l'intégration avec `custom_components/family_power_access/__init__.py`, `custom_components/family_power_access/translations/` et `tests/`, sans logique fonctionnelle.
- [X] T002 [P] Configurer `pyproject.toml` pour Python 3.14.2+, les fixtures pytest Home Assistant compatibles, Ruff et Pyright comme dépendances de développement uniquement.
- [X] T003 [P] Compléter `.gitignore` pour exclure `.venv/`, les caches Python et les artefacts de validation, en conservant l'exclusion `.ha-runtime/`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Définir le domaine, le manifeste local et les fixtures communes aux deux récits.

**⚠️ CRITICAL**: Terminer cette phase avant de réaliser les parcours US1 ou US2.

- [X] T004 Définir dans `custom_components/family_power_access/const.py` le domaine `family_power_access`, le nom `Family Power Access` et l'identifiant unique stable `family_power_access_hello_world`.
- [X] T005 [P] Créer `custom_components/family_power_access/manifest.json` avec `domain=family_power_access`, `name=Family Power Access`, `version=0.1.0`, `config_flow=true` et aucune dépendance Python à l'exécution; compléter les URL GitHub réelles avant la release en T017.
- [X] T006 [P] Préparer `tests/conftest.py` pour charger l'intégration personnalisée avec les fixtures Home Assistant, sans dépendre d'une connexion GitHub.

**Checkpoint**: Le domaine et l'environnement de validation sont prêts.

---

## Phase 3: User Story 1 — Installer et vérifier l'intégration (Priority: P1) 🎯 MVP

**Goal**: Installer une release `0.1.0` depuis un dépôt GitHub public et voir un capteur
« Hello World » stable dans Home Assistant.

**Independent Test**: Installer `0.1.0` via HACS dans Home Assistant Container, ajouter
l'intégration sans paramètre d'appareil, vérifier le capteur et son retour après redémarrage.

### Tests for User Story 1

- [X] T007 [P] [US1] Écrire dans `tests/test_config_flow.py` les cas d'ajout sans champ, d'entrée `data={}` avec schéma version `1` et de refus d'un second ajout; constater l'échec initial.
- [X] T008 [P] [US1] Écrire dans `tests/test_sensor.py` les cas de valeur `Hello World`, d'identifiant unique `family_power_access_hello_world`, de déchargement, de redémarrage et d'indépendance à GitHub; constater l'échec initial.
- [X] T009 [P] [US1] Écrire dans `tests/test_package.py` le contrôle d'un seul domaine `family_power_access`, de la version `0.1.0`, des traductions et du paquet HACS; constater l'échec initial.

### Implementation for User Story 1

- [X] T010 [P] [US1] Implémenter `custom_components/family_power_access/config_flow.py` avec un écran d'ajout sans champ, une entrée unique à données vides et un arrêt « déjà configuré » pour un second ajout.
- [X] T011 [P] [US1] Implémenter `custom_components/family_power_access/__init__.py` pour charger l'entrée de configuration, transmettre la plateforme capteur et la décharger proprement.
- [X] T012 [P] [US1] Implémenter `custom_components/family_power_access/sensor.py` avec un seul capteur texte `Hello World`, un identifiant unique stable et aucune requête réseau ni interrogation périodique.
- [X] T013 [P] [US1] Fournir les libellés de configuration et du capteur dans `custom_components/family_power_access/strings.json`, `custom_components/family_power_access/translations/en.json` et `custom_components/family_power_access/translations/fr.json`.
- [X] T014 [P] [US1] Créer `hacs.json` à la racine avec le nom de l'intégration et `hide_default_branch: true`, pour limiter le parcours d'installation aux releases publiées.
- [X] T015 [P] [US1] Créer `brand/icon.png` au format et à la taille attendus par HACS pour l'intégration personnalisée.
- [X] T016 [US1] Documenter dans `README.md` les prérequis HACS, l'ajout du dépôt personnalisé après la première release stable, le montage local avant release, l'ajout dans Home Assistant et le capteur attendu.
- [X] T017 [US1] Préparer le dépôt GitHub public puis renseigner son URL réelle, sa documentation, son suivi de problèmes et ses mainteneurs dans `custom_components/family_power_access/manifest.json` et `README.md`; obtenir l'autorisation requise avant la publication publique.
- [X] T018 [US1] Préparer et publier, après validation, la release stable `0.1.0` dont le tag correspond exactement à `custom_components/family_power_access/manifest.json`; consigner l'URL de release et la compatibilité dans `README.md`.
- [X] T019 [US1] Exécuter le parcours local puis l'installation HACS `0.1.0` de `specs/001-hello-world-update/quickstart.md` dans une configuration Container séparée, et y consigner les résultats et les mesures SC-001/SC-002.

**Checkpoint**: US1 est démontrable seule, sans automatisation de mise à jour.

---

## Phase 4: User Story 2 — Recevoir et appliquer une mise à jour (Priority: P1)

**Goal**: Faire suivre les releases stables par HACS et proposer une automatisation activée par
le parent, ciblant seulement l'entité de mise à jour du dépôt et sans redémarrage implicite.

**Independent Test**: Avec `0.1.0` installée, publier `0.1.1`, activer l'automatisation, vérifier
le téléchargement HACS, l'état « Pending restart », puis la version active après un redémarrage
choisi par le parent. Désactiver l'automatisation et vérifier qu'une release ultérieure n'est pas
installée automatiquement.

### Tests for User Story 2

- [X] T020 [US2] Écrire dans `tests/test_auto_update_blueprint.py` des cas pour la cible `update` choisie, l'heure locale proposée `21:00`, l'installation seulement si une mise à jour existe, l'absence de version explicite et le caractère facultatif du blueprint; simuler aussi l'échec de `update.install` et vérifier la trace d'erreur, l'absence d'autre cible et de redémarrage; constater l'échec initial.

### Implementation for User Story 2

- [X] T021 [US2] Créer `blueprints/automation/family_power_access_auto_update.yaml` avec un sélecteur d'entité `update`, une heure configurable par défaut à `21:00`, une condition de mise à jour disponible et l'action `update.install` sur cette seule cible; laisser une erreur d'action visible dans la trace Home Assistant, sans autre cible ni redémarrage, et ne créer aucune automatisation active par défaut.
- [X] T022 [US2] Ajouter dans `README.md` l'import du blueprint par URL, son activation et sa désactivation, le commutateur HACS des préversions sur OFF, la distinction version téléchargée/version active, l'état « Pending restart » et la réinstallation stable avant redémarrage après un téléchargement interrompu.
- [X] T023 [US2] Préparer `0.1.1` en synchronisant le numéro de `custom_components/family_power_access/manifest.json` avec le tag stable, puis publier la release GitHub après validation et consigner ses notes dans `README.md`.
- [X] T024 [US2] Suivre `specs/001-hello-world-update/quickstart.md` dans l'instance HACS isolée pour vérifier la découverte de `0.1.1` après actualisation réussie du dépôt, l'installation automatique activée, la cible unique, la version téléchargée avant redémarrage puis active après redémarrage; consigner les résultats.
- [X] T025 [US2] Clôture acceptée avec écarts consignés : le parcours préversion exclue, l'indisponibilité GitHub et le téléchargement interrompu n'ont pas été simulés; l'automatisation a été désactivée après le test et l'erreur `update.install` est couverte par un test de trace. La procédure de réinstallation stable figure dans `README.md`.

**Checkpoint**: Les deux récits sont vérifiés; le parent peut activer ou désactiver les mises à
jour automatiques sans installer de préversion ni provoquer un redémarrage silencieux.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Vérifier l'ensemble du comportement et la cohérence de la livraison.

- [X] T026 Exécuter les contrôles Ruff, Pyright et pytest définis dans `pyproject.toml` et le parcours de `specs/001-hello-world-update/quickstart.md`; consigner les résultats et les limites observées dans `specs/001-hello-world-update/quickstart.md`.
- [X] T027 Relire `README.md` et `specs/001-hello-world-update/quickstart.md` contre FR-001 à FR-011, les contrats et l'exception exploratoire de `specs/001-hello-world-update/spec.md`; corriger les instructions d'installation, de mise à jour ou de récupération qui ne correspondent pas au comportement livré.

## Dependencies & Execution Order

### Phase Dependencies

```text
Setup (T001–T003) → Foundational (T004–T006) → US1 (T007–T019) → documentation/release US2 (T022–T023) → validation US2 (T024–T025) → Polish (T026–T027)
                                         └──────────────→ blueprint US2 (T020–T021)
```

- T002 précède T006. T004–T006 précèdent les tests des récits.
- T007–T009 précèdent T010–T015; les tests échouent d'abord, puis passent après l'implémentation.
- T016–T018 précèdent la validation HACS T019. Le dépôt public et les releases sont des actions
  externes : préparer leur contenu, puis obtenir l'autorisation nécessaire à la publication.
- T020 précède T021. Le test et le blueprint T020–T021 peuvent être préparés dès la fin de la
  phase Foundational. T022 attend la documentation US1 dans `README.md`; la validation T024–T025
  attend la release `0.1.0` de US1.
- T023 attend T018 et les fichiers du blueprint; T024–T025 attendent T023.
- T026–T027 concluent les récits et ne remplacent pas leurs contrôles indépendants.

### Parallel Opportunities

- Après Setup, T004, T005 et T006 touchent des fichiers distincts et peuvent avancer en
  parallèle, sous réserve de la configuration de développement T002 pour T006.
- Après Foundation, T007–T009 vérifient des contrats distincts et peuvent être écrits en
  parallèle. Après leurs échecs initiaux, T010–T015 touchent des fichiers distincts.
- Après Foundation, T020–T021 peuvent progresser pendant US1 sur des fichiers distincts;
  T022 attend T016–T017 car ces tâches éditent aussi `README.md`. T024–T025 restent dépendantes
  de la première release installée via HACS.

### Parallel Example: User Story 1

```text
T007 [US1] tests/test_config_flow.py
T008 [US1] tests/test_sensor.py
T009 [US1] tests/test_package.py

Puis, après les échecs attendus :
T010 [US1] custom_components/family_power_access/config_flow.py
T011 [US1] custom_components/family_power_access/__init__.py
T012 [US1] custom_components/family_power_access/sensor.py
T013 [US1] custom_components/family_power_access/strings.json et translations/
T014 [US1] hacs.json
T015 [US1] brand/icon.png
```

### Parallel Example: User Story 2

```text
T020 [US2] tests/test_auto_update_blueprint.py
Puis T021 [US2] blueprints/automation/family_power_access_auto_update.yaml
La documentation T022 [US2] README.md suit les modifications US1 du même fichier.
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Terminer Setup et Foundational.
2. Écrire les contrôles US1, observer leurs échecs, puis construire l'intégration.
3. Préparer le dépôt et la release `0.1.0`, demander l'autorisation requise pour publier.
4. Installer dans l'instance HACS séparée et vérifier US1 sans automatisation.

### Incremental Delivery

1. Livrer US1 comme socle Hello World installable depuis une release GitHub stable.
2. Ajouter le blueprint US2 et le guide de récupération sans changer le capteur.
3. Publier `0.1.1` après validation, puis vérifier l'installation automatique facultative dans
   l'instance HACS séparée.
4. Effectuer les contrôles finaux et conserver les résultats dans le quickstart.

## Notes

- Les tests T007, T008 et T020 existent et passent après implémentation. Leur échec initial
  (« phase rouge ») n'a pas été enregistré séparément; cette partie du processus TDD ne peut
  pas être attestée rétroactivement.
- Les scénarios T025 de préversion, d'indisponibilité GitHub et de reprise après téléchargement
  interrompu n'ont pas été provoqués dans l'instance; leur report est accepté à la clôture.

- Chaque tâche `[P]` possède des fichiers propres; les tâches de publication et de validation
  HACS dépendent des releases et ne sont pas parallélisées avec elles.
- Aucun script de mise à jour autonome dans l'intégration : HACS gère les releases et
  l'automatisation Home Assistant déclenche leur installation.
- Le projet ne promet pas de restauration automatique des fichiers après un échec de
  téléchargement HACS; la réinstallation stable avant redémarrage est documentée.

## Clôture de la spec 001

Le 27 septembre 2026, l'utilisateur a accepté de clore cette spécification sans exécuter les
scénarios non bloquants ci-dessus. SC-001 n'a pas été chronométré formellement. Les versions
stables `0.1.0` et `0.1.1`, le parcours HACS, le capteur après redémarrage et l'absence de
redémarrage automatique ont été vérifiés. Aucun travail supplémentaire n'est requis pour
rouvrir cette spec; les scénarios laissés de côté pourront être repris dans une future spec si
nécessaire.
