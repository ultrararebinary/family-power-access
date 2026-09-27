# Modèle de données : panneau Family Power Access

Ce jalon n'ajoute aucune donnée persistante. Il utilise l'entrée de configuration créée par
la spec 001 pour déterminer la présence de la page dans Home Assistant.

## Entrée de configuration existante

- **Identité** : une seule entrée pour le domaine `family_power_access`, conformément au
  manifeste actuel.
- **Relation** : lorsqu'elle est chargée, cette entrée possède une entrée de navigation et
  une page. Lorsqu'elle est déchargée, le panneau est retiré.
- **Données** : les données actuelles restent vides; aucun paramètre ou secret supplémentaire
  n'est ajouté pour cette page.

## Entrée de navigation

- **Titre visible** : `Family Power Access`.
- **Chemin** : `/family-power-access`, unique dans une instance Home Assistant.
- **Icône** : `mdi:power-plug`.
- **Visibilité** : utilisateurs Home Assistant connectés autorisés à utiliser la navigation;
  aucune restriction administrateur supplémentaire.
- **Cardinalité** : au plus une entrée par instance.
- **Stockage** : état géré en mémoire par Home Assistant, sans fichier propre au projet.

## Page

- **Destination** : la même page est ouverte par l'entrée de navigation.
- **Contenu** : texte statique exact `Hello World`.
- **Interactions** : aucune commande d'appareil, aucun formulaire, aucune donnée enfant.
- **Ressource** : module local inclus dans le dossier de l'intégration et chargé par
  Home Assistant.

## Transitions

| État initial | Événement | État attendu |
| --- | --- | --- |
| Intégration non configurée | Ajout de l'entrée de configuration | Une entrée de navigation est enregistrée |
| Intégration chargée | Sélection de l'entrée | La page affiche `Hello World` |
| Intégration chargée | Rechargement de l'interface ou de l'entrée | Toujours une seule entrée et une seule page |
| Intégration chargée | Déchargement ou suppression de l'entrée | L'entrée disparaît de la navigation |
| Intégration configurée | Redémarrage Home Assistant | L'entrée et la page sont de nouveau enregistrées |

Le chemin statique du module peut rester enregistré en mémoire jusqu'au redémarrage de Home
Assistant après un déchargement; il ne crée pas de point de navigation et ne contient aucune
donnée sensible.
