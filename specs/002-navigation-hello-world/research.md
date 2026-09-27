# Recherche : navigation Family Power Access

## Décision 1 — Panneau personnalisé enregistré par l'intégration

**Decision**: Enregistrer une page personnalisée au chargement de l'entrée de configuration
Family Power Access, avec le titre de barre latérale « Family Power Access » et un chemin
stable propre au domaine. Retirer ce panneau au déchargement de l'entrée.

**Rationale**: Les [panneaux personnalisés Home Assistant](https://developers.home-assistant.io/docs/frontend/custom-ui/creating-custom-panels/)
sont des pages accessibles depuis la barre latérale. Home Assistant 2026.9.3 fournit
`panel_custom.async_register_panel` et `frontend.async_remove_panel`; les intégrations Core
comme KNX enregistrent déjà un panneau et son fichier statique de cette façon. Le panneau
peut être créé avec l'intégration sans édition de la configuration de l'utilisateur.

**Alternatives considered**:

- Déclarer `panel_custom` dans `configuration.yaml` : demanderait une étape manuelle et ne
  suivrait pas directement l'ajout ou le retrait de l'intégration.
- Créer un tableau de bord à la place : ajouterait une configuration utilisateur et davantage
  d'état à gérer pour afficher une seule phrase.

## Décision 2 — Module JavaScript minimal inclus dans le paquet HACS

**Decision**: Placer un module JavaScript sans dépendance ni étape de compilation dans
`custom_components/family_power_access/frontend/`. Il définit un élément personnalisé qui
affiche « Hello World » avec les couleurs de thème Home Assistant et un agencement lisible
sur écran étroit.

**Rationale**: Un panneau Home Assistant est un élément personnalisé du navigateur. Le
module reste dans le dossier d'intégration livré par HACS, de sorte que l'installation de
la release fournit la page sans téléchargement externe. Les [docs des panneaux](https://developers.home-assistant.io/docs/frontend/custom-ui/creating-custom-panels/)
décrivent le chargement par `module_url` et les propriétés `hass`, `narrow` et `panel`.
Le contenu statique n'utilise aucune donnée de l'utilisateur.

**Alternatives considered**:

- Ajouter Lit, React ou un outil de compilation : inutile pour une phrase et accroîtrait
  les dépendances du projet.
- Charger un module hébergé sur un CDN : créerait une dépendance réseau pour une page locale.

**Test dependency**: L'environnement de développement Home Assistant ne contient pas par
défaut le paquet `hass_frontend` requis pour démarrer le composant `frontend`. La dépendance
de développement officielle `home-assistant-frontend==20260826.7`, correspondant au manifeste
de Home Assistant 2026.9.3, sera ajoutée afin que les tests chargent le même frontend que le
conteneur. Elle n'est pas déclarée dans `manifest.json` et n'est pas installée sur les systèmes
utilisateurs comme exigence Python de l'intégration.

## Décision 3 — Exposition du module et cycle de vie

**Decision**: Enregistrer le répertoire du module une seule fois lors de `async_setup`, avec
`hass.http.async_register_static_paths` et `StaticPathConfig(..., cache_headers=False)`.
Enregistrer le panneau lors de `async_setup_entry`; le supprimer lors de
`async_unload_entry`. Déclarer `panel_custom` comme dépendance Home Assistant de
l'intégration; ce composant dépend déjà de `frontend`, qui dépend de `http`.

**Rationale**: L'[API asynchrone des chemins statiques](https://developers.home-assistant.io/blog/2024/06/18/async_register_static_paths/)
évite les E/S bloquantes dans la boucle Home Assistant. Le `async_setup` du domaine ne se
répète pas à chaque rechargement d'entrée, ce qui évite de réenregistrer le même chemin.
Le panneau peut être retiré sans supprimer le chemin statique; le module ne contient que
du contenu public « Hello World ». La [déclaration de dépendances](https://developers.home-assistant.io/docs/creating_integration_manifest/#dependencies)
garantit que les composants nécessaires sont prêts avant le chargement.

**Alternatives considered**:

- Réenregistrer le chemin statique dans chaque `async_setup_entry` : un rechargement pourrait
  tenter d'enregistrer deux fois la même route.
- Garder le panneau après le déchargement : contredirait le comportement de navigation
  attendu par FR-006.

## Décision 4 — Portée des droits et des validations

**Decision**: Rendre la page accessible aux utilisateurs Home Assistant connectés qui ont
accès à la navigation, sans restriction administrateur supplémentaire. Garder le module
statique sans secret ni données personnelles. Vérifier le titre, le chemin unique, le
chargement de la page, l'absence de doublons et le retrait au déchargement de l'entrée.

**Rationale**: La page ne permet aucune commande et l'exigence FR-007 suit les droits de
navigation Home Assistant. La validation combine les tests de cycle de vie de l'intégration
et un parcours navigateur réel sur Home Assistant Container 2026.9.3, y compris une fenêtre
étroite. Les [principes des panneaux](https://developers.home-assistant.io/docs/frontend/custom-ui/creating-custom-panels/)
confirment que le frontend charge la page dans l'interface existante.

**Alternatives considered**:

- Réserver la page aux administrateurs : empêcherait des utilisateurs Home Assistant
  ordinaires de voir le simple message sans bénéfice pour la sécurité.
