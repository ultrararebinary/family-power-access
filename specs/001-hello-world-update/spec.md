# Feature Specification: Intégration personnalisée Hello World et mises à jour GitHub

**Feature Branch**: `001-hello-world-update`

**Created**: 2026-09-26

**Status**: Draft

**Input**: Demande corrigée : « Créer une intégration personnalisée Home Assistant façon “Hello World”, que l’on puisse mettre à jour automatiquement à partir d’un dépôt GitHub. »

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Installer et vérifier l’intégration (Priority: P1)

Un parent installe l’intégration personnalisée dans son instance Home Assistant depuis le dépôt GitHub du
projet. Il peut l’ajouter depuis l’interface Home Assistant et voit un élément « Hello World »
confirmant que l’intégration fonctionne.

**Why this priority**: Ce socle confirme que le dépôt fournit bien une intégration installable et
exécutable avant d’ajouter les fonctions familiales et Zigbee.

**Independent Test**: Installer la version initiale dans une instance Home Assistant Container,
ajouter l’intégration, puis vérifier que son élément « Hello World » est visible et utilisable.

**Acceptance Scenarios**:

1. **Given** une instance Home Assistant compatible et le dépôt public du projet, **When** le
   parent installe puis ajoute l’intégration, **Then** l’intégration apparaît dans Home Assistant
   et expose un élément identifiable affichant « Hello World ».
2. **Given** l’intégration est configurée, **When** Home Assistant redémarre, **Then** l’élément
   « Hello World » réapparaît sans nouvelle configuration.
3. **Given** GitHub est indisponible, **When** Home Assistant démarre, **Then** l’élément
   « Hello World » reste disponible sans attendre une vérification des mises à jour.

### User Story 2 - Recevoir et appliquer une mise à jour (Priority: P1)

Un parent peut laisser Home Assistant suivre les versions stables publiées dans le dépôt GitHub.
Il voit la version téléchargée et la version proposée, puis peut activer l’installation automatique
des nouvelles versions stables. L'état HACS et la trace de l'automatisation permettent de
vérifier le résultat; HACS indique si Home Assistant doit être redémarré pour charger la
nouvelle version.

**Why this priority**: Les mises à jour depuis le dépôt sont une exigence de départ et évitent de
devoir copier manuellement les fichiers de l’intégration.

**Independent Test**: Installer une première version, publier une version stable plus récente,
activer les mises à jour automatiques, puis vérifier que la version proposée et l’état de la mise
à jour sont visibles dans Home Assistant.

**Acceptance Scenarios**:

1. **Given** une version stable plus récente est publiée sur le dépôt GitHub, **When** HACS
   actualise avec succès les informations du dépôt, **Then** Home Assistant présente la version
   téléchargée, la nouvelle version et les informations de publication disponibles.
2. **Given** le parent a activé les mises à jour automatiques, **When** une nouvelle version
   stable est disponible, **Then** elle est récupérée et appliquée sans copie manuelle de fichiers,
   et le parent voit le résultat ainsi que toute action restante pour l’activer.
3. **Given** les mises à jour automatiques sont désactivées, **When** une nouvelle version stable
   est disponible, **Then** elle est signalée sans être installée automatiquement.
4. **Given** GitHub est temporairement indisponible, **When** HACS tente d’actualiser le dépôt,
   **Then** le code déjà chargé continue de fonctionner et une nouvelle actualisation reste
   possible; aucune garantie de notification propre à l’intégration n’est requise.
5. **Given** le téléchargement d’une mise à jour échoue, **When** le parent consulte le dépôt
   dans HACS, **Then** il peut accéder au README décrivant la réinstallation de la dernière
   version stable avant tout redémarrage.
6. **Given** une préversion est publiée, **When** les versions disponibles sont recherchées,
   **Then** elle n’est pas installée comme version stable.

### Edge Cases

- Le dépôt ne publie encore aucune version stable : le montage local permet de tester
  l’intégration; l’installation par HACS commence après la publication de `0.1.0`.
- Une nouvelle version n’est pas plus récente que la version téléchargée : elle n’est pas proposée
  comme mise à jour.
- La connexion à GitHub est interrompue pendant la vérification : le code déjà chargé et
  l’élément « Hello World » restent utilisables; les métadonnées HACS peuvent rester anciennes.
- La récupération d’une mise à jour est interrompue : HACS peut laisser le dossier incomplet;
  le parent consulte son état et le README, puis réinstalle une version stable avant redémarrage.
- Une mise à jour récupérée ne peut pas être activée immédiatement : son état reste visible et
  Home Assistant indique l’action nécessaire, sans redémarrer l’instance à l’insu du parent.
- Le dépôt GitHub est privé ou inaccessible avec les droits de l’utilisateur : l’installation ou
  la vérification échoue avec une explication exploitable et sans effacer l’installation actuelle.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: L’intégration personnalisée MUST pouvoir être installée dans une instance Home Assistant depuis
  le dépôt GitHub public du projet, sans copie manuelle de ses fichiers.
- **FR-002**: Un parent MUST pouvoir ajouter l’intégration depuis l’interface Home Assistant sans
  avoir à saisir de configuration propre à un appareil pour cette version « Hello World ».
- **FR-003**: Après son ajout, l’intégration MUST exposer dans Home Assistant un élément visible,
  identifiable et portant le message « Hello World ».
- **FR-004**: L’élément « Hello World » MUST rester disponible après un redémarrage normal de Home
  Assistant et MUST NOT dépendre de l’accès à GitHub pour son fonctionnement courant.
- **FR-005**: Le parcours de mise à jour MUST suivre les releases stables publiées dans le dépôt
  GitHub et présenter la version téléchargée, la dernière version stable proposée et l’état de
  mise à jour disponible dans HACS après une actualisation réussie.
- **FR-006**: Un parent MUST pouvoir activer ou désactiver l’installation automatique des versions
  stables. Le réglage initial MUST laisser l’installation automatique désactivée.
- **FR-007**: Lorsque l’installation automatique est activée, la solution MUST récupérer et
  appliquer une version stable plus récente sans copie manuelle de fichiers.
- **FR-008**: Les préversions MUST être exclues des mises à jour stables.
- **FR-009**: HACS MUST rendre visibles une mise à jour disponible et le redémarrage nécessaire
  après téléchargement; le résultat d’une automatisation MUST rester consultable dans Home
  Assistant. La solution MUST NOT redémarrer Home Assistant sans action explicite du parent.
- **FR-010**: Un échec de vérification MUST laisser le code déjà chargé utilisable. Le README
  accessible depuis le dépôt HACS MUST décrire comment réinstaller la dernière release stable
  après un téléchargement interrompu et avant tout redémarrage.
- **FR-011**: Cette fonctionnalité MUST se limiter au socle « Hello World » et à son installation
  et cycle de mise à jour. Le contrôle Zigbee, les codes personnels, les calendriers, les quotas et
  le suivi d’utilisation des enfants sont hors périmètre de cette spécification.

### Key Entities *(include if feature involves data)*

- **Intégration chargée**: L’intégration actuellement exécutée par Home Assistant; elle conserve
  sa version active jusqu’au prochain redémarrage ou rechargement requis.
- **Version téléchargée**: La version enregistrée par HACS, qui peut être plus récente que la
  version active tant qu’un redémarrage est nécessaire.
- **Version publiée**: Une version stable du projet publiée sur son dépôt GitHub, avec numéro de
  version et informations de publication.
- **Préférence de mise à jour**: Le choix du parent d’autoriser ou non l’installation automatique
  des versions stables.
- **État de mise à jour**: Les informations HACS disponibles après actualisation, la trace d'une
  installation automatisée et l'éventuel redémarrage restant au parent.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un parent peut installer et ajouter l’intégration en moins de 5 minutes, sans copier
  de fichiers à la main ni saisir de paramètre d’appareil.
- **SC-002**: Dans 100 % des parcours de vérification sur une instance prise en charge, l’élément
  « Hello World » devient visible dans les 2 minutes suivant l’ajout de l’intégration.
- **SC-003**: Dans 100 % des parcours de validation avec GitHub accessible, la nouvelle release
  stable est proposée après une actualisation réussie des informations du dépôt HACS, automatique
  ou déclenchée depuis son interface.
- **SC-004**: Quand l’installation automatique est activée, une mise à jour stable est récupérée
  sans action de copie ou de téléchargement manuel par le parent; toute action d’activation
  restante est indiquée clairement.
- **SC-005**: Dans 100 % des parcours de validation où GitHub est indisponible, l’élément
  « Hello World » déjà chargé reste visible et utilisable.

## Assumptions

- Le dépôt GitHub sera public et publiera des versions stables identifiées par un numéro de
  version; les préversions seront réservées aux essais et exclues du canal stable.
- L’installation automatique est une option explicite du parent et est désactivée par défaut.
- HACS est déjà installé et configuré sur l’instance utilisée pour mesurer le parcours de cinq
  minutes. Son installation initiale est un prérequis distinct de cette fonctionnalité.
- Home Assistant ne sera pas redémarré automatiquement. Si une mise à jour nécessite un
  redémarrage pour prendre effet, HACS l'indiquera au parent.
- Cette première version n’interagit avec aucun appareil Zigbee et ne stocke aucune donnée
  d’utilisation d’enfant.
- Il s’agit d’une intégration personnalisée distribuée séparément de Home Assistant Core.
- L’instance de développement et de validation est Home Assistant Container, conformément à la
  constitution du projet.

## Exception de portée constitutionnelle — jalon exploratoire

Cette release `0.1.x` sert uniquement à vérifier le chargement, l’installation et les mises à
jour d’une intégration personnalisée. Elle n’énergise aucune prise et ne traite ni code enfant
ni donnée d’utilisation. À ce titre, les capacités finales imposées par les principes I, III,
IV et V de la constitution (clavier Zigbee, calendrier, quotas et audit par enfant) sont
temporairement différées. Le choix des appareils Zigbee, des unités de quota et des limites de
jour/fuseau horaire est réservé à la première spécification qui pilote effectivement une prise;
aucune fonction de pilotage ne peut être implémentée avant ces décisions.

**Justification**: Le demandeur a précisé que Hello World sert seulement à tester les
intégrations personnalisées. Cette exception limitée au jalon exploratoire a été revue et
acceptée le 2026-09-26; elle ne modifie pas les obligations du produit final.
