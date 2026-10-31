# INVENTAIRE DÉTAILLÉ DES POINTS DE VENTE (POS) — ZIRI.PMS

ZIRI.PMS inclut un module POS complet intégré, capable de gérer divers points de vente hôteliers avec transfert automatique vers les comptes chambres.

## 1. CAPACITÉS POS GÉNÉRALES
- **Multi-Outlet :** Gestion illimitée de points de vente (Restaurants, Bars, Spa).
- **Intégration :** Transfert direct des charges vers le `Folio` du client.
- **Gestion des stocks :** Décrémentation automatique des ingrédients lors de la vente.
- **Clôture :** Sessions de caisse par caissier et par outlet.
- **Support technique :** Écrans de préparation cuisine / bar.

## 2. INVENTAIRE DES POS IDENTIFIÉS (CONFIGURATION)
D'après les tables de configuration, voici les types de POS supportés :

| Point de Vente | Type | État de Configuration |
| :--- | :--- | :--- |
| Restaurant Principal | Restaurant | Configurable |
| Bar de l'hôtel | Bar | Configurable |
| Room Service | Room Service | Configurable |
| Centre de Bien-être | Spa | Configurable |
| Snack Piscine | Other | Configurable |

## 3. FICHE TECHNIQUE DÉTAILLÉE D'UN POS

| Caractéristique | Spécification |
| :--- | :--- |
| **Logiciel de caisse** | Interface POS React (Kamra) |
| **Modes de paiement** | Espèces, Carte bancaire, Transfert chambre |
| **Transfert sur chambre** | Oui, en temps réel |
| **Lien avec stock** | Oui, via `Menu Item Ingredient` |
| **Préparation** | Interface Kitchen intégrée |
| **Gestion des tables** | Support des plans de salle (T1, T2...) |

## 4. DÉSIGNATION COMMERCIALE
Le système est prêt pour le déploiement multi-points de vente. Pour un déploiement, nous devons valider :
1. Le nombre réel de points de vente par établissement.
2. Le besoin d'écrans de cuisine (KDS) séparés.
3. Le besoin d'imprimantes thermiques locales.
4. Les règles de TVA par point de vente.

---
**Attention :** Ces points de vente sont configurables. Leur mise en production nécessite une saisie exhaustive du menu, des tarifs et des ingrédients par le client.
