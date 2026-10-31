# -*- coding: utf-8 -*-
# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

"""
API RH - Pointage et Présences
"""

import frappe
from frappe import _
from frappe.utils import nowdate, getdate, get_first_day, get_last_day, add_days
from typing import Any, Dict, List


@frappe.whitelist()
def get_attendance_log(
    employee: str = None,
    department: str = None,
    from_date: str = None,
    to_date: str = None,
    status: str = None,
    anomaly_only: bool = False,
    page: int = 1,
    page_size: int = 100
) -> Dict[str, Any]:
    """Journal de pointage paginé"""
    filters = {}
    if employee:
        filters["employee"] = employee
    if department:
        filters["department"] = department
    if from_date:
        filters["attendance_date"] = [">=", from_date]
    if to_date:
        if "attendance_date" in filters:
            filters["attendance_date"] = ["between", [filters["attendance_date"][1], to_date]]
        else:
            filters["attendance_date"] = ["<=", to_date]
    if status:
        filters["status"] = status
    if anomaly_only:
        filters["is_anomaly"] = 1
    
    fields = [
        "name", "employee", "employee_name", "department", "attendance_date",
        "shift", "check_in", "check_out", "expected_check_in", "expected_check_out",
        "working_hours", "overtime_hours", "late_minutes", "early_departure_minutes",
        "status", "is_anomaly", "anomaly_type", "device_id", "device_type",
        "validated_by", "validated_on"
    ]
    
    records = frappe.get_all("HR Attendance", filters=filters, fields=fields,
                            order_by="attendance_date desc, employee_name",
                            limit=page_size, start=(page-1)*page_size)
    
    total = frappe.db.count("HR Attendance", filters)
    
    return {
        "data": records,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@frappe.whitelist()
def get_employee_attendance(employee: str, month: int, year: int) -> Dict[str, Any]:
    """Pointage mensuel d'un employé pour bulletin"""
    from frappe.utils import get_first_day, get_last_day
    
    start = get_first_day(f"{year}-{month:02d}-01")
    end = get_last_day(start)
    
    records = frappe.get_all("HR Attendance",
        filters={
            "employee": employee,
            "attendance_date": ["between", [start, end]],
            "status": ["in", ["Présent", "Retard", "Sortie anticipée"]]
        },
        fields=["attendance_date", "shift", "check_in", "check_out",
                "working_hours", "overtime_hours", "late_minutes", "early_departure_minutes", "status"],
        order_by="attendance_date")
    
    # Agrégation
    days_worked = len(records)
    total_hours = sum(r.working_hours or 0 for r in records)
    total_overtime = sum(r.overtime_hours or 0 for r in records)
    total_late = sum(r.late_minutes or 0 for r in records)
    shifts = list(set(r.shift for r in records))
    
    # Congés pris
    leaves = frappe.get_all("HR Leave Application",
        filters={
            "employee": employee,
            "from_date": ["<=", end],
            "to_date": [">=", start],
            "status": "Approuvé"
        },
        fields=["leave_type", "total_days"])
    
    leave_days = sum(l.total_days for l in leaves)
    leave_by_type = {}
    for l in leaves:
        leave_by_type[l.leave_type] = leave_by_type.get(l.leave_type, 0) + l.total_days
    
    return {
        "employee": employee,
        "period": f"{year}-{month:02d}",
        "days_worked": days_worked,
        "leave_days": leave_days,
        "leave_by_type": leave_by_type,
        "total_hours": total_hours,
        "total_overtime": total_overtime,
        "total_late_minutes": total_late,
        "shifts": shifts,
        "daily_records": records
    }


@frappe.whitelist()
def validate_attendance(attendance_id: str, validator: str = None) -> Dict[str, Any]:
    """Valider une anomalie de pointage"""
    doc = frappe.get_doc("HR Attendance", attendance_id)
    
    if not doc.is_anomaly:
        return {"message": "Aucune anomalie à valider"}
    
    doc.is_anomaly = 0
    doc.anomaly_type = ""
    doc.validated_by = validator or frappe.session.user
    doc.validated_on = frappe.utils.now_datetime()
    doc.save(ignore_permissions=True)
    
    return {"name": doc.name, "message": "Anomalie validée"}


@frappe.whitelist()
def get_anomalies_summary(date: str = None) -> Dict[str, Any]:
    """Résumé anomalies pour une date"""
    from kamra.kamra.hr.attendance.processor import AnomalyDetector
    return AnomalyDetector.scan_daily(date)


@frappe.whitelist()
def get_monthly_attendance_summary(month: int, year: int, department: str = None) -> Dict[str, Any]:
    """Résumé mensuel complet pour paie"""
    from frappe.utils import get_first_day, get_last_day
    from kamra.kamra.hr.attendance.processor import AnomalyDetector
    
    return AnomalyDetector.scan_monthly(month, year)


@frappe.whitelist()
def import_attendance(file_url: str, device_type: str = 'Biométrique') -> Dict[str, Any]:
    """Importer fichier pointage"""
    from kamra.kamra.hr.attendance.processor import import_attendance_file
    return import_attendance_file(file_url, device_type)


@frappe.whitelist()
def get_today_status(employee: str = None) -> Dict[str, Any]:
    """Statut pointage du jour"""
    today = nowdate()
    emp = employee or frappe.db.get_value("HR Employee", {"user_id": frappe.session.user}, "name")
    
    if not emp:
        return {"status": "Non employé"}
    
    record = frappe.get_all("HR Attendance",
        filters={"employee": emp, "attendance_date": today},
        fields=["name", "shift", "check_in", "check_out", "status", "is_anomaly", "anomaly_type"],
        limit=1)
    
    if record:
        return {"has_record": True, **record[0]}
    
    return {"has_record": False, "message": "Pas de pointage aujourd'hui"}


@frappe.whitelist()
def mark_attendance(employee: str, action: str, shift: str = 'Matin') -> Dict[str, Any]:
    """Badgeage manuel (entrée/sortie)"""
    from frappe.utils import now_datetime
    
    today = nowdate()
    now = now_datetime().time()
    
    existing = frappe.get_all("HR Attendance",
        filters={"employee": employee, "attendance_date": today, "shift": shift},
        limit=1)
    
    if existing:
        doc = frappe.get_doc("HR Attendance", existing[0].name)
        if action == 'check_in' and not doc.check_in:
            doc.check_in = now
            doc.status = 'Présent'
        elif action == 'check_out' and not doc.check_out:
            doc.check_out = now
        doc.save(ignore_permissions=True)
        return {"action": action, "time": str(now), "message": f"{action} enregistré"}
    else:
        if action == 'check_in':
            doc = frappe.get_doc({
                "doctype": "HR Attendance",
                "employee": employee,
                "attendance_date": today,
                "shift": shift,
                "check_in": now,
                "status": "Présent",
                "device_type": "Application Mobile"
            })
            doc.insert(ignore_permissions=True)
            return {"action": "check_in", "time": str(now), "message": "Arrivée enregistrée"}
        else:
            frappe.throw(_("Impossible de badger sortie sans arrivée"))