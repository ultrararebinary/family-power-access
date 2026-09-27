# Quickstart de validation: Hello World et releases GitHub

Ce guide valide les parcours de [spec.md](spec.md) avec les contrats
[Home Assistant](contracts/home-assistant.md) et [GitHub/HACS](contracts/github-releases.md).
Il décrit des contrôles à exécuter après l'implémentation. La
[release stable `0.1.0`](https://github.com/ultrararebinary/family-power-access/releases/tag/0.1.0)
est publiée; le parcours HACS peut maintenant être validé dans une configuration séparée.

## Prérequis

- Mac Apple silicon avec Apple `container` et image officielle Home Assistant `2026.9.3`.
- Dépôt de travail dans `/Users/yann/Documents/ChatGPT/David`.
- Pour le parcours release : dépôt GitHub public publié, HACS configuré dans une instance de
  validation, release stable `0.1.0` publiée, puis release `0.1.1` à créer après le premier
  parcours d'installation HACS.
- Pour les contrôles Python : environnement 3.14.2 ou ultérieur avec les dépendances de
  développement prévues dans le plan. Le Python 3.12 du Mac ne remplace pas cet environnement.

## 1. Valider l'intégration dans Home Assistant Container

Depuis le dépôt de travail :

```sh
cd /Users/yann/Documents/ChatGPT/David
container ls
curl -I http://127.0.0.1:8123/
```

Si le conteneur de développement existant n'est pas disponible, lancer une configuration isolée
sans écraser ses données :

```sh
cd /Users/yann/Documents/ChatGPT/David
mkdir -p .ha-runtime/hello-dev
container run -d --name family-power-dev -p 8124:8123 \
  -v "$PWD/.ha-runtime/hello-dev:/config" \
  -v "$PWD/custom_components:/config/custom_components" \
  ghcr.io/home-assistant/home-assistant:2026.9.3
curl -I http://127.0.0.1:8124/
```

Ouvrir l'interface de l'instance utilisée. Ajouter `Family Power Access` dans *Settings →
Devices & services → Add integration*. Vérifier qu'aucun champ d'appareil n'est requis et qu'un
capteur « Hello World » affiche `Hello World`. Redémarrer Home Assistant depuis l'interface :
le capteur doit revenir avec le même identifiant unique. Déconnecter temporairement GitHub ou
répéter hors réseau : le capteur doit rester disponible.

## 2. Contrôler la qualité du code

Dans l'environnement Python 3.14.2+ prévu pour le projet :

```sh
python3 -m ruff check custom_components tests
python3 -m ruff format --check custom_components tests
python3 -m pyright custom_components
python3 -m pytest tests -q
```

Résultat attendu : le flux de configuration, le capteur, l'unicité et le redémarrage passent
sans erreur. Les fichiers de test et outils indiqués ici seront créés pendant l'implémentation.

## 3. Valider une release HACS dans une configuration séparée

La validation HACS ne doit pas écrire dans le dossier source monté à l'étape 1. Démarrer une
seconde instance avec son propre `/config` :

```sh
cd /Users/yann/Documents/ChatGPT/David
mkdir -p .ha-runtime/hello-release
container run -d --name family-power-release -p 8125:8123 \
  -v "$PWD/.ha-runtime/hello-release:/config" \
  ghcr.io/home-assistant/home-assistant:2026.9.3
curl -I http://127.0.0.1:8125/
```

Dans cette instance :

1. Configurer HACS selon son [guide officiel](https://hacs.xyz/docs/use/configuration/basic/).
2. Ajouter le dépôt GitHub public du projet comme dépôt personnalisé de type *Integration* et
   installer la release stable `0.1.0`.
3. Redémarrer si HACS l'indique, ajouter `Family Power Access` et vérifier le capteur.
4. Publier `0.1.1`. Attendre la vérification HACS ou utiliser *Update information* pour le
   contrôle ponctuel. L'entité HACS du dépôt doit indiquer la version téléchargée, la nouvelle
   version et l'URL de la release; la préversion reste désactivée.
5. Importer le blueprint du dépôt, sélectionner **uniquement** l'entité `update` HACS de ce
   dépôt, choisir l'heure, puis activer l'automatisation. Déclencher son exécution dans
   l'interface pour vérifier qu'elle appelle `update.install` sans version explicite.
6. Vérifier l'état HACS « Pending restart » : `0.1.1` est téléchargée, tandis que le code déjà
   chargé peut encore être `0.1.0`. Le parent choisit quand redémarrer. Après redémarrage,
   `0.1.1` est active et « Hello World » visible.
7. Désactiver l'automatisation, publier une autre release stable et vérifier qu'elle est
   proposée sans installation automatique.

## 4. Vérifier les échecs et la récupération

- Sans accès GitHub lors d'un contrôle HACS, vérifier que l'élément Hello World déjà chargé
  reste visible. Les métadonnées HACS peuvent rester anciennes; effectuer un nouveau contrôle
  après le retour du réseau.
- Faire échouer `update.install` dans l'instance de validation. Consulter la trace de
  l'automatisation et l'état du dépôt HACS; vérifier qu'aucune autre entité `update` n'est
  modifiée et qu'aucun redémarrage n'est lancé.
- Si HACS indique qu'un téléchargement a échoué, ouvrir le README depuis la page du dépôt,
  suivre sa procédure et **ne pas redémarrer** avant d'avoir réinstallé la dernière release
  stable. Confirmer ensuite que les fichiers sont complets, puis redémarrer.
- Publier une préversion dans le dépôt de validation : elle ne doit pas être proposée tant que
  le commutateur HACS des préversions est désactivé.
- Mesurer les objectifs de la spec : ajout en moins de 5 minutes avec HACS déjà configuré,
  capteur visible en moins de 2 minutes et release stable proposée après une actualisation HACS
  réussie lorsque GitHub est accessible. La cadence des contrôles automatiques HACS n'est pas
  un engagement de délai de ce jalon.

## Résultat attendu

Le parcours est complet quand la version `0.1.0` s'installe depuis GitHub via HACS, que son
capteur persiste au redémarrage, que l'automatisation activée installe `0.1.1` depuis la release
stable sans copie manuelle, et qu'aucun redémarrage n'est déclenché à l'insu du parent.

## Résultats observés le 27 septembre 2026

- Home Assistant 2026.9.3 tourne dans l'instance Container isolée `family-power-release`
  (`http://127.0.0.1:8125/`). HACS 2.0.5 y est configuré et le dépôt
  `ultrararebinary/family-power-access` est ajouté comme *Integration*.
- HACS a téléchargé la release stable `0.1.0`. Après redémarrage, l'intégration a été ajoutée
  sans champ et le capteur `Hello World` a affiché l'état `Hello World`. Le journal Recorder
  a enregistré l'entrée à `16:45:25.956 UTC` et son premier état à `16:45:25.977 UTC` (environ
  20 ms plus tard). Le temps SC-001 n'a pas été chronométré au départ du parcours utilisateur;
  le capteur était visible dans les minutes suivant le flux d'ajout.
- Pour le test de mise à jour, le blueprint a été importé depuis la release `0.1.0` puis
  instancié en visant uniquement `update.family_power_access_update`, avec l'heure par défaut
  `21:00`. HACS a détecté la release stable `0.1.1` après actualisation. La trace Home
  Assistant montre l'action `update.install` avec `service_data: {}` et cette seule cible.
- Après l'action, les fichiers HACS étaient en `0.1.1`, tandis que la page d'intégration
  indiquait encore la version active `0.1.0` et Home Assistant signalait `HACS Restart
  required`. Le conteneur était toujours actif : aucun redémarrage automatique n'a eu lieu.
  Après le redémarrage manuel de l'instance de validation, la page de l'intégration a indiqué
  `0.1.1`; l'entité `Hello World` affichait toujours le même état. L'automatisation de test a
  ensuite été désactivée.
- GitHub publie les releases stables
  [`0.1.0`](https://github.com/ultrararebinary/family-power-access/releases/tag/0.1.0) et
  [`0.1.1`](https://github.com/ultrararebinary/family-power-access/releases/tag/0.1.1).
- Sur Python 3.14.2, `pytest tests -q` : 14 tests réussis. `ruff check .`,
  `ruff format --check custom_components tests` et `pyright custom_components` : réussis.
  `check_config` a aussi réussi dans le conteneur. Un test simule un échec de `update.install`
  et vérifie son apparition dans la trace et la cible unique.
- Les scénarios HACS de préversion, GitHub indisponible et téléchargement interrompu n'ont
  pas été provoqués dans cette instance. Le README décrit la récupération après échec; ces
  cas restent à valider en test complémentaire. Leur report et l'absence de chronométrage de
  SC-001 ont été acceptés par l'utilisateur à la clôture de Spec 001 le 27 septembre 2026.
