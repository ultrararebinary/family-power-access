# Contrat GitHub et HACS: installation et mises à jour

## Dépôt publié

- Le dépôt GitHub est public, possède un README d'installation, une description et les thèmes
  GitHub requis par HACS.
- Il ne livre qu'une intégration sous `custom_components/family_power_access/`.
- `hacs.json` est à la racine du dépôt, nomme l'intégration et masque la branche par défaut dans
  le parcours HACS (`hide_default_branch: true`).
- `manifest.json` nomme le domaine, l'intégration, sa version, la documentation, le suivi des
  problèmes et les mainteneurs. La première version est `0.1.0`.
- Le dépôt contient `brand/icon.png` et tous les fichiers nécessaires à l'exécution dans le
  dossier de l'intégration.
- Chaque version distribuée correspond à une *release* GitHub stable publiée, avec un tag SemVer
  identique à la version du manifeste. Un simple tag ou une branche non publiée ne suffit pas.
- Tant qu'aucune release stable n'existe, le projet ne prend pas en charge l'installation HACS;
  le montage local reste utilisable pour le test.

L'URL publique réelle et les identifiants des mainteneurs sont ajoutés au manifeste et à la
documentation avant la première release. Le checkout actuel n'a pas encore de remote Git.

## Installation et découverte

1. Le parent ajoute le dépôt public dans HACS comme dépôt personnalisé de type *Integration*.
2. Il télécharge une release stable, redémarre Home Assistant si HACS l'indique, puis ajoute
   `Family Power Access` dans *Devices & services*.
3. HACS expose pour ce dépôt une entité `update` présentant la version téléchargée, la dernière
   version disponible, le résumé et l'URL de la release lorsqu'ils existent. Après un
   téléchargement, la version exécutée reste celle déjà chargée jusqu'au redémarrage requis.
4. Le commutateur HACS des préversions du dépôt reste désactivé pour ce canal stable.

## Installation automatique facultative

Le projet fournit un blueprint d'automatisation importable par URL depuis le dépôt. Le parent
choisit l'entité `update` HACS de **ce seul dépôt** et l'heure de contrôle, puis active
l'automatisation dans Home Assistant. Le comportement prévu est :

```text
Déclencheur : heure locale choisie (proposition : 21:00)
Condition   : l'entité update choisie a une mise à jour disponible
Action      : update.install sur cette entité, sans argument de version
```

L'automatisation ne redémarre jamais Home Assistant et ne modifie aucune autre entité `update`.
Le parent peut la désactiver dans Home Assistant; l'installation automatique est désactivée par
défaut tant qu'il ne l'a pas activée. HACS signale ensuite « Pending restart » et expose
l'action de redémarrage requise.

## Erreurs et récupération

- Si GitHub n'est pas joignable pendant un contrôle de métadonnées, l'intégration Hello World
  déjà chargée continue de fonctionner; les informations HACS peuvent rester anciennes et une
  nouvelle vérification sera possible. Aucune notification réseau propre à l'intégration n'est
  garantie.
- Le résultat d'une automatisation est consultable dans sa trace Home Assistant; l'état du
  dépôt est consultable dans HACS. Le README affiché depuis la page HACS du dépôt donne la
  procédure de reprise. Une erreur de `update.install` ne déclenche aucun redémarrage ni action
  sur une autre entité de mise à jour.
- Si le téléchargement HACS échoue, le parent réinstalle la dernière release stable depuis HACS
  avant de redémarrer Home Assistant. Le guide ne promet pas une alerte dédiée supplémentaire.
- HACS efface le dossier cible avant de télécharger. Le projet ne promet donc pas une
  restauration automatique des fichiers en cas d'échec pendant l'installation.
- Le parcours de validation des releases se fait dans une configuration Container jetable,
  séparée du montage du code source de développement.

## Références

[Exigences de publication HACS](https://hacs.xyz/docs/publish/start/),
[structure des intégrations HACS](https://hacs.xyz/docs/publish/integration/),
[entités de mise à jour HACS](https://hacs.xyz/docs/use/entities/update/),
[automatisations Home Assistant](https://www.home-assistant.io/integrations/update/),
[préversions HACS](https://hacs.xyz/docs/use/entities/switch/),
[séquence de téléchargement HACS](https://hacs.xyz/docs/faq/download/).
