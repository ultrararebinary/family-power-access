# Family Power Access

Intégration personnalisée Home Assistant en phase **Hello World**. Cette version sert à
valider l'installation, le chargement dans Home Assistant et les mises à jour depuis des
releases GitHub. Elle ne contrôle encore aucune prise, ne lit aucun clavier Zigbee et ne gère
ni codes enfants, ni calendriers, ni quotas.

## Versions et prérequis

- Home Assistant Container 2026.9.3 ou version compatible plus récente.
- HACS configuré pour l'installation depuis GitHub.
- Le dépôt GitHub public
  [`ultrararebinary/family-power-access`](https://github.com/ultrararebinary/family-power-access),
  avec les releases stables
  [`0.1.0`](https://github.com/ultrararebinary/family-power-access/releases/tag/0.1.0)
  et [`0.1.1`](https://github.com/ultrararebinary/family-power-access/releases/tag/0.1.1).

La branche par défaut est masquée dans HACS : le parcours d'installation pris en charge
commence avec la release `0.1.0`. La version actuelle est `0.1.1`. Pour développer localement, monter `custom_components/`
dans un conteneur Home Assistant; voir le
[guide de validation](specs/001-hello-world-update/quickstart.md).

## Installer l'intégration

1. Dans HACS, ajouter `ultrararebinary/family-power-access` comme dépôt personnalisé de type
   **Integration**, puis télécharger la dernière release stable.
2. Redémarrer Home Assistant si HACS affiche **Pending restart**.
3. Dans **Paramètres → Appareils et services → Ajouter une intégration**, choisir
   **Family Power Access**. Aucun paramètre d'appareil n'est requis.
4. Vérifier que l'entité **Hello World** affiche l'état `Hello World`.

La configuration et l'entité reviennent après un redémarrage de Home Assistant. Le message
Hello World reste disponible même si GitHub est inaccessible.

## Mises à jour

HACS suit les releases stables du dépôt et crée une entité `update` pour celui-ci. Dans HACS,
laisser le commutateur des **préversions** sur **OFF**. Une nouvelle version peut être
téléchargée manuellement depuis HACS.

Pour autoriser l'installation automatique, importer le
[blueprint de mise à jour](blueprints/automation/family_power_access_auto_update.yaml) dans
Home Assistant depuis son URL GitHub
(`https://raw.githubusercontent.com/ultrararebinary/family-power-access/0.1.1/blueprints/automation/family_power_access_auto_update.yaml`),
sélectionner **uniquement** l'entité `update` HACS de ce
dépôt, choisir l'heure de contrôle (21 h par défaut), puis créer et activer
l'automatisation. La désactiver dans Home Assistant pour revenir aux mises à jour manuelles.
L'automatisation n'est pas créée lors de l'installation de l'intégration.

### Releases

- [`0.1.0`](https://github.com/ultrararebinary/family-power-access/releases/tag/0.1.0) :
  première intégration avec le capteur de diagnostic `Hello World`.
- [`0.1.1`](https://github.com/ultrararebinary/family-power-access/releases/tag/0.1.1) :
  version utilisée pour valider le téléchargement HACS, le statut de redémarrage requis et
  l'activation de la nouvelle version après redémarrage manuel.

L'automatisation appelle `update.install` pour cette seule entité, sans imposer de version
ou de branche. Elle ne redémarre pas Home Assistant. Après un téléchargement réussi, HACS
peut montrer **Pending restart** : la **version téléchargée** peut alors être plus récente
que la **version active**. Le parent choisit quand redémarrer pour activer le nouveau code.
Le résultat d'une automatisation reste consultable dans sa trace Home Assistant.

### Si une mise à jour échoue

Si GitHub est momentanément inaccessible pendant le contrôle, le code Hello World déjà
chargé continue de fonctionner. Les informations HACS peuvent rester anciennes; réessayer
l'actualisation du dépôt quand le réseau revient.

Si le téléchargement ou `update.install` échoue :

1. **Ne pas redémarrer Home Assistant.** HACS peut avoir supprimé le dossier de l'intégration
   avant de télécharger les nouveaux fichiers.
2. Ouvrir la page du dépôt dans HACS, consulter son état, puis choisir **Redownload** et
   réinstaller la dernière release stable publiée.
3. Vérifier que HACS indique le téléchargement terminé. Redémarrer Home Assistant seulement
   après cette réinstallation, puis vérifier l'entité Hello World.

HACS ne garantit pas un retour automatique à la version précédente si un téléchargement est
interrompu. Une erreur de l'automatisation est visible dans sa trace; cette intégration ne
crée pas de notification supplémentaire.

## Développement

Le projet utilise [SpecKit](specs/001-hello-world-update/spec.md). Le code de l'intégration
vit dans `custom_components/family_power_access/`. Les données Home Assistant restent sous
`.ha-runtime/`, exclu du dépôt Git.

```sh
UV_CACHE_DIR=/private/tmp/fpa-uv-cache UV_PYTHON_INSTALL_DIR="$PWD/.ha-runtime/uv-python" uv sync --group dev --python 3.14.2
.venv/bin/python -m pytest tests -q
.venv/bin/ruff check custom_components tests
.venv/bin/pyright custom_components
```

Le [quickstart](specs/001-hello-world-update/quickstart.md) décrit les validations dans
Home Assistant Container et dans une configuration HACS séparée.
