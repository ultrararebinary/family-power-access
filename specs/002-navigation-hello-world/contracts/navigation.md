# Contrat UI : navigation Family Power Access

Ce contrat relie les exigences de [spec.md](../spec.md) à la page que l'utilisateur voit dans
Home Assistant. Il ne définit pas de nouvelle API métier.

## Entrée de navigation

- **Libellé** : `Family Power Access`, exactement une fois lorsque l'intégration est chargée.
- **Chemin** : `/family-power-access`.
- **Icône** : `mdi:power-plug`.
- **Accès** : utilisateurs connectés qui peuvent utiliser la navigation Home Assistant.
- **Activation** : apparaît automatiquement après l'ajout de l'intégration, sans édition d'un
  tableau de bord ni de `configuration.yaml`.
- **Retrait** : disparaît lorsque l'entrée de configuration est déchargée ou supprimée.

## Page ouverte

- L'entrée ouvre une page dédiée dans l'interface Home Assistant.
- Le texte `Hello World` est visible sans interaction supplémentaire.
- La page est lisible dans une fenêtre normale et dans une fenêtre étroite.
- Ce jalon ne présente aucun contrôle de prise, code enfant, calendrier, quota ou historique.
- La page ne dépend pas d'un service externe pour afficher son contenu.

## Cycle de vie

- Un rechargement de l'interface, un rechargement de l'intégration et un redémarrage normal
  conservent l'accès à la page et n'ajoutent aucun doublon.
- Un chemin de panneau déjà occupé ne doit pas être remplacé silencieusement; l'échec de
  configuration doit être visible dans les diagnostics Home Assistant.
- Le capteur `Hello World` livré par la spec 001 conserve son comportement.

## Ressource de panneau

Le module frontend fait partie de `custom_components/family_power_access/`, afin que les
releases HACS contiennent à la fois l'intégration et sa page. Son URL interne est une ressource
statique de l'intégration; elle ne contient aucune donnée privée. L'interface Home Assistant
gère l'authentification de la page et la navigation vers celle-ci.
