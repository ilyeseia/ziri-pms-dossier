# INVENTAIRE EXHAUSTIF DES SERVICES HÔTELIERS — ZIRI.PMS

Ce document répertorie les services hôteliers couverts par la solution ZIRI.PMS, les modules correspondants et leur état de disponibilité.

## 1. TABLEAU RÉCAPITULATIF DES SERVICES

| N° | Service Hôtelier | Module Logiciel | Fonctionnalités Clés | Interfaces | Statut |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Direction & Admin** | Kamra Core | Pilotage, KPI, Paramétrage légal (RC/NIS) | Dashboard, Property Form | Opérationnel |
| 2 | **Réception** | Front Office | Check-in, Check-out, Main courante | Tape Chart, Reservation Detail | Opérationnel |
| 3 | **Réservations** | Booking Engine | Réservations individuelles, groupes, directes | CRS Screen, Public Booking | Opérationnel |
| 4 | **Hébergement** | Room Mgmt | Statuts de chambres, Inventaire | Room List, Status Board | Opérationnel |
| 5 | **Revenue Mgmt** | Pricing Engine | Plans tarifaires, Saisons, Restrictions | Rate Plan, Season Form | Opérationnel |
| 6 | **Caisse & Facturation** | Finance | Folios, Paiements, Sessions de caisse | Folio View, Cashier Till | Opérationnel |
| 7 | **Service des Étages** | Housekeeping | Planning nettoyage, Objets trouvés | HK Board, Mobile App | Opérationnel |
| 8 | **Restauration** | F&B / POS | Gestion des tables, Commandes cuisine | POS Screen, Kitchen Display | Opérationnel |
| 9 | **Banquets & Évènements**| Banquet | Devis, Menus banquets, Planning salles | Banquet Screen, Function Form | Opérationnel |
| 10 | **Maintenance** | Technical | Bons d'intervention, Suivi des pannes | Service Ticket | Opérationnel |
| 11 | **Ressources Humaines** | HR (Basic) | Pointage, Passations de consigne | Shift Handover | Partiel |
| 12 | **Smart Access** | Smart Access | Gestion des serrures, Cartes magnétiques | Smart Lock Dashboard | Partiel (F) |
| 13 | **Stocks & Achats** | Inventory | Gestion des ingrédients, Stocks PDV | Inventory Screen | Opérationnel |

## 2. STATISTIQUES RÉELLES

- **Nombre de services hôteliers identifiés :** 13
- **Nombre de modules logiciels distincts :** 5 (Kamra Core, POS, HK, Banquet, Smart Access)
- **Nombre de fonctionnalités vérifiées :** ~85
- **Services 100% Opérationnels :** 11
- **Services Partiels :** 2 (RH, Smart Access)
- **Services nécessitant un équipement externe :** 1 (Smart Access - Serrures)

## 3. MÉTHODE DE COMPTAGE
Le comptage est basé sur l'existence combinée de :
1. Un **DocType** dédié dans le backend.
2. Une **Interface utilisateur** spécifique (React Screen ou Workspace).
3. Un **Workflow métier** identifiable dans le code Python (`controller.py` ou `api.py`).

---

**Note pour le client :**
ZIRI.PMS couvre l'intégralité du cycle de vie du client, de la réservation en ligne jusqu'au départ, en incluant la gestion complète des points de vente et du service technique.
