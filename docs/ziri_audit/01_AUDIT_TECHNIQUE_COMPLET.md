# RAPPORT D'AUDIT TECHNIQUE COMPLET — ZIRI.PMS

## 1. INFORMATIONS GÉNÉRALES
- **Nom du projet :** ZIRI PMS
- **Version du projet :** 2.6.5
- **Framework :** Frappe Framework v15+
- **Application principale :** `kamra`
- **Modules installés :** `Kamra`, `Smart Access`, `HR Management`, `payments`
- **Architecture :** Monolithe Frappe avec Frontend SPA en React.

## 2. MODULES FONCTIONNELS ET DOCTYPES
L'architecture est organisée autour de DocTypes spécialisés couvrant les opérations hôtelières.

### A. Gestion de l'Établissement (Configuration)
| Fonctionnalité | DocType | Preuve Technique | Statut |
| :--- | :--- | :--- | :--- |
| Paramétrage Hôtel | `Property` | `kamra/doctype/property/` | A |
| Typologie Chambres | `Room Type` | `kamra/doctype/room_type/` | A |
| Inventaire Chambres | `Room` | `kamra/doctype/room/` | A |
| Saisons et Tarifs | `Season`, `Rate Plan` | `kamra/doctype/season/` | A |

### B. Front Office & Réception
| Fonctionnalité | DocType | Preuve Technique | Statut |
| :--- | :--- | :--- | :--- |
| Réservations | `Reservation` | `kamra/doctype/reservation/` | A |
| Fiches Clients | `Guest` | `kamra/doctype/guest/` | A |
| Enregistrement (Check-in) | `Check In` | `kamra/doctype/check_in/` | A |
| Clôture (Check-out) | `Check Out` | `kamra/doctype/check_out/` | A |
| Main courante / Planning | N/A | `frontend/src/screens/TapeChart.tsx` | A |

### C. Caisse et Facturation
| Fonctionnalité | DocType | Preuve Technique | Statut |
| :--- | :--- | :--- | :--- |
| Comptes de séjour | `Folio` | `kamra/doctype/folio/` | A |
| Transactions | `Folio Ledger Entry` | `kamra/doctype/folio_ledger_entry/` | A |
| Paiements | `Folio Payment` | `kamra/doctype/folio_payment/` | A |
| Sessions de caisse | `Cashier Session` | `kamra/doctype/cashier_session/` | A |

### D. Restauration & Points de Vente (POS)
| Fonctionnalité | DocType | Preuve Technique | Statut |
| :--- | :--- | :--- | :--- |
| Configuration PDV | `POS Outlet` | `kamra/doctype/pos_outlet/` | A |
| Prise de commande | `POS Order` | `kamra/doctype/pos_order/` | A |
| Carte / Menus | `Menu Item` | `kamra/doctype/menu_item/` | A |
| Interface Caisse | N/A | `frontend/src/screens/POS.tsx` | A |

### E. Service des Étages (Housekeeping)
| Fonctionnalité | DocType | Preuve Technique | Statut |
| :--- | :--- | :--- | :--- |
| Suivi des tâches | `Housekeeping Task` | `kamra/doctype/housekeeping_task/` | A |
| Tableau de bord | N/A | `frontend/src/screens/HousekeepingBoard.tsx` | A |
| Objets trouvés | `Lost and Found Item` | `kamra/doctype/lost_and_found_item/` | A |

### F. Contrôle d'Accès (Smart Access)
| Fonctionnalité | DocType | Preuve Technique | Statut |
| :--- | :--- | :--- | :--- |
| Gestion des serrures | `Smart Lock` | `kamra/smart_access/doctype/smart_lock/` | A |
| Cartes d'accès | `Lock Credential` | `kamra/smart_access/doctype/lock_credential/` | A |
| Commandes à distance | `Lock Command` | `kamra/smart_access/doctype/lock_command/` | B |

### G. Ressources Humaines & Paie (HR Management)
| Fonctionnalité | DocType | Preuve Technique | Statut |
| :--- | :--- | :--- | :--- |
| Fiches employés | `HR Employee` | `kamra/doctype/hr_employee/` | A |
| Contrats de travail | `HR Contract` | `kamra/doctype/hr_contract/` | A |
| Types de congés | `HR Leave Type` | `kamra/doctype/hr_leave_type/` | A |
| Demandes congés | `HR Leave Application` | `kamra/doctype/hr_leave_application/` | A |
| Pointage journalier | `HR Attendance` | `kamra/doctype/hr_attendance/` | A |
| Overtime | `HR Overtime` | `kamra/doctype/hr_overtime/` | A |
| Structure salaire | `HR Salary Structure` | `kamra/doctype/hr_salary_structure/` | A |
| Bulletins de paie | `HR Salary Slip` | `kamra/doctype/hr_salary_slip/` | A |
| Moteur paie Algérie | N/A | `kamra/hr/payroll/algeria_payroll.py` | A |
| Processeur pointage | N/A | `kamra/hr/attendance/processor.py` | A |
| Dashboard RH | N/A | `frontend/src/hr/screens/HRDashboard.tsx` | A |
| Journal pointage | N/A | `frontend/src/hr/screens/AttendanceLog.tsx` | A |
| Bulletins paie UI | N/A | `frontend/src/hr/screens/PayslipView.tsx` | A |

## 3. INTERFACES ET ROUTES FRONTEND
ZIRI.PMS utilise une interface moderne en React montée sur `/ziri`.

| Route | Écran | Utilisateur Cible | Statut |
| :--- | :--- | :--- | :--- |
| `/ziri` | Tableau de bord | Direction / Réception | A |
| `/ziri/tape-chart` | Planning des chambres | Réception | A |
| `/ziri/pos` | Caisse Point de Vente | Caissier Restaurant | A |
| `/ziri/hk` | Service des étages | Gouvernante | A |
| `/ziri/hr` | Dashboard RH | Responsable RH | A |
| `/ziri/hr/employees` | Liste employés | RH / Direction | A |
| `/ziri/hr/leaves` | Suivi congés | RH / Manager | A |
| `/ziri/hr/attendance` | Journal pointage | RH / Pointeur | A |
| `/ziri/hr/payslips` | Bulletins paie | RH / Comptable | A |
| `/ziri/book` | Réservation publique | Client | A |

## 4. LOCALISATION ALGÉRIENNE
Le système intègre nativement les spécificités du marché algérien :
- **Devise :** Dinars Algériens (DZD).
- **Fiscalité :** Gestion de la TVA et taxe de séjour.
- **Cotisations sociales :** CNSS (26% patronal / 9% salarial), CNAS (1.5% patronal / 0.5% salarial).
- **Impôts :** Barème IRG 2024 avec abattement professionnel (10%).
- **Documents légaux :** Champs pour RC, NIS, AI et NIF (DocType `Property`).
- **Traduction :** Interface disponible en Français et Arabe.

## 5. STATUT GÉNÉRAL DE MATURITÉ
- **Noyau PMS :** Très Mature (A).
- **POS / Restauration :** Opérationnel (A).
- **Ressources Humaines & Paie :** Opérationnel complet (A).
- **Smart Access :** En cours de finalisation (B/F).
- **Reporting :** Opérationnel (A).

**Légende des statuts :**
- **A :** Implémenté et vérifié.
- **B :** Partiellement implémenté.
- **F :** Dépendant d'équipement externe.

