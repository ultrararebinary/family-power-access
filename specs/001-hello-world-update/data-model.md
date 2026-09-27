# Data Model: Intégration personnalisée Hello World

Cette phase ne crée aucune base de données propre. Home Assistant conserve l'entrée de
configuration et l'automatisation; HACS conserve les métadonnées de la release installée.

## Entrée de configuration Home Assistant

| Champ | Valeur ou règle |
| --- | --- |
| `domain` | `family_power_access` |
| `unique_id` | Constante stable empêchant un second ajout de la même intégration |
| `data` | Vide; aucun appareil ou secret à configurer pour Hello World |
| `version` | Version du schéma d'entrée de configuration, initialement `1` |

**Relations**: Une entrée crée exactement un capteur Hello World. Elle persiste aux redémarrages
et peut être déchargée sans modifier les données HACS.

**Validation**: Un second flux d'ajout doit s'arrêter avec « déjà configuré ». Aucun code PIN,
identifiant d'enfant ou donnée Zigbee n'est accepté ou stocké à cette étape.

## Entité Hello World

| Champ | Valeur ou règle |
| --- | --- |
| Plateforme | Capteur Home Assistant |
| `unique_id` | `family_power_access_hello_world`, stable entre redémarrages |
| Nom affiché | « Hello World »; traduction anglaise et française fournie |
| Valeur | Texte constant `Hello World` |
| Disponibilité | Disponible tant que l'entrée de configuration est chargée; indépendante de GitHub |

**Relations**: L'entité appartient à l'entrée de configuration. Le retrait ou déchargement de
l'entrée retire l'entité active; un redémarrage la recrée avec le même identifiant.

## Release GitHub et dépôt HACS

| Champ | Propriétaire | Valeur ou règle |
| --- | --- | --- |
| URL du dépôt | Documentation du projet / HACS | Dépôt GitHub public unique |
| Version téléchargée | HACS | Version des fichiers présents après téléchargement; peut attendre un redémarrage |
| Version active | Home Assistant | Version du code chargé, inchangée jusqu'au redémarrage requis |
| Dernière version | HACS | Dernière release stable compatible |
| Préversion | HACS | Non considérée lorsque le commutateur de préversions est désactivé |
| État de mise à jour | HACS | À jour, disponible, téléchargement ou redémarrage requis; les données peuvent rester anciennes si GitHub est indisponible |

Le manifeste de l'intégration et le tag de la release publiée portent le même numéro SemVer.
Le code « Hello World » ne lit pas ces métadonnées pour fonctionner.

## Automatisation facultative de mise à jour

| Champ | Valeur ou règle |
| --- | --- |
| Cible | L'entité `update` HACS de ce dépôt, sélectionnée par le parent |
| Activation | Désactivée ou non créée par défaut; activée par le parent |
| Heure de vérification | Heure locale choisie par le parent; valeur proposée `21:00` |
| Condition | La cible indique une mise à jour disponible |
| Action | Installer la dernière version proposée sans fournir de branche ou SHA explicite |
| Redémarrage | Jamais lancé par l'automatisation |

**Relations**: L'automatisation cible une seule entité HACS. Elle ne crée aucune donnée dans
l'entrée de configuration de l'intégration personnalisée.

## Transitions d'état observables

| État de départ | Événement | État attendu |
| --- | --- | --- |
| Dépôt sans release stable | Essai d'installation HACS avec branche par défaut masquée | Parcours HACS hors du jalon pris en charge; montage local de développement possible |
| Non installée | Installation HACS de `0.1.0`, puis ajout | Installée et Hello World visible |
| À jour | Publication d'une release stable, puis contrôle HACS | Mise à jour disponible |
| Mise à jour disponible | Automatisation activée et heure atteinte | Téléchargement, puis redémarrage requis |
| Redémarrage requis | Parent redémarre Home Assistant | Version téléchargée devient active, Hello World visible |
| À jour | Vérification GitHub impossible | Code actuel disponible; métadonnées HACS possiblement inchangées |
| Téléchargement | Échec ou interruption | Résultat consultable dans HACS ou la trace d'automatisation; README de récupération accessible avant redémarrage |

La dernière transition ne garantit pas une restauration automatique : HACS efface le dossier
cible avant de télécharger les nouveaux fichiers. Le guide de récupération fait partie du
contrat de distribution.
