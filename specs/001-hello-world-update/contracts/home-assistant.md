# Contrat Home Assistant: installation et Hello World

## Flux de configuration

- **Nom**: `Family Power Access`.
- **Domaine**: `family_power_access`.
- **Ajout**: Le parent choisit l'intégration dans *Settings → Devices & services → Add
  integration*. Le seul écran d'ajout confirme la création; aucun champ d'appareil, de compte ou
  de code n'est demandé.
- **Unicité**: Une seconde tentative d'ajout indique que l'intégration est déjà configurée.
- **Déchargement**: Le retrait de l'entrée décharge proprement l'entité.

## Entité exposée

| Propriété | Contrat observable |
| --- | --- |
| Type | Capteur |
| Nom | « Hello World » dans l'interface |
| État | `Hello World` |
| Identifiant unique | Stable entre ajout, rechargement et redémarrage |
| Connexion GitHub | Aucune pour lire ou conserver l'état |

L'identifiant d'entité attribué par Home Assistant peut être renommé par l'utilisateur; les
vérifications doivent donc se baser sur l'identifiant unique ou l'entrée de configuration, pas
uniquement sur un nom d'entité présumé.

## Limites de cette version

Aucune entité prise électrique, clavier, calendrier, quota ou historique enfant n'est exposée.
Aucune donnée sensible ni donnée de compte GitHub n'est enregistrée par cette intégration.

## Références

[Flux de configuration](https://developers.home-assistant.io/docs/core/integration/config_flow/),
[entrées de configuration](https://developers.home-assistant.io/docs/config_entries_index/),
[entités](https://developers.home-assistant.io/docs/core/entity/),
[traductions](https://developers.home-assistant.io/docs/internationalization/custom_integration/).
