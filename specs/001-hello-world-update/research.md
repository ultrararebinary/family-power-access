# Phase 0 Research: Intégration personnalisée Hello World

Toutes les décisions nécessaires au plan sont résolues. Cette phase ne prévoit aucun appareil
Zigbee ni aucune donnée relative aux enfants.

## Décision 1 — Socle Home Assistant

**Decision**: Créer une seule intégration personnalisée sous
`custom_components/family_power_access/`, avec une configuration ajoutable dans l'interface et
une entité de type capteur affichant « Hello World ». L'entité a un identifiant unique stable et
ne dépend d'aucune requête réseau. La version initiale est `0.1.0`.

**Rationale**: Home Assistant charge les intégrations personnalisées depuis `custom_components`.
Une version est requise dans leur manifeste; un flux de configuration permet l'ajout depuis
l'interface. Une entité stable rend le résultat visible et vérifiable après redémarrage.
[Création d'intégration](https://developers.home-assistant.io/docs/creating_component_index/),
[manifeste](https://developers.home-assistant.io/docs/creating_integration_manifest/),
[flux de configuration](https://developers.home-assistant.io/docs/core/integration/config_flow/),
[entités](https://developers.home-assistant.io/docs/core/entity/).

**Alternatives considered**: Une simple notification au démarrage disparaîtrait sans fournir
d'entité persistante. Une configuration YAML manuelle ne satisfait pas l'ajout dans l'interface.
Un coordinateur de données n'a pas d'utilité pour une valeur fixe.

## Décision 2 — Distribution et versions

**Decision**: Publier un dépôt GitHub public contenant une seule intégration, un `hacs.json` à la
racine, un `manifest.json` versionné dans l'intégration, un README et une icône. Distribuer par
HACS comme dépôt personnalisé. Publier des releases GitHub stables numérotées (`0.1.0`, puis
`0.1.1`, etc.); synchroniser la version du manifeste et le tag. Masquer la branche par défaut
dans HACS afin que le parcours normal ne propose que les releases.

Sans release stable, le projet ne prend pas en charge l'installation HACS; le montage local
du code reste la voie de validation avant la première publication.

**Rationale**: HACS décrit cette structure pour les intégrations, requiert un dépôt public et
un `hacs.json` à la racine. Les tags seuls ne constituent pas des releases utilisables comme
versions distantes. L'installation et le suivi des mises à jour sont déjà fournis par HACS.
[Exigences générales HACS](https://hacs.xyz/docs/publish/start/),
[structure d'intégration HACS](https://hacs.xyz/docs/publish/integration/),
[dépôts personnalisés](https://hacs.xyz/docs/faq/custom_repositories/).

**Alternatives considered**: Télécharger le contenu de la branche par défaut contournerait les
releases stables de la constitution. Un dépôt privé n'est pas pris en charge par HACS.
[Limite des dépôts privés](https://hacs.xyz/docs/faq/private_repositories/).

## Décision 3 — Mises à jour automatiques facultatives

**Decision**: Laisser HACS exposer l'entité de mise à jour du dépôt. Fournir un blueprint
d'automatisation Home Assistant qui cible uniquement cette entité, vérifie chaque soir qu'une
mise à jour est disponible, puis lance `update.install` sans version explicite. Le parent importe
et active l'automatisation; elle est absente ou désactivée par défaut. Le commutateur HACS des
préversions reste désactivé. Aucun redémarrage automatique de Home Assistant.

**Rationale**: HACS crée une entité `update` pour chaque dépôt suivi et permet l'action
`update.install`. Home Assistant documente l'automatisation d'une installation programmée. Le
commutateur HACS détermine si les préversions sont prises en compte. Après téléchargement d'une
intégration, HACS signale l'état « Pending restart » et une réparation de redémarrage.
[Entités HACS](https://hacs.xyz/docs/use/entities/update/),
[automatisations de mise à jour](https://www.home-assistant.io/integrations/update/),
[préversions HACS](https://hacs.xyz/docs/use/entities/switch/),
[état de redémarrage HACS](https://hacs.xyz/docs/use/repositories/dashboard/).

**Alternatives considered**: Un programme de mise à jour inclus dans l'intégration devrait
écrire son propre code et reproduire la gestion des versions de HACS. Une simple notification
HACS exigerait une installation manuelle et ne répondrait pas à l'option automatique demandée.

## Décision 4 — Échec et récupération

**Decision**: Une erreur de vérification ne modifie pas l'installation actuelle. Après une
erreur de téléchargement, le guide demande de réinstaller la dernière release stable dans HACS
avant tout redémarrage. Le résultat d'une automatisation se consulte dans sa trace Home
Assistant et la procédure de récupération dans le README visible depuis HACS. La mise à jour
doit être validée dans une installation de test séparée du montage du code source de
développement.

**Rationale**: HACS supprime le dossier cible avant de télécharger les nouveaux fichiers; ses
documents ne garantissent donc pas une restauration transactionnelle en cas d'interruption.
Le plan et la spec décrivent explicitement ce comportement et la procédure de récupération.
HACS contrôle les métadonnées des dépôts régulièrement sans publier de délai maximal garanti;
le critère de succès se rapporte donc à une actualisation réussie, pas à une limite de 24 h.
[Séquence de téléchargement HACS](https://hacs.xyz/docs/faq/download/),
[actualisation du dépôt HACS](https://hacs.xyz/docs/use/repositories/dashboard/).

**Alternatives considered**: Promettre que la version précédente reste installée après toute
erreur de téléchargement ne serait pas étayé par le comportement documenté de HACS. Une
méthode de sauvegarde personnalisée ajouterait une dépendance système et du code hors du socle.

## Décision 5 — Environnement et validation

**Decision**: Développer dans Home Assistant Container sur Apple `container`; épingler
`2026.9.3` pour les validations reproductibles. Vérifier l'intégration avec les outils de test
Home Assistant et les vérifications de style/type du dépôt. Vérifier les releases HACS dans une
configuration Home Assistant jetable distincte de la configuration de développement.

**Rationale**: La version stable publiée au moment de ce plan est 2026.9.3; l'environnement de
développement Home Assistant requiert Python 3.14.2 ou ultérieur. Un paquet de test de composants
personnalisés fournit les fixtures Home Assistant dans un dépôt indépendant du Core.
[Version Home Assistant](https://www.home-assistant.io/integrations/update/),
[environnement de développement](https://developers.home-assistant.io/docs/development_environment/),
[fixtures de test](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component),
[volumes Apple container](https://github.com/apple/container/blob/main/docs/volumes.md).

**Alternatives considered**: Exécuter HACS dans la configuration de développement monterait
les fichiers du dépôt comme cible de mises à jour et pourrait les modifier. Les tests Python
sur l'interpréteur macOS 3.12 ne correspondent pas au runtime Home Assistant 2026.9.
