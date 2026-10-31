# FICHE TECHNIQUE — RESSOURCES HUMAINES (VERSION COMPLÈTE)

## A. IDENTIFICATION
- **Service :** Ressources Humaines
- **Module :** HR Management
- **Niveau de maturité :** En développement (C → A cible)
- **Statut d'implémentation :** C (Structure technique existante uniquement)
- **Dépendances :** Module Pointage, Smart Access (cartes personnel)

## B. PRÉSENTATION MÉTIER
- **Objectif :** Gestion complète du cycle de vie des employés
- **Rôle dans l'hôtel :** Administration du personnel, conformité sociale, coûts de personnel
- **Problèmes résolus :**
  - Fiches employés centralisées
  - Planning des équipes et rotations
  - Gestion congés/absences avec validation
  - Contrats et avenants
  - Calcul masse salariale
  - Rapports légaux (CNSS, CNAS, IRG)

## C. FONCTIONNALITÉS DÉTAILLÉES

| N° | Fonctionnalité | Description | Utilité | Interface | Utilisateur responsable | Statut | Preuve technique |
|---|---|---|---|---|---|---|---|
| 1 | Fiche Employé | Données personnelles, contact, poste, département, manager | Référentiel unique | Employee Form | RH | C | À créer |
| 2 | Contrat | Type CDI/CDD/Stage, dates, salaire, coefficients | Base légale | Contract Form | RH | C | À créer |
| 3 | Planning Équipes | Rotations par service, quarts jour/nuit, remplacements | Organisation | Schedule Board | Chef service | C | À créer |
| 4 | Demandes Congés | Congés annuels, maladie, maternité, exceptionnels | Workflow validation | Leave Request | Employé/RH | C | À créer |
| 5 | Absences/Retards | Suivi pointage, justification, régularisation | Discipline | Attendance Log | RH/Manager | C | À créer |
| 6 | Heures Supplémentaires | Calcul taux (125%, 150%, 200%), récupération | Paie | Overtime Log | RH | C | À créer |
| 7 | Bulletins Paie | Génération mensuelle, cotisations CNSS/CNAS/IRG | Conformité | Payslip | RH/Comptable | C | À créer |
| 8 | Avances/Salaires | Demande avance, retenue mensuelle | Trésorerie | Salary Advance | RH | C | À créer |
| 9 | Fin Contrat | Démission, licenciement, retraite, solde tout compte | Juridique | Exit Process | RH | C | À créer |
| 10 | Documents RH | Contrats, avenants, certificats, attestations | Archive | Document Manager | RH | C | À créer |
| 11 | Formation | Plan formation, suivi compétences, certifications | Développement | Training | RH | C | À créer |
| 12 | Évaluation | Entretiens annuels, objectifs, grille évaluation | Performance | Appraisal | Manager/RH | C | À créer |
| 13 | Notes de Frais | Remboursement frais déplacement, repas | Trésorerie | Expense Claim | RH/Finance | C | À créer |
| 14 | Rapports Légaux | DPAE, DSN, registre unique, livre paie | Conformité Algérie | Legal Reports | RH | C | À créer |

## D. INTERFACES UTILISATEUR

| Nom | Type | Route | Objectif | Actions possibles | Utilisateurs autorisés |
|---|---|---|---|---|---|
| Employee List | Liste | `/ziri/hr/employees` | Annuaire personnel | Filtrer, exporter, créer | RH, Direction |
| Employee Form | Formulaire | `/ziri/hr/employee/{id}` | Fiche complète | Voir, modifier, documents | RH, Manager (lecture) |
| Contract Form | Formulaire | `/ziri/hr/contract/{id}` | Gestion contrat | Créer, renouveler, rompre | RH |
| Schedule Board | Tableau | `/ziri/hr/schedule` | Planning équipes | Glisser-déposer, publier | Chef service, RH |
| Leave Dashboard | Tableau | `/ziri/hr/leaves` | Suivi congés | Valider, rejeter, solde | RH, Manager |
| Attendance Log | Liste | `/ziri/hr/attendance` | Pointage journalier | Corriger, valider | RH, Pointeur |
| Payslip View | Formulaire | `/ziri/hr/payslip/{id}` | Bulletin paie | Générer, PDF, email | RH, Comptable |
| HR Dashboard | Tableau de bord | `/ziri/hr` | KPI RH | Effectifs, coûts, absences | RH, Direction |

## E. UTILISATEURS ET RÔLES

| Fonction | Responsabilités | Profils types | Relations hiérarchiques |
|---|---|---|---|
| Responsable RH | Stratégie RH, paie, légal, recrutement | 1 | Directeur Général |
| Gestionnaire Paie | Bulletin, cotisations, déclarations | 1-2 | Responsable RH |
| Gestionnaire Personnel | Contrats, dossiers, entrées/sorties | 1-2 | Responsable RH |
| Chef de Département | Planning, validation congés, évaluations | Par service | Directeur Exploitation |
| Employé | Demandes congés, voir bulletins, pointage | Tous | Chef direct |

## F. MATRICE DE PERMISSIONS

| Fonction | Consultation | Création | Modification | Validation | Annulation | Export | Approbation |
|---|---|---|---|---|---|---|---|
| Responsable RH | Oui | Oui | Oui | Oui | Oui | Oui | Oui |
| Gestionnaire Paie | Oui | Oui | Oui | Oui | Non | Oui | Non |
| Gestionnaire Personnel | Oui | Oui | Oui | Non | Non | Oui | Non |
| Chef Département | Oui (son service) | Non | Non | Oui (congés) | Non | Non | Oui |
| Employé | Oui (propre) | Oui (demandes) | Non | Non | Oui (propres) | Non | Non |

## G. FLUX D'INFORMATIONS

**Données entrantes :**
- Nouvelles embauches (recrutement)
- Données pointage (pointeuse/biométrique)
- Demandes employés (congés, avances, frais)
- Paramètres légaux (SMIG, taux cotisations, IRG)

**Données sortantes :**
- Bulletins de paie (PDF/Email)
- Déclarations CNSS/CNAS mensuelles
- DPAE (Déclaration Préalable À l'Embauche)
- Registre unique du personnel
- États coûts personnel par service
- Rapports pour Expert-Comptable

**Documents générés :**
- Contrats de travail (AR/FR)
- Avenants
- Certificats de travail
- Attestations employeur
- Bulletins de paie
- Solde tout compte

**Notifications :**
- Validation congés (email/push)
- Échéances contrats (30j, 15j)
- Anomalies pointage (quotidien)
- Échéances visites médicales

**Données partagées :**
- Avec Pointage : plannings, employés actifs
- Avec Smart Access : cartes personnel, zones accès
- Avec Finance : coûts personnel, avances, notes frais
- Avec Réception : planning réceptionnistes

## H. PROCÉDURES QUOTIDIENNES

1. **Matin :** Vérification pointage, anomalies (absences non justifiées)
2. **Quotidien :** Validation demandes congés en attente
3. **Hebdo :** Révision planning semaine suivante
4. **Mensuel (J+1 à J+5) :** 
   - Clôture pointage
   - Calcul heures sup
   - Génération bulletins
   - Déclarations CNSS/CNAS
   - Virement salaires
5. **Événementiel :** Gestion entrées/sorties, visites médicales

## I. EXCEPTIONS ET CAS PARTICULIERS

| Situation | Traitement | Acteurs |
|---|---|---|
| Absence injustifiée > 48h | Mise en demeure, procédure disciplinaire | RH + Manager |
| Accident travail | Déclaration 48h, certificat médical, AT/MP | RH + Médecin travail |
| Congé maladie > 6 mois | Inaptitude, reclassement, licenciement | RH + Médecin + Juridique |
| Grève | Suivi grévistes, réquisitions, paie | RH + Direction |
| Pic activité (saison) | CDD saisonniers, intérim, heures sup | RH + Managers |

## J. INDICATEURS DE PERFORMANCE (KPI RH)

| Indicateur | Formule | Fréquence | Cible |
|---|---|---|---|
| Effectif total | CDI + CDD + Stagiaires | Mensuel | Selon budget |
| Taux turnover | (Sorties / Effectif moyen) × 100 | Mensuel | < 15% |
| Taux absentéisme | (Jours absence / Jours théoriques) × 100 | Mensuel | < 5% |
| Coût personnel / CA | Masse salariale / CA HT | Mensuel | < 30% |
| Heures sup / Heures normales | Ratio | Mensuel | < 10% |
| Délai traitement congés | Jours demande → validation | Mensuel | < 3j |
| Taux formation | Employés formés / Effectif | Annuel | > 50% |

## K. DÉPENDANCES ET INTÉGRATIONS

| Dépendance | Type | Détail |
|---|---|---|
| Module Pointage | Interne | Import quotidien, biométrique/RFID |
| Smart Access | Interne | Cartes personnel, zones, horaires |
| Finance/Comptabilité | Interne | Écritures paie, avances, notes frais |
| Paie Externe | Externe | Export SAGE/CEGID/EBP (format DSN) |
| CNSS/CNAS | Externe | API/Télédéclaration Algérie |
| Médecine Travail | Externe | Suivi visites, inaptitudes |
| Expert-Comptable | Externe | Export FEC, livre paie |

## L. LIMITES ACTUELLES (VERSION AUDITÉE)

1. **Aucun DocType Employee/Contract/Leave/Attendance/Payslip** dans le code
2. **Aucune interface RH** dans le frontend React
3. **Aucun contrôleur Python** pour workflows RH
4. **Pas d'intégration pointeuse** (biométrique, RFID, badge)
5. **Pas de moteur paie** (calcul cotisations Algérie)
6. **Pas de déclarations légales** (CNSS, CNAS, IRG, DSN)
7. **Pas de gestion documents RH** (contrats, certificats)

## M. AMÉLIORATIONS PROPOSÉES (ROADMAP)

| Priorité | Élément | Effort | Description |
|---|---|---|---|
| **P0 - Indispensable** | DocTypes Employee, Contract, Leave, Attendance, Payslip | 3 sem | Structure données complète |
| **P0 - Indispensable** | Employee Form, Leave Request, Schedule Board | 2 sem | Interfaces utilisateurs |
| **P0 - Indispensable** | Moteur paie Algérie (CNSS 26%, CNAS 1.5%, IRG progressif) | 3 sem | Calculs conformes |
| **P0 - Indispensable** | Import pointeuse (CSV/API), validation anomalies | 1 sem | Automatisation pointage |
| **P1 - Important** | Workflow congés (demande → manager → RH) | 1 sem | Processus validation |
| **P1 - Important** | Génération bulletins PDF + email | 1 sem | Distribution dématérialisée |
| **P1 - Important** | Déclarations CNSS/CNAS mensuelles | 2 sem | Conformité légale |
| **P1 - Important** | Planning équipes avec quarts jour/nuit | 1 sem | Organisation opérationnelle |
| **P2 - Souhaitable** | Gestion formation et compétences | 1 sem | Développement RH |
| **P2 - Souhaitable** | Évaluation annuelle 360° | 1 sem | Performance |
| **P3 - Évolution** | Portail employé (self-service) | 2 sem | Autonomie employés |
| **P3 - Évolution** | Intégration SAGE/CEGID compta | 1 sem | Échange données |

## N. CRITÈRES D'ACCEPTATION MODULE RH

Le module RH est prêt pour déploiement hôtelier quand :

- [ ] 5 DocTypes créés et migrés (Employee, Contract, Leave, Attendance, Payslip)
- [ ] 4 interfaces React fonctionnelles (List, Form, Board, Dashboard)
- [ ] Workflow congés validé (création → validation manager → validation RH)
- [ ] Calcul paie testé sur 3 mois avec cas réels (CDI, CDD, temps partiel, heures sup)
- [ ] Déclaration CNSS/CNAS générée et format validé
- [ ] Import pointeuse testé (fichier test fourni par client)
- [ ] Rapports légaux (registre unique, DPAE) conformes inspection travail
- [ ] Permissions testées selon matrice (5 profils)
- [ ] Documents générés : contrat, bulletin, certificat, solde tout compte
- [ ] Intégration Smart Access : carte personnel → zone/horaire

## O. QUESTIONS À POSER AU RESPONSABLE RH

1. **Effectifs :** Combien d'employés par type (CDI, CDD, saisonniers, stagiaires) ?
2. **Conventions :** Convention collective applicable ? (Hôtellerie/Restauration)
3. **Horaires :** Quarts de travail (jour/nuit/continu) ? Durée hebdo (40h/44h/48h) ?
4. **Congés :** Politique congés (30j/an ? fractionnement ? ancienneté ?)
5. **Paie :** Externalisée ou internalisée ? Logiciel actuel (SAGE, CEGID, EBP, Excel) ?
6. **Cotisations :** Taux CNSS/CNAS applicables ? Exonérations (jeunes, zones) ?
7. **Pointage :** Matériel actuel (marque/modèle) ? Export possible ? Biométrie ?
8. **Avantages :** Primes (ancienneté, rendement, panier, transport) ? Logement ?
9. **Médecine travail :** Médecin désigné ? Fréquence visites ?
10. **Documents :** Modèles contrats, certificats, attestations actuels ?
11. **Budget :** Masse salariale cible ? Ratio personnel/CA ?
12. **Formation :** Plan formation existant ? Organismes partenaires ?

---

*Cette fiche technique définit le périmètre complet du module RH à développer pour ZIRI.PMS. Elle sert de base au cahier des charges de développement.*