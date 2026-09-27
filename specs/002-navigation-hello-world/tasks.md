# Tasks: Navigation Family Power Access

**Input**: Documents de conception dans `specs/002-navigation-hello-world/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contrat UI](contracts/navigation.md) et
[quickstart.md](quickstart.md)

**Tests**: Requis par le principe V de la constitution pour tout changement de comportement.

**Organization**: La spec contient un seul parcours P1, réalisable et vérifiable sans fonction
Zigbee ni nouveau stockage.

## Format: `[ID] [P?] [Story] Description`

- **[P]** : travail parallélisable sur des fichiers distincts, sans dépendance inachevée.
- **[Story]** : rattachement à la User Story de [spec.md](spec.md).
- Chaque tâche ci-dessous nomme les chemins concernés.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Préparer le code source et les fixtures du panneau sans changer le comportement
de l'intégration existante.

- [X] T001 Créer le dossier `custom_components/family_power_access/frontend/` qui contiendra le module distribué par HACS.
- [X] T002 [P] Ajouter dans `pyproject.toml` et `uv.lock` le paquet de développement officiel `home-assistant-frontend==20260826.7` correspondant à Home Assistant 2026.9.3, puis étendre `tests/conftest.py` pour charger `frontend`, `panel_custom` et conserver `enable_custom_integrations`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Fixer les identifiants et dépendances dont dépendent la page et ses tests.

**⚠️ CRITICAL**: Terminer cette phase avant les tâches de la User Story.

- [X] T003 [P] Déclarer `panel_custom` dans les dépendances Home Assistant de `custom_components/family_power_access/manifest.json`, sans nouvelle exigence Python ni changement de la version `0.1.1` à ce stade.
- [X] T004 [P] Définir dans `custom_components/family_power_access/const.py` le slug de panneau `family-power-access` (URL visible `/family-power-access`), le nom d'élément `family-power-access-panel`, l'URL du module `/api/family_power_access/frontend/panel.js` et l'icône `mdi:power-plug`, en réutilisant le titre existant `Family Power Access`.

**Checkpoint**: La structure et les identifiants du panneau sont prêts pour la User Story.

---

## Phase 3: User Story 1 — Ouvrir Family Power Access depuis la navigation (Priority: P1) 🎯 MVP

**Goal**: Après configuration de l'intégration, afficher une entrée de navigation unique
qui ouvre une page locale `Hello World`; retirer cette entrée au déchargement.

**Independent Test**: Dans Home Assistant Container, ajouter l'intégration, sélectionner
« Family Power Access » dans la barre latérale et voir `Hello World` en moins de 2 secondes;
recharger puis décharger l'entrée pour vérifier unicité et retrait.

### Tests for User Story 1

> Écrire les tests avant le comportement et constater leur échec initial.

- [X] T005 [P] [US1] Écrire dans `tests/test_panel.py` les cas d'absence avant configuration, d'enregistrement d'un seul panneau au titre `Family Power Access` et au slug `family-power-access` (URL `/family-power-access`), accessible sans privilège administrateur supplémentaire, de retrait au déchargement, de recréation après rechargement et de collision sans écrasement; constater l'échec initial.
- [X] T006 [P] [US1] Écrire dans `tests/test_panel_asset.py` les contrôles du module livré depuis `custom_components/family_power_access/frontend/panel.js` et servi à `/api/family_power_access/frontend/panel.js`, avec le texte exact `Hello World` et sans chargement de script externe; constater l'échec initial.

### Implementation for User Story 1

- [X] T007 [US1] Créer `custom_components/family_power_access/frontend/panel.js` comme élément personnalisé JavaScript sans dépendance, affichant visiblement `Hello World` avec les couleurs Home Assistant et une mise en page lisible sur fenêtre étroite.
- [X] T008 [US1] Ajouter dans `custom_components/family_power_access/__init__.py` un `async_setup` qui sert une seule fois `custom_components/family_power_access/frontend/` à la route `/api/family_power_access/frontend` via l'API HTTP asynchrone, avec `cache_headers=False`.
- [X] T009 [US1] Étendre `async_setup_entry` dans `custom_components/family_power_access/__init__.py` pour enregistrer le panneau personnalisé au titre `Family Power Access`, au slug `family-power-access` et avec le module local, sans restriction administrateur supplémentaire, tout en conservant le chargement du capteur existant.
- [X] T010 [US1] Étendre `async_unload_entry` et la gestion d'erreur dans `custom_components/family_power_access/__init__.py` pour retirer le panneau, éviter tout doublon au rechargement et refuser clairement une collision de chemin sans remplacer un autre panneau.
- [X] T011 [P] [US1] Documenter dans `README.md` l'entrée de navigation, la page `Hello World`, son accès après configuration et l'absence de commandes d'appareil dans ce jalon.

**Checkpoint**: La User Story fonctionne indépendamment dans une instance locale; le capteur
`Hello World` de la spec 001 reste présent.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Valider l'intégration existante, mesurer le parcours et distribuer la nouveauté
dans une release stable.

- [X] T012 Synchroniser la version mineure `0.2.0` dans `custom_components/family_power_access/manifest.json`, `pyproject.toml`, `uv.lock` et `tests/test_package.py` après validation du comportement local.
- [X] T013 Exécuter pytest, Ruff et Pyright sur `custom_components/family_power_access/` et `tests/`, puis `check_config` dans le conteneur Home Assistant; consigner les résultats dans `specs/002-navigation-hello-world/quickstart.md`.
- [X] T014 Suivre `specs/002-navigation-hello-world/quickstart.md` dans l'instance locale pour vérifier le clic, le délai inférieur à 2 secondes, la fenêtre étroite, le rechargement, le redémarrage, le retrait au déchargement et le maintien du capteur; consigner les observations.
- [ ] T015 Préparer les notes de version dans `README.md`, créer le tag correspondant à la version du `custom_components/family_power_access/manifest.json` et publier la release GitHub stable `0.2.0` après les validations locales.
- [ ] T016 Installer la release stable `0.2.0` par HACS dans l'instance isolée et consigner dans `specs/002-navigation-hello-world/quickstart.md` la version active, l'entrée de navigation, la page `Hello World` et la préservation de la configuration et du capteur existants.
- [ ] T017 Relire `README.md` et `specs/002-navigation-hello-world/quickstart.md` contre FR-001 à FR-007, SC-001 à SC-004 et `specs/002-navigation-hello-world/contracts/navigation.md`; corriger toute divergence et noter les limites restantes.

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Setup (T001–T002) → Foundational (T003–T004) → US1 (T005–T011)
                                            → validation locale (T012–T014)
                                            → release et HACS (T015–T016) → revue (T017)
```

- **Setup**: T001 et T002 peuvent démarrer immédiatement.
- **Foundational**: T003 et T004 suivent Setup et bloquent la User Story.
- **US1**: T005/T006 sont écrits et échouent avant T007–T010. T011 peut avancer pendant
  l'implémentation car il ne modifie pas ses fichiers.
- **Polish**: T012–T014 suivent le code fonctionnel. La release T015 dépend des validations
  locales, et la vérification HACS T016 dépend de la release publiée.

### User Story Dependencies

- **User Story 1 (P1)**: dépend seulement de la fondation T003–T004. Aucun autre récit n'est
  défini dans cette spec.

### Within User Story 1

1. T005 et T006 définissent les contrats vérifiables et échouent d'abord.
2. T007 crée le module visible; T008 enregistre sa ressource locale.
3. T009 enregistre le panneau; T010 garantit son retrait et ses erreurs.
4. T011 explique l'accès à l'utilisateur; le récit est validable dans le conteneur local.

### Parallel Opportunities

- T001 et T002 portent sur des chemins distincts.
- T003 et T004 portent sur `manifest.json` et `const.py` distincts.
- T005 et T006 portent sur deux fichiers de test distincts.
- T011 peut être rédigé après la fondation pendant les changements de code T007–T010.

## Parallel Example: User Story 1

```text
Task: "Écrire les cas de cycle de vie dans tests/test_panel.py" (T005)
Task: "Écrire les contrôles de ressource dans tests/test_panel_asset.py" (T006)

Task: "Implémenter le panneau dans custom_components/family_power_access/frontend/panel.js" (T007)
Task: "Documenter son accès dans README.md" (T011)
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Terminer Setup et Foundational.
2. Écrire les tests de panneau et constater leur échec.
3. Implémenter le module, la route et le cycle de vie du panneau.
4. Valider le récit dans Home Assistant Container et vérifier le capteur existant.

### Incremental Delivery

1. Obtenir une page locale navigable avec le texte exact `Hello World`.
2. Vérifier le déchargement, le rechargement et le redémarrage sans doublons.
3. Synchroniser `0.2.0`, publier la release stable puis valider l'installation HACS.

## Notes

- Les tâches `[P]` n'écrivent pas dans le même fichier et n'attendent pas le résultat d'une
  autre tâche inachevée.
- La spec 001 et ses tests restent la référence pour le capteur et le mécanisme HACS.
- Aucun appareil Zigbee ni donnée d'enfant n'entre dans le périmètre de cette spec.
