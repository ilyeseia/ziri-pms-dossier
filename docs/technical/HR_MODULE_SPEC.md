# DOCUMENTATION TECHNIQUE — MODULE RH (HR MANAGEMENT)

## Architecture du module

Le module RH sera organisé comme une app Frappe dédiée `ziri_hr` ou intégré dans `kamra` avec les DocTypes suivants :

### 1. DocTypes à créer

| DocType | Nom interne | Description | Champs clés |
|---|---|---|---|
| Employee | `HR Employee` | Fiche employé | employee_id, first_name, last_name, email, phone, department, designation, employment_type, date_of_joining, status, manager, user_id, bank_account, cnss_number |
| Contract | `HR Contract` | Contrat de travail | employee, contract_type, start_date, end_date, salary_base, salary_gross, working_hours, coefficient, status |
| Leave Type | `HR Leave Type` | Types de congés | leave_type_name, max_days, is_carry_forward, requires_approval |
| Leave Application | `HR Leave Application` | Demande congé | employee, leave_type, from_date, to_date, total_days, status, approved_by |
| Attendance | `HR Attendance` | Pointage journalier | employee, attendance_date, check_in, check_out, working_hours, overtime_hours, status, device_id |
| Overtime | `HR Overtime` | Heures supplémentaires | employee, date, hours, rate_multiplier, status, approved_by |
| Salary Structure | `HR Salary Structure` | Structure de paie | name, component, amount, type (earning/deduction), condition |
| Salary Slip | `HR Salary Slip` | Bulletin de paie | employee, payroll_period, earnings, deductions, net_pay, status |
| Payroll Entry | `HR Payroll Entry` | Lancement paie | period, department, status, salary_slips |
| Expense Claim | `HR Expense Claim` | Note de frais | employee, expense_date, category, amount, status |
| Employee Document | `HR Employee Document` | Documents RH | employee, document_type, file, expiry_date |
| Training | `HR Training` | Formation | employee, training_name, provider, date, status, cost |
| Appraisal | `HR Appraisal` | Évaluation | employee, period, scores, reviewer, status |

### 2. Controllers Python (kamra/hr/)

```
kamra/hr/
├── __init__.py
├── doctype/
│   ├── hr_employee/
│   │   ├── __init__.py
│   │   ├── hr_employee.py
│   │   ├── hr_employee.json
│   │   └── test_hr_employee.py
│   ├── hr_contract/
│   ├── hr_leave_application/
│   ├── hr_attendance/
│   ├── hr_overtime/
│   ├── hr_salary_structure/
│   ├── hr_salary_slip/
│   ├── hr_payroll_entry/
│   ├── hr_expense_claim/
│   ├── hr_employee_document/
│   ├── hr_training/
│   └── hr_appraisal/
├── payroll/
│   ├── __init__.py
│   ├── algeria_payroll.py      # Calculs spécifiques Algérie
│   ├── cnss_cnas_calculator.py
│   └── irg_calculator.py
├── attendance/
│   ├── __init__.py
│   ├── processor.py            # Import/traitement pointage
│   └── anomaly_detector.py
├── reports/
│   ├── __init__.py
│   ├── payroll_register.py
│   ├── cnss_declaration.py
│   ├── cnas_declaration.py
│   └── workforce_report.py
└── api/
    ├── __init__.py
    ├── employee_api.py
    ├── leave_api.py
    ├── attendance_api.py
    └── payroll_api.py
```

### 3. Frontend React (frontend/src/hr/)

```
frontend/src/hr/
├── screens/
│   ├── EmployeeList.tsx
│   ├── EmployeeForm.tsx
│   ├── ContractForm.tsx
│   ├── ScheduleBoard.tsx
│   ├── LeaveDashboard.tsx
│   ├── AttendanceLog.tsx
│   ├── PayslipView.tsx
│   └── HRDashboard.tsx
├── components/
│   ├── EmployeeCard.tsx
│   ├── LeaveRequestCard.tsx
│   ├── ShiftSelector.tsx
│   ├── PayrollCalculator.tsx
│   └── DocumentViewer.tsx
├── hooks/
│   ├── useEmployees.ts
│   ├── useLeaveRequests.ts
│   ├── useAttendance.ts
│   └── usePayroll.ts
└── api/
    ├── employeeApi.ts
    ├── leaveApi.ts
    ├── attendanceApi.ts
    └── payrollApi.ts
```

### 4. Routes à ajouter (frontend/src/lib/routing.ts)

```typescript
const HR_ROUTES = {
  employees: '/ziri/hr/employees',
  employee: '/ziri/hr/employee/:id',
  contract: '/ziri/hr/contract/:id',
  schedule: '/ziri/hr/schedule',
  leaves: '/ziri/hr/leaves',
  attendance: '/ziri/hr/attendance',
  payslip: '/ziri/hr/payslip/:id',
  dashboard: '/ziri/hr',
};
```

### 5. Rôles Frappe à créer

| Rôle | Description | Permissions |
|---|---|---|
| HR Manager | Responsable RH complet | All HR DocTypes: read, write, create, delete, submit, cancel, amend |
| HR Payroll Officer | Gestionnaire paie | Salary Slip, Payroll Entry, Salary Structure: read, write, create, submit |
| HR Staff Officer | Gestionnaire personnel | Employee, Contract, Employee Document: read, write, create |
| Department Head | Chef de département | Leave Application (own dept): read, write; Attendance (own dept): read |
| Employee Self Service | Employé | Leave Application (own): read, write, create; Attendance (own): read; Salary Slip (own): read |

### 6. Workflows à implémenter

**Workflow Demande Congé :**
```
Draft → Submitted (Employee) → Approved by Manager → Approved by HR → Approved
                      ↓
                 Rejected (Manager/HR) → Rejected
```

**Workflow Bulletin Paie :**
```
Draft → Calculated → Verified (Payroll Officer) → Submitted (HR Manager) → Paid
                      ↓
                 Cancelled
```

**Workflow Pointage :**
```
Raw Import → Processed → Anomalies Detected → Validated (HR) → Closed
```

### 7. Calculs Paie Algérie (kamra/hr/payroll/algeria_payroll.py)

```python
# Cotisations Sociales Algérie 2024
CNSS_EMPLOYER_RATE = 0.26      # 26% part patronale
CNSS_EMPLOYEE_RATE = 0.09      # 9% part salariale
CNAS_EMPLOYER_RATE = 0.015     # 1.5% part patronale
CNAS_EMPLOYEE_RATE = 0.005     # 0.5% part salariale

# IRG Tranches 2024 (revenu net imposable annuel)
IRG_BRACKETS = [
    (0, 120000, 0.00),
    (120000, 360000, 0.20),
    (360000, 1440000, 0.30),
    (1440000, float('inf'), 0.35),
]

# SMIG 2024
SMIG_MONTHLY = 20000  # DA

def calculate_net_salary(gross: float) -> dict:
    """Calcule le salaire net avec cotisations et IRG"""
    cnss_employee = gross * CNSS_EMPLOYEE_RATE
    cnas_employee = gross * CNAS_EMPLOYEE_RATE
    taxable = gross - cnss_employee - cnas_employee
    irg = calculate_irg(taxable * 12) / 12  # Mensualisé
    net = taxable - irg
    return {
        'gross': gross,
        'cnss_employee': cnss_employee,
        'cnas_employee': cnas_employee,
        'taxable': taxable,
        'irg': irg,
        'net': net,
        'employer_cost': gross + gross * CNSS_EMPLOYER_RATE + gross * CNAS_EMPLOYER_RATE
    }
```

### 8. Intégration Pointage

```python
# kamra/hr/attendance/processor.py
def process_attendance_import(file_path: str, device_type: str):
    """
    Traite un fichier d'import pointage
    Formats supportés: CSV, Excel, JSON, API biométrique
    """
    pass

def detect_anomalies(attendance_records: list) -> list:
    """
    Détecte: absent non justifié, retard > 15min, 
    sortie avant horaire, double badgeage
    """
    pass
```

### 9. API REST principales

| Endpoint | Méthode | Description |
|---|---|---|
| `/api/method/ziri_hr.api.employee_api.get_employees` | GET | Liste employés avec filtres |
| `/api/method/ziri_hr.api.employee_api.create_employee` | POST | Créer employé |
| `/api/method/ziri_hr.api.leave_api.submit_leave` | POST | Soumettre demande congé |
| `/api/method/ziri_hr.api.leave_api.approve_leave` | POST | Valider congé |
| `/api/method/ziri_hr.api.attendance_api.import_attendance` | POST | Importer pointage |
| `/api/method/ziri_hr.api.attendance_api.get_anomalies` | GET | Anomalies du jour |
| `/api/method/ziri_hr.api.payroll_api.generate_payroll` | POST | Lancer paie mensuelle |
| `/api/method/ziri_hr.api.payroll_api.get_payslip` | GET | Bulletin employé |
| `/api/method/ziri_hr.api.payroll_api.export_cnss` | GET | Déclaration CNSS |

### 10. Rapports légaux à générer

| Rapport | Fréquence | Format | Destinataire |
|---|---|---|---|
| Registre Unique Personnel | Permanent | PDF/Excel | Inspection Travail |
| DPAE | À l'embauche | XML (CNSS) | CNSS |
| Déclaration Mensuelle CNSS | Mensuelle (J+15) | CSV/XML | CNSS |
| Déclaration Mensuelle CNAS | Mensuelle (J+15) | CSV/XML | CNAS |
| Livre de Paie | Mensuel | PDF | Comptable/Expert-Comptable |
| État Coûts par Service | Mensuel | Excel | Direction/Finance |
| Déclaration IRG | Annuelle | XML | Impôts |

---

*Ce document technique sert de spécification complète pour le développement du module RH ZIRI.PMS.*