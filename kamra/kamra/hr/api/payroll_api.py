# -*- coding: utf-8 -*-
# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

"""
API RH - Paie et Bulletins
"""

import frappe
from frappe import _
from frappe.utils import nowdate, getdate, get_first_day, get_last_day, flt
from decimal import Decimal
from typing import Any, Dict, List


def _period_start(period):
	"""Retourne le premier jour de la période (YYYY-MM -> YYYY-MM-01)."""
	period = str(period)
	if len(period) == 7:
		return f"{period}-01"
	return getdate(period)


@frappe.whitelist()
def generate_payslip(
    employee: str,
    period: str,
    gross_salary: float = None,
    overtime_hours: float = 0,
    overtime_rate_type: str = 'jour'
) -> Dict[str, Any]:
    """Générer un bulletin de paie"""
    from kamra.kamra.hr.payroll.algeria_payroll import generate_payslip as compute_payslip
    
    if gross_salary is None:
        emp = frappe.get_doc("HR Employee", employee)
        gross_salary = float(emp.salary_gross or emp.salary_base or 0)
        if not gross_salary:
            frappe.throw(_("Salaire non défini pour l'employé"))
    
    # Récupérer heures sup réelles
    if overtime_hours == 0:
        from kamra.kamra.hr.payroll.algeria_payroll import get_monthly_overtime
        overtime_hours = float(get_monthly_overtime(employee, period))
    
    return compute_payslip(employee, period, gross_salary, overtime_hours, overtime_rate_type)


@frappe.whitelist()
def batch_generate_payroll(
    employees: List[str],
    period: str
) -> List[Dict[str, Any]]:
    """Générer paie pour plusieurs employés"""
    from kamra.kamra.hr.payroll.algeria_payroll import batch_generate_payroll as compute_batch
    return compute_batch(employees, period)


@frappe.whitelist()
def create_salary_slips(period: str, department: str = None) -> Dict[str, Any]:
    """Créer bulletins pour tous employés actifs"""
    filters = {"status": "Actif"}
    if department:
        filters["department"] = department
    
    employees = frappe.get_all("HR Employee", filters=filters, fields=["name", "department", "salary_gross", "salary_base"])

    period_start = _period_start(period)
    created = 0
    errors = []

    for emp in employees:
        try:
            gross = float(emp.salary_gross or emp.salary_base or 0)
            if gross <= 0:
                errors.append(f"{emp.name}: Salaire non défini")
                continue

            # Vérifier si existe déjà
            existing = frappe.db.exists("HR Salary Slip", {
                "employee": emp.name,
                "payroll_period": period_start
            })
            if existing:
                errors.append(f"{emp.name}: Bulletin existe déjà")
                continue

            result = generate_payslip(emp.name, period, gross)

            earnings = [
                {"component": e.get("label") or e.get("code"), "amount": flt(e.get("amount")), "is_earning": 1}
                for e in result.get("earnings_detail", [])
                if flt(e.get("amount"))
            ]
            deductions = [
                {"component": d.get("label") or d.get("code"), "amount": flt(d.get("amount")), "is_earning": 0}
                for d in result.get("deductions_detail", [])
                if flt(d.get("amount"))
            ]

            # Créer document
            slip = frappe.get_doc({
                "doctype": "HR Salary Slip",
                "employee": emp.name,
                "employee_name": result.get('employee_name'),
                "department": emp.department,
                "payroll_period": period_start,
                "gross_salary": result['gross_salary'],
                "cnss_employee": result['cnss_employee'],
                "cnas_employee": result['cnas_employee'],
                "irg": result['irg'],
                "net_salary": result['net_salary'],
                "cnss_employer": result['cnss_employer'],
                "cnas_employer": result['cnas_employer'],
                "total_employer_cost": result['total_employer_cost'],
                "days_worked": result['working_days'],
                "overtime_hours": result['overtime_hours'],
                "overtime_amount": result['overtime_amount'],
                "total_deductions": flt(result['gross_salary']) - flt(result['net_salary']),
                "earnings": earnings,
                "deductions": deductions,
                "status": "Calculé"
            })
            slip.insert(ignore_permissions=True)
            created += 1
        except Exception as e:
            errors.append(f"{emp.name}: {str(e)}")
    
    return {"created": created, "errors": errors, "total": len(employees)}


@frappe.whitelist()
def get_payslip(payslip_id: str) -> Dict[str, Any]:
    """Récupérer bulletin complet"""
    slip = frappe.get_doc("HR Salary Slip", payslip_id)
    
    # Récupérer détails gains/retenues
    earnings = frappe.get_all("HR Salary Slip Component",
        filters={"parent": payslip_id, "parenttype": "HR Salary Slip", "is_earning": 1},
        fields=["component", "amount"])
    
    deductions = frappe.get_all("HR Salary Slip Component",
        filters={"parent": payslip_id, "parenttype": "HR Salary Slip", "is_earning": 0},
        fields=["component", "amount"])
    
    return {
        "header": slip.as_dict(),
        "earnings": earnings,
        "deductions": deductions
    }


@frappe.whitelist()
def get_payroll_summary(period: str, department: str = None) -> Dict[str, Any]:
    """Résumé paie pour période"""
    filters = {"payroll_period": _period_start(period)}
    if department:
        filters["department"] = department
    
    slips = frappe.get_all("HR Salary Slip", filters=filters, fields=[
        "employee", "employee_name", "gross_salary", "cnss_employee", "cnas_employee",
        "irg", "net_salary", "cnss_employer", "cnas_employer", "total_employer_cost", "status"
    ])
    
    totals = {
        "count": len(slips),
        "gross": sum(flt(s.gross_salary) for s in slips),
        "cnss_employee": sum(flt(s.cnss_employee) for s in slips),
        "cnas_employee": sum(flt(s.cnas_employee) for s in slips),
        "irg": sum(flt(s.irg) for s in slips),
        "net": sum(flt(s.net_salary) for s in slips),
        "cnss_employer": sum(flt(s.cnss_employer) for s in slips),
        "cnas_employer": sum(flt(s.cnas_employer) for s in slips),
        "employer_cost": sum(flt(s.total_employer_cost) for s in slips),
    }
    
    by_status = {}
    for s in slips:
        by_status[s.status] = by_status.get(s.status, 0) + 1
    
    return {
        "period": period,
        "totals": totals,
        "by_status": by_status,
        "slips": slips
    }


@frappe.whitelist()
def submit_payroll(period: str) -> Dict[str, Any]:
    """Valider et soumettre la paie (HR Manager)"""
    slips = frappe.get_all("HR Salary Slip", filters={
        "payroll_period": _period_start(period),
        "status": "Calculé"
    }, fields=["name"])
    
    submitted = 0
    for s in slips:
        doc = frappe.get_doc("HR Salary Slip", s.name)
        doc.status = "Vérifié"
        doc.save(ignore_permissions=True)
        submitted += 1
    
    return {"submitted": submitted, "message": f"{submitted} bulletins soumis pour vérification"}


@frappe.whitelist()
def approve_payroll(period: str) -> Dict[str, Any]:
    """Approuver paie pour paiement"""
    slips = frappe.get_all("HR Salary Slip", filters={
        "payroll_period": _period_start(period),
        "status": "Vérifié"
    }, fields=["name"])
    
    approved = 0
    for s in slips:
        doc = frappe.get_doc("HR Salary Slip", s.name)
        doc.status = "Payé"
        doc.payment_date = nowdate()
        doc.save(ignore_permissions=True)
        approved += 1
    
    return {"approved": approved, "message": f"{approved} bulletins approuvés pour paiement"}


@frappe.whitelist()
def export_cnss_declaration(period: str) -> Dict[str, Any]:
    """Export déclaration CNSS mensuelle"""
    from frappe.utils import get_first_day, get_last_day
    
    start = _period_start(period)
    end = get_last_day(start)

    # Employés avec salaire brut
    employees = frappe.get_all("HR Salary Slip", filters={
        "payroll_period": start,
        "status": ["in", ["Calculé", "Vérifié", "Payé"]]
    }, fields=["employee", "employee_name", "gross_salary", "cnss_employee", "cnss_employer", "days_worked"])

    employer_id = "A_COMPLETER"
    try:
        if frappe.db.exists("DocType", "Company") and frappe.get_meta("Company").has_field("cnss_number"):
            employer_id = frappe.db.get_single_value("Company", "cnss_number") or "A_COMPLETER"
    except Exception:
        pass

    # Format CNSS (exemple format standard)
    declaration = {
        "period": period,
        "declaration_date": nowdate(),
        "employer_id": employer_id,
        "employees": []
    }
    
    for e in employees:
        emp_doc = frappe.get_doc("HR Employee", e.employee)
        declaration["employees"].append({
            "cnss_number": emp_doc.cnss_number or "A_COMPLETER",
            "last_name": emp_doc.last_name,
            "first_name": emp_doc.first_name,
            "gross_salary": flt(e.gross_salary),
            "cnss_employee": flt(e.cnss_employee),
            "cnss_employer": flt(e.cnss_employer),
            "days_worked": flt(e.days_worked) or 26
        })

    return {
        "declaration": declaration,
        "total_employees": len(declaration["employees"]),
        "total_gross": sum(flt(e["gross_salary"]) for e in declaration["employees"]),
        "total_cnss_employee": sum(flt(e["cnss_employee"]) for e in declaration["employees"]),
        "total_cnss_employer": sum(flt(e["cnss_employer"]) for e in declaration["employees"])
    }


@frappe.whitelist()
def export_cnas_declaration(period: str) -> Dict[str, Any]:
    """Export déclaration CNAS mensuelle"""
    # Similaire à CNSS
    return {"message": "Format CNAS - À implémenter selon format officiel"}


@frappe.whitelist()
def get_salary_slips(period: str, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
    """Liste paginée des bulletins pour une période"""
    from frappe.utils import get_first_day, get_last_day
    period_start = _period_start(period)
    
    filters = {"payroll_period": period_start}
    
    total = frappe.db.count("HR Salary Slip", filters)
    
    slips = frappe.get_all("HR Salary Slip",
        filters=filters,
        fields=["name", "employee", "employee_name", "department", "payroll_period",
                "status", "gross_salary", "cnss_employee", "cnas_employee", "irg",
                "net_salary", "cnss_employer", "cnas_employer", "total_employer_cost",
                "days_worked", "overtime_hours", "overtime_amount", "total_deductions", "payment_date"],
        order_by="employee",
        limit=page_size,
        start=(page - 1) * page_size)
    
    return {"data": slips, "total": total, "page": page, "page_size": page_size}


@frappe.whitelist()
def mark_payslip_paid(payslip_id: str) -> Dict[str, Any]:
    """Marquer un bulletin comme Payé"""
    slip = frappe.get_doc("HR Salary Slip", payslip_id)
    
    if slip.status not in ["Vérifié", "Approuvé"]:
        frappe.throw(_("Seuls les bulletins 'Vérifié' ou 'Approuvé' peuvent être marqués payés"))
    
    slip.status = "Payé"
    slip.payment_date = nowdate()
    slip.save(ignore_permissions=True)
    
    return {"name": slip.name, "status": slip.status, "payment_date": str(slip.payment_date)}


@frappe.whitelist()
def get_employee_payslips(employee: str, year: int = None) -> List[Dict]:
    """Historique bulletins employé"""
    filters = {"employee": employee}
    if year:
        from frappe.utils import get_first_day, get_last_day
        start = get_first_day(f"{year}-01-01")
        end = get_last_day(f"{year}-12-01")
        filters["payroll_period"] = ["between", [start, end]]
    
    return frappe.get_all("HR Salary Slip", filters=filters,
        fields=["name", "payroll_period", "gross_salary", "net_salary", "status", "payment_date"],
        order_by="payroll_period desc")


@frappe.whitelist()
def calculate_annual_cost(employee: str) -> Dict[str, Any]:
    """Coût annuel complet employé"""
    from kamra.kamra.hr.payroll.algeria_payroll import compute_payslip
    
    emp = frappe.get_doc("HR Employee", employee)
    gross = float(emp.salary_gross or emp.salary_base or 0)
    
    # Simuler 12 mois
    monthly = compute_payslip(employee, "2024-01", Decimal(str(gross)))
    
    return {
        "employee": employee,
        "monthly_gross": float(monthly.gross_salary),
        "monthly_net": float(monthly.net_salary),
        "monthly_employer_cost": float(monthly.total_employer_cost),
        "annual_gross": float(monthly.gross_salary * 12),
        "annual_net": float(monthly.net_salary * 12),
        "annual_employer_cost": float(monthly.total_employer_cost * 12),
        "annual_cnss_employer": float(monthly.cnss_employer * 12),
        "annual_cnas_employer": float(monthly.cnas_employer * 12)
    }