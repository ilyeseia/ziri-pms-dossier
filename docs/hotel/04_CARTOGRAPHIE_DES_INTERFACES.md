# CARTOGRAPHIE DES INTERFACES UTILISATEURS — ZIRI.PMS

Ce document répertorie toutes les interfaces utilisateurs disponibles dans ZIRI.PMS, classées par service et type.

## 1. TABLEAU RÉCAPITULATIF DES INTERFACES

| N° | Service | Nom de l'Interface | Type | Utilisateur Cible | Route | Fonction Principale | Statut |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direction | Dashboard | Tableau de bord | Direction | `/ziri` | Pilotage global | Opérationnel |
| 2 | Réception | Tape Chart | Liste | Réception | `/ziri/tape-chart` | Planning des chambres | Opérationnel |
| 3 | Réservations | CRS Screen | Formulaire | Réception | `/ziri/crs` | Gestion des réservations | Opérationnel |
| 4 | Hébergement | Room List | Liste | Réception | `/ziri/rooms` | Inventaire des chambres | Opérationnel |
| 5 | Caisse | Folio View | Formulaire | Réception | `/ziri/folio/{folio}` | Gestion des comptes | Opérationnel |
| 6 | Service des Étages | HK Board | Tableau de bord | Gouvernante | `/ziri/hk` | Suivi des tâches | Opérationnel |
| 7 | Restauration | POS Screen | Interface | Caissier | `/ziri/pos` | Prise de commande | Opérationnel |
| 8 | Banquets | Banquet Screen | Formulaire | Banquet | `/ziri/banquet` | Gestion des événements | Opérationnel |
| 9 | Smart Access | Smart Lock Dashboard | Tableau de bord | Réception | `/ziri/smart-access` | Gestion des serrures | Partiel |
| 10 | Public | Public Booking | Page Web | Client | `/book` | Réservation en ligne | Opérationnel |

## 2. RÉSUMÉ PAR SERVICE

| Service | Pages | Listes | Formulaires | Tableaux de bord | Rapports | Interfaces Publiques | Total |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Direction | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 2 |
| Réception | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 6 |
| Hébergement | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| Caisse | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 2 |
| Service des Étages | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 2 |
| Restauration | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| Banquets | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 2 |
| Smart Access | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| Public | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |

## 3. INTERFACES NON VÉRIFIABLES

- **Mobile App Housekeeping** : Non implémenté dans la version actuelle.
- **Tableau de bord Smart Access** : En cours de développement.

**Total d'interfaces vérifiées :** 12
