# -*- coding: utf-8 -*-
# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

"""
API RH - Congés et Absences
"""

import frappe
from frappe import _
from frappe.utils import nowdate, now_datetime, getdate, date_diff
from typing import Any, Dict, List


@frappe.whitelist()
def get_leave_types() -> List[Dict]:
    """Types de congés disponibles"""
    return frappe.get_all("HR Leave Type",
        filters={"is_active": 1},
        fields=["name", "leave_type_name", "max_days", "is_carry_forward", "carry_forward_limit", "is_paid", "color"])


@frappe.whitelist()
def get_leave_balance(employee: str, leave_type: str = None) -> Dict[str, Any]:
    """Solde congés pour un employé"""
    from frappe.utils import flt
    
    filters = {"employee": employee, "status": "Approuvé", "docstatus": 1}
    if leave_type:
        filters["leave_type"] = leave_type
    
    taken = frappe.db.sql("""
        SELECT leave_type, COALESCE(SUM(total_days), 0) as total
        FROM `tabHR Leave Application`
        WHERE employee = %(employee)s AND status = 'Approuvé' AND docstatus = 1
        GROUP BY leave_type
    """, {"employee": employee}, as_dict=True)
    
    leave_types = frappe.get_all("HR Leave Type", fields=["name", "leave_type_name", "max_days", "is_carry_forward"])
    
    balances = {}
    for lt in leave_types:
        taken_days = next((t.total for t in taken if t.leave_type == lt.name), 0)
        balances[lt.leave_type_name] = {
            "quota": lt.max_days,
            "taken": flt(taken_days),
            "remaining": max(0, lt.max_days - flt(taken_days)),
            "carry_forward": lt.is_carry_forward
        }
    
    return {"employee": employee, "balances": balances}


@frappe.whitelist()
def submit_leave_application(data: Dict[str, Any]) -> Dict[str, Any]:
    """Soumettre une demande de congé"""
    required = ['employee', 'leave_type', 'from_date', 'to_date', 'reason']
    for field in required:
        if not data.get(field):
            frappe.throw(_("Champ requis: {0}").format(field))
    
    # Calculer jours
    from_date = getdate(data['from_date'])
    to_date = getdate(data['to_date'])
    if to_date < from_date:
        frappe.throw(_("Date fin antérieure à date début"))
    
    total_days = date_diff(to_date, from_date) + 1
    if data.get('half_day'):
        total_days -= 0.5
    
    # Vérifier solde
    leave_type = frappe.get_doc("HR Leave Type", data['leave_type'])
    balance = get_leave_balance(data['employee'], leave_type.name)
    remaining = balance['balances'].get(leave_type.leave_type_name, {}).get('remaining', 0)
    
    if total_days > remaining:
        frappe.throw(_("Solde insuffisant: {0} jours restants").format(remaining))
    
    # Créer demande
    leave = frappe.get_doc({
        "doctype": "HR Leave Application",
        "employee": data['employee'],
        "leave_type": data['leave_type'],
        "from_date": from_date,
        "to_date": to_date,
        "total_days": total_days,
        "half_day": data.get('half_day', 0),
        "half_day_date": data.get('half_day_date'),
        "reason": data['reason'],
        "status": "Soumis"
    })
    leave.insert(ignore_permissions=True)
    
    return {"name": leave.name, "status": leave.status, "message": "Demande soumise"}


@frappe.whitelist()
def approve_leave(leave_id: str, approver: str = None, comments: str = "") -> Dict[str, Any]:
    """Approuver une demande (par Manager ou RH)"""
    leave = frappe.get_doc("HR Leave Application", leave_id)
    
    if leave.status not in ['Soumis', 'Approuvé Manager']:
        frappe.throw(_("Demande ne peut pas être approuvée dans l'état: {0}").format(leave.status))
    
    # Déterminer étape
    leave_type = frappe.get_doc("HR Leave Type", leave.leave_type)
    
    if leave.status == 'Soumis' and leave_type.approval_workflow == 'Manager puis RH':
        leave.status = 'Approuvé Manager'
    else:
        leave.status = 'Approuvé'
    
    leave.approved_by = approver or frappe.session.user
    leave.approved_on = now_datetime()
    if comments:
        leave.reason += f"\n--- Validation: {comments}"
    leave.save(ignore_permissions=True)
    
    # Notifier employé
    frappe.publish_realtime(
        event='leave_approved',
        message={'leave_id': leave_id, 'status': leave.status},
        user=frappe.db.get_value("HR Employee", leave.employee, "user_id")
    )
    
    return {"name": leave.name, "status": leave.status, "message": "Demande approuvée"}


@frappe.whitelist()
def reject_leave(leave_id: str, rejection_reason: str, rejecter: str = None) -> Dict[str, Any]:
    """Rejeter une demande"""
    leave = frappe.get_doc("HR Leave Application", leave_id)
    
    if leave.status not in ['Soumis', 'Approuvé Manager']:
        frappe.throw(_("Demande ne peut pas être rejetée dans l'état: {0}").format(leave.status))
    
    leave.status = 'Rejeté'
    leave.rejection_reason = rejection_reason
    leave.approved_by = rejecter or frappe.session.user
    leave.approved_on = now_datetime()
    leave.save(ignore_permissions=True)
    
    return {"name": leave.name, "status": leave.status, "message": "Demande rejetée"}


@frappe.whitelist()
def cancel_leave(leave_id: str) -> Dict[str, Any]:
    """Annuler une demande (par l'employé)"""
    leave = frappe.get_doc("HR Leave Application", leave_id)
    
    if leave.status not in ['Brouillon', 'Soumis']:
        frappe.throw(_("Demande ne peut pas être annulée dans l'état: {0}").format(leave.status))
    
    leave.status = 'Annulé'
    leave.save(ignore_permissions=True)
    
    return {"name": leave.name, "status": leave.status, "message": "Demande annulée"}


@frappe.whitelist()
def get_leave_dashboard(
    department: str = None,
    status: str = None,
    page: int = 1,
    page_size: int = 50
) -> Dict[str, Any]:
    """Tableau de bord congés"""
    filters = {}
    if status:
        filters["status"] = status
    if department:
        filters["department"] = department
    
    fields = ["name", "employee", "employee_name", "leave_type", "from_date", "to_date", "total_days", "status", "approved_by", "approved_on"]
    
    leaves = frappe.get_all("HR Leave Application", filters=filters, fields=fields,
                           order_by="from_date desc", limit=page_size, start=(page-1)*page_size)
    
    total = frappe.db.count("HR Leave Application", filters)
    
    # Stats rapides
    stats = frappe.db.sql("""
        SELECT status, COUNT(*) as count
        FROM `tabHR Leave Application`
        GROUP BY status
    """, as_dict=True)
    
    return {
        "data": leaves,
        "total": total,
        "page": page,
        "stats": {s.status: s.count for s in stats}
    }


@frappe.whitelist()
def get_team_leaves(manager: str = None, month: int = None, year: int = None) -> List[Dict]:
    """Congés de l'équipe d'un manager"""
    if not manager:
        manager = frappe.session.user
    
    # Employés gérés
    employees = frappe.get_all("HR Employee", filters={"manager": manager}, fields=["name", "employee_name"])
    emp_names = [e.name for e in employees]
    
    if not emp_names:
        return []
    
    from frappe.utils import get_first_day, get_last_day
    if month and year:
        start = get_first_day(f"{year}-{month:02d}-01")
        end = get_last_day(start)
    else:
        start = get_first_day(nowdate())
        end = get_last_day(start)
    
    return frappe.get_all("HR Leave Application",
        filters={
            "employee": ["in", emp_names],
            "from_date": ["<=", end],
            "to_date": [">=", start],
            "status": ["in", ["Approuvé", "Approuvé Manager", "Approuvé RH"]]
        },
        fields=["employee", "employee_name", "leave_type", "from_date", "to_date", "total_days", "status"])


@frappe.whitelist()
def carry_forward_balances(year: int) -> Dict[str, Any]:
    """Report des soldes congés (exécution annuelle)"""
    # Créer entrées report pour employés actifs
    employees = frappe.get_all("HR Employee", filters={"status": "Actif"}, fields=["name"])
    
    carried = 0
    for emp in employees:
        balances = get_leave_balance(emp.name)
        for leave_type, bal in balances['balances'].items():
            if bal['carry_forward'] and bal['remaining'] > 0:
                carry = min(bal['remaining'], frappe.db.get_value("HR Leave Type", {"leave_type_name": leave_type}, "carry_forward_limit") or 15)
                if carry > 0:
                    # Créer entrée report
                    frappe.get_doc({
                        "doctype": "HR Leave Ledger Entry",
                        "employee": emp.name,
                        "leave_type": frappe.db.get_value("HR Leave Type", {"leave_type_name": leave_type}, "name"),
                        "transaction_type": "Report",
                        "days": carry,
                        "from_date": f"{year}-01-01",
                        "reference": f"Report {year-1}"
                    }).insert(ignore_permissions=True)
                    carried += 1
    
    return {"carried_entries": carried, "message": f"{carried} reports effectués"}