# -*- coding: utf-8 -*-
# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

"""
API RH - Employés
"""

import frappe
from frappe import _
from frappe.utils import nowdate, add_days, get_first_day, get_last_day
from typing import Any, Dict, List


@frappe.whitelist()
def get_employees(
    department: str = None,
    status: str = 'Actif',
    designation: str = None,
    search: str = None,
    page: int = 1,
    page_size: int = 50
) -> Dict[str, Any]:
    """Liste paginée des employés"""
    filters = {"status": status}
    if department:
        filters["department"] = department
    if designation:
        filters["designation"] = designation
    
    fields = [
        "name", "employee_id", "first_name", "last_name", "employee_name",
        "department", "designation", "employment_type", "date_of_joining",
        "status", "email", "phone", "manager", "salary_gross"
    ]
    
    if search:
        employees = frappe.db.sql("""
            SELECT {fields}
            FROM `tabHR Employee`
            WHERE status = %(status)s
            AND (employee_name LIKE %(search)s OR employee_id LIKE %(search)s)
            ORDER BY employee_name
            LIMIT %(limit)s OFFSET %(offset)s
        """.format(fields=", ".join(fields)), {
            "status": status,
            "search": f"%{search}%",
            "limit": page_size,
            "offset": (page - 1) * page_size
        }, as_dict=True)
    else:
        employees = frappe.get_all("HR Employee", filters=filters, fields=fields,
                                  order_by="employee_name", limit=page_size, start=(page-1)*page_size)
    
    total = frappe.db.count("HR Employee", filters)
    
    return {
        "data": employees,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@frappe.whitelist()
def get_employee_details(employee: str) -> Dict[str, Any]:
    """Détails complets d'un employé"""
    emp = frappe.get_doc("HR Employee", employee)
    
    # Contrat actif
    contract = frappe.get_all("HR Contract",
        filters={"employee": employee, "status": "Actif"},
        fields=["name", "contract_type", "start_date", "end_date", "salary_gross", "salary_base"],
        limit=1)
    
    # Solde congés
    leave_balance = {}
    leave_types = frappe.get_all("HR Leave Type", fields=["name", "leave_type_name", "max_days"])
    for lt in leave_types:
        taken = frappe.db.sql("""
            SELECT COALESCE(SUM(total_days), 0)
            FROM `tabHR Leave Application`
            WHERE employee = %s AND leave_type = %s AND status = 'Approuvé' AND docstatus = 1
        """, (employee, lt.name))[0][0] or 0
        leave_balance[lt.leave_type_name] = {
            "quota": lt.max_days,
            "taken": taken,
            "remaining": max(0, lt.max_days - taken)
        }
    
    # Pointage mois courant
    from frappe.utils import get_first_day, get_last_day
    start = get_first_day(nowdate())
    end = get_last_day(start)
    
    attendance = frappe.get_all("HR Attendance",
        filters={"employee": employee, "attendance_date": ["between", [start, end]]},
        fields=["attendance_date", "shift", "check_in", "check_out", "working_hours", "overtime_hours", "status", "late_minutes"])
    
    return {
        "employee": emp.as_dict(),
        "contract": contract[0] if contract else None,
        "leave_balance": leave_balance,
        "attendance_month": attendance
    }


@frappe.whitelist()
def create_employee(data: Dict[str, Any]) -> Dict[str, Any]:
    """Créer un nouvel employé"""
    # Validation
    required = ['first_name', 'last_name', 'department', 'designation', 'date_of_joining', 'employment_type']
    for field in required:
        if not data.get(field):
            frappe.throw(_("Champ requis manquant: {0}").format(field))
    
    # Générer matricule
    last = frappe.db.sql("""SELECT MAX(CAST(SUBSTRING(employee_id, 5) AS UNSIGNED)) FROM `tabHR Employee` WHERE employee_id LIKE 'EMP-%'""")[0][0] or 0
    employee_id = f"EMP-{last + 1:04d}"
    
    emp = frappe.get_doc({
        "doctype": "HR Employee",
        "employee_id": employee_id,
        **data
    })
    emp.insert(ignore_permissions=True)
    
    # Créer utilisateur si email
    if data.get('email'):
        user = frappe.get_doc({
            "doctype": "User",
            "email": data['email'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "phone": data.get('phone'),
            "send_welcome_email": 1
        })
        user.insert(ignore_permissions=True)
        emp.user_id = user.name
        emp.save()
    
    return {"name": emp.name, "employee_id": emp.employee_id, "message": "Employé créé"}


@frappe.whitelist()
def update_employee(employee: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Modifier un employé"""
    emp = frappe.get_doc("HR Employee", employee)
    emp.update(data)
    emp.save(ignore_permissions=True)
    return {"message": "Employé mis à jour"}


@frappe.whitelist()
def get_dashboard_stats() -> Dict[str, Any]:
    """Statistiques pour tableau de bord RH"""
    from frappe.utils import nowdate, add_days, get_first_day, get_last_day
    
    total = frappe.db.count("HR Employee", {"status": "Actif"})
    
    # Nouveaux ce mois
    start = get_first_day(nowdate())
    new_this_month = frappe.db.count("HR Employee", {
        "date_of_joining": ["between", [start, nowdate()]],
        "status": "Actif"
    })
    
    # Départs ce mois
    departures = frappe.db.count("HR Employee", {
        "date_of_leaving": ["between", [start, nowdate()]],
        "status": ["in", ["Démissionné", "Licencié", "Retraité"]]
    })
    
    # Congés en attente
    pending_leaves = frappe.db.count("HR Leave Application", {"status": "Soumis"})
    
    # Taux présence aujourd'hui
    today = nowdate()
    total_today = frappe.db.count("HR Attendance", {"attendance_date": today})
    present_today = frappe.db.count("HR Attendance", {"attendance_date": today, "status": ["in", ["Présent", "Retard"]]})
    attendance_rate = round(present_today / total_today * 100, 1) if total_today > 0 else 100
    
    # Heures sup ce mois
    ot = frappe.db.sql("""
        SELECT COALESCE(SUM(overtime_hours), 0)
        FROM `tabHR Attendance`
        WHERE attendance_date BETWEEN %s AND %s
    """, (start, get_last_day(start)))[0][0]
    
    # Coût paie estimé
    payroll_cost = frappe.db.sql("""
        SELECT COALESCE(SUM(salary_gross), 0)
        FROM `tabHR Employee`
        WHERE status = 'Actif'
    """)[0][0]
    
    # Par département
    by_dept = frappe.db.sql("""
        SELECT department, COUNT(*) as count
        FROM `tabHR Employee`
        WHERE status = 'Actif'
        GROUP BY department
        ORDER BY count DESC
    """, as_dict=True)
    
    return {
        "total_employees": total,
        "new_hires": new_this_month,
        "departures": departures,
        "pending_leaves": pending_leaves,
        "attendance_rate": attendance_rate,
        "overtime_hours": float(ot or 0),
        "estimated_payroll_cost": float(payroll_cost or 0),
        "by_department": by_dept
    }


@frappe.whitelist()
def get_birthdays_this_month() -> List[Dict]:
    """Anniversaires du mois"""
    from frappe.utils import nowdate, get_first_day, get_last_day
    start = get_first_day(nowdate())
    end = get_last_day(start)
    
    return frappe.get_all("HR Employee",
        filters={"status": "Actif", "date_of_birth": ["between", [start, end]]},
        fields=["name", "employee_id", "first_name", "last_name", "date_of_birth", "department"])


@frappe.whitelist()
def get_contracts_expiring(days: int = 30) -> List[Dict]:
    """Contrats arrivant à échéance"""
    from frappe.utils import nowdate, add_days
    end = add_days(nowdate(), days)
    
    return frappe.get_all("HR Contract",
        filters={"status": "Actif", "end_date": ["between", [nowdate(), end]]},
        fields=["name", "employee", "employee_name", "contract_type", "end_date", "salary_gross"])