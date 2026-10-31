# FICHE TECHNIQUE — DIRECTION & ADMINISTRATION

## A. IDENTIFICATION
- **Service :** Direction & Administration
- **Module Logiciel :** Kamra Core
- **Niveau de maturité :** Opérationnel
- **Statut d'implémentation :** A
- **Dépendances :** Aucune

## B. PRÉSENTATION MÉTIER
- **Objectif :** Pilotage stratégique de l'établissement.
- **Rôle :** Direction générale et administration.
- **Problèmes résolus :**
  - Paramétrage légal (RC, NIS, AI, NIF)
  - Configuration des règles fiscales (TVA, taxe de séjour)
  - Gestion des paramètres opérationnels (horaires, devise)

## C. FONCTIONNALITÉS CLÉS

| Fonctionnalité | Description | Interface Utilisée | Utilisateur Responsable | Statut |
| :--- | :--- | :--- | :--- | :--- |
| Paramétrage Hôtel | Configuration des données légales et opérationnelles | Property Form | Directeur d'hôtel | A |
| Pilotage Global | Tableau de bord direction | Dashboard | Direction | A |
| Gestion des Saisons | Configuration des périodes tarifaires | Season Form | Responsable Revenue | A |

## D. INTERFACES

| Nom | Type | Route | Objectif | Utilisateurs Autorisés |
| :--- | :--- | :--- | :--- | :--- |
| Dashboard | Tableau de bord | `/ziri` | Pilotage global | Direction, Finance |
| Property Form | Formulaire | `/ziri/property` | Configuration hôtel | Direction |

## E. UTILISATEURS

| Fonction | Responsabilités | Nombre de Profils Types |
| :--- | :--- | :--- |
| Directeur d'hôtel | Configuration globale | 1 |
| Responsable Finance | Paramètres fiscaux | 1 |

## F. PERMISSIONS

| Fonction | Consultation | Création | Modification | Validation | Export |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Directeur d'hôtel | Oui | Oui | Oui | Oui | Oui |
| Responsable Finance | Oui | Non | Oui | Oui | Oui |

## G. FLUX D'INFORMATIONS
- **Données entrantes :**
  - Données légales (RC, NIS)
  - Paramètres fiscaux (TVA, taxe de séjour)
- **Données sortantes :**
  - Rapports de performance
  - Données pour le reporting

## H. PROCÉDURES QUOTIDIENNES
1. Vérification des paramètres fiscaux
2. Mise à jour des données légales
3. Consultation des indicateurs de performance

## I. EXCEPTIONS
- **Problème :** Erreur de configuration fiscale
- **Solution :** Vérification par le Directeur d'hôtel

## J. INDICATEURS DE PERFORMANCE
- Taux d'occupation
- Chiffre d'affaires global
- Nombre de réservations

## K. DÉPENDANCES
- **Matériel :** Aucun
- **Applications externes :** Aucun

## L. LIMITES
- Configuration initiale requise avant utilisation

## M. AMÉLIORATIONS PROPOSÉES
- Intégration avec un système de reporting externe

## N. CRITÈRES D'ACCEPTATION
- Configuration complète des paramètres légaux et fiscaux
- Accès aux rapports de performance

## O. QUESTIONS À POSER AU RESPONSABLE
1. Avez-vous besoin d'une assistance pour la configuration initiale ?
2. Souhaitez-vous intégrer un système de reporting spécifique ?
