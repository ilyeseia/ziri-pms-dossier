# ORGANISATION DES UTILISATEURS ET DES RÔLES

Ce document détermine quels employés doivent utiliser ZIRI.PMS et quelles interfaces leur doivent être accessibles.

## 1. MATRICE DES POSTES ET INTERFACES

| Poste | Service | Role Logiciel | Interfaces Accesibles | Permissions | Restrictions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Directeur d'hôtel | Direction | System Manager | Dashboard, Property Form | Consultation, Création, Modification, Validation, Export | Aucun |
| Responsable Finance | Finance | Finance | Folio View, Property Form | Consultation, Modification | Non modification des droits d'utilisateur |
| Chef de réception | Réception | Hotel Admin | Dashboard, Tape Chart, Reservation | Consultation, Modification, Création | Non modification des rôles |
| Réceptionniste | Réception | Front Desk | Dashboard, Tape Chart, Reservation, Folio View | Consultation, Création, Modification | Non accès à la configuration |
| Responsable Revenue | Revenue Manager | Revenue Manager | Rate Plan, Season Form | Consultation, Modification | Accès restreint aux tarifs |
| Gouvernante générale | Housekeeping | Housekeeping Supervisor | HK Board, Room List | Consultation, Modification | Non modification des statuts |
| Caissier | Caisse | Kamra Agent | POS Screen, Cashier Till | Consultation, Modification, Validation | Non accès au Dashboard |
| Responsable maintenance | Maintenance | System Manager | Service Ticket, Room List | Consultation, Modification | Non accès aux interfaces RH |

## 2. MATRICE DE PERMISSIONS

| Fonction | Direction | Finance | Réception | Housekeeping | Maintenance | Caisse | Revenue |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Consultation** | Oui | Oui | Oui | Oui | Oui | Oui | Oui |
| **Création** | Oui | Oui | Oui | Non | Non | Oui | Oui |
| **Modification** | Oui | Oui | Oui | Non | Non | Oui | Oui |
| **Validation** | Oui | Oui | Oui | Non | Non | Oui | Oui |
| **Annulation** | Oui | Oui | Oui | Non | Non | Oui | Non |
| **Export** | Oui | Oui | Non | Non | Non | Non | Oui |
| **Approbation** | Oui | Oui | Oui | Non | Non | Non | Non |

## 3. PRINCIPES DE SÉCURITÉ

1. **Principe du moindre privilège :** Chaque poste ne dispose que des permissions strictement nécessaires.
2. **Séparation des responsabilités :** Le contrôle financier ne revient pas au même que la saisie.
3. **Traçabilité des opérations :** Toutes les actions sont journalisées.
4. **Protection des données clients :** Masquage des identifiants sensibles.

## 4. MODÈLES ORGANISATIONNELS MODÉLISÉS

### Modèle 1 : Hôtel à Équipe Réduite
| Poste | Effectif | Services | Interfaces |
| :--- | :--- | :--- | :--- |
| Directeur | 1 | Tout | Dashboard |
| Réceptionniste | 1 | Réception | Dashboard, POS |
| Gouvernante | 1 | Chambre | HK Board |
| Caissier | 1 | Caisse | POS |

### Modèle 2 : Hôtel à Organisation Intermédiaire
| Poste | Effectif | Services | Interfaces |
| :--- | :--- | :--- | :--- |
| Directeur | 1 | Direction, Finance | Dashboard |
| Réception | 2 | Arrivées, Départs | Dashboard, POS |
| Gouvernante | 1 | Étages | HK Board |
| Caissier | 1 | Caisse | POS |

### Modèle 3 : Hôtel à Organisation Complète
| Poste | Effectif | Services | Interfaces |
| :--- | :--- | :--- | :--- |
| Directeur | 1 | Direction, Finance | Dashboard |
| Sous-Directeurs | 2 | Direction, Finance | Dashboard |
| Réception | 3 | Arrivées, Départs, Groupes | Dashboard, POS |
| Gouvernante | 1 | Étages | HK Board |
| Caissier | 2 | Caisse | POS |

---
**Note :** Ces effectifs sont donnés à titre indicatif et non comme des données réelles du client. La configuration réelle dépendra du besoins de chaque établissement.

## 5. MODÈLES DE RÔLES PAR DÉPARTEMENT

### Modèle Direction & Administration
- Accès complet à toutes les interfaces
- Modification des paramètres système
- Export de rapports complets

### Modèle Réception
- Accès aux arrivées/départs
- Gestion des réservations
- Consultation des folios
- Non accès aux paramètres financiers

### Modèle Housekeeping
- Accès au tableau de bord des chambres
- Mise à jour des statuts
- Non accès aux interfaces financières

### Modèle Caisse / Restauration
- Accès à l'interface POS
- Consultation des comptes clients
- Validation des transactions
- Non accès aux paramètres système

### Modèle Finance
- Accès aux folios et transactions
- Consultation des rapports
- Création de nouveaux comptes
- Non accès aux interfaces opérationnelles