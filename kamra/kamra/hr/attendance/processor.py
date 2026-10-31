# -*- coding: utf-8 -*-
# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

"""
Processeur de pointage - ZIRI.PMS
Import, validation et traitement des données de présence
"""

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime, time_diff_in_seconds, add_days, get_first_day, get_last_day
from typing import List, Dict, Any, Optional, Tuple
import csv
from io import StringIO, BytesIO
import json


SUPPORTED_FORMATS = ['csv', 'xlsx', 'json', 'txt']


class AttendanceProcessor:
    """Processeur principal pour l'import et traitement du pointage"""
    
    def __init__(self, company: str = None):
        self.company = company or frappe.defaults.get_global_default('company')
        self.errors = []
        self.warnings = []
        self.stats = {'created': 0, 'updated': 0, 'skipped': 0, 'anomalies': 0}
    
    def process_file(self, file_content: bytes, filename: str, device_type: str = 'Biométrique') -> Dict[str, Any]:
        """Traite un fichier de pointage selon son format"""
        ext = filename.split('.')[-1].lower()
        
        if ext == 'csv':
            records = self._parse_csv(file_content)
        elif ext in ['xlsx', 'xls']:
            records = self._parse_excel(file_content)
        elif ext == 'json':
            records = self._parse_json(file_content)
        else:
            raise ValueError(f"Format non supporté: {ext}")
        
        return self.process_records(records, device_type)
    
    def _parse_csv(self, content: bytes) -> List[Dict]:
        """Parse CSV avec détection encodage"""
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                text = content.decode(encoding)
                reader = csv.DictReader(StringIO(text))
                return list(reader)
            except UnicodeDecodeError:
                continue
        raise ValueError("Impossible de décoder le fichier CSV")
    
    def _parse_excel(self, content: bytes) -> List[Dict]:
        """Parse Excel (openpyxl requis)"""
        try:
            import openpyxl
        except ImportError:
            frappe.throw(_("Module openpyxl requis pour lire les fichiers Excel"))
        
        wb = openpyxl.load_workbook(BytesIO(content))
        ws = wb.active
        
        headers = [str(cell.value).strip().lower() if cell.value else '' for cell in ws[1]]
        records = []
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            record = {}
            for i, val in enumerate(row):
                if i < len(headers) and headers[i]:
                    record[headers[i]] = val
            if any(record.values()):
                records.append(record)
        
        return records
    
    def _parse_json(self, content: bytes) -> List[Dict]:
        """Parse JSON"""
        return json.loads(content.decode('utf-8'))
    
    def process_records(self, records: List[Dict], device_type: str = 'Biométrique') -> Dict[str, Any]:
        """Traite une liste d'enregistrements bruts"""
        self.stats = {'created': 0, 'updated': 0, 'skipped': 0, 'anomalies': 0}
        self.errors = []
        self.warnings = []
        
        for idx, row in enumerate(records, 1):
            try:
                self._process_single_record(row, device_type)
            except Exception as e:
                self.errors.append(f"Ligne {idx}: {str(e)}")
        
        return {
            'stats': self.stats,
            'errors': self.errors,
            'warnings': self.warnings
        }
    
    def _process_single_record(self, row: Dict, device_type: str) -> None:
        """Traite un enregistrement unique"""
        # Normaliser les clés (insensible à la casse)
        row = {k.lower().strip(): v for k, v in row.items() if v is not None}
        
        # Identifier l'employé
        emp_id = row.get('employee_id') or row.get('matricule') or row.get('badge_id') or row.get('id')
        if not emp_id:
            raise ValueError("Matricule employé manquant")
        
        employee = frappe.db.get_value("HR Employee", {"employee_id": str(emp_id)}, "name")
        if not employee:
            raise ValueError(f"Employé non trouvé: {emp_id}")
        
        # Date
        att_date = row.get('date') or row.get('attendance_date') or row.get('jour')
        if not att_date:
            raise ValueError("Date manquante")
        att_date = getdate(att_date)
        
        # Quart
        shift = row.get('shift') or row.get('quart') or row.get('equipe') or 'Matin'
        
        # Vérifier existence
        existing = frappe.db.get_value("HR Attendance", {
            "employee": employee,
            "attendance_date": att_date,
            "shift": shift
        }, "name")
        
        # Horaires
        check_in = self._parse_time(row.get('check_in') or row.get('arrivee') or row.get('entree'))
        check_out = self._parse_time(row.get('check_out') or row.get('depart') or row.get('sortie'))
        
        # Déterminer statut
        status = self._determine_status(check_in, check_out, row)
        
        if existing:
            # Mettre à jour
            doc = frappe.get_doc("HR Attendance", existing)
            if check_in:
                doc.check_in = check_in
            if check_out:
                doc.check_out = check_out
            doc.status = status
            doc.device_type = device_type
            doc.device_id = str(row.get('device_id') or row.get('terminal') or '')
            doc.save(ignore_permissions=True)
            self.stats['updated'] += 1
        else:
            # Créer nouveau
            doc = frappe.get_doc({
                "doctype": "HR Attendance",
                "employee": employee,
                "attendance_date": att_date,
                "shift": shift,
                "check_in": check_in,
                "check_out": check_out,
                "device_type": device_type,
                "device_id": str(row.get('device_id') or row.get('terminal') or ''),
                "status": status
            })
            doc.insert(ignore_permissions=True)
            self.stats['created'] += 1
        
        # Détecter anomalies
        if doc.is_anomaly:
            self.stats['anomalies'] += 1
            self.warnings.append(f"Anomalie {doc.name}: {doc.anomaly_type}")
    
    def _parse_time(self, time_val) -> Optional[str]:
        """Convertit various formats temps en HH:MM"""
        if not time_val:
            return None
        
        if isinstance(time_val, str):
            # Formats: HH:MM, HH:MM:SS, H:MM
            parts = time_val.split(':')
            if len(parts) >= 2:
                return f"{int(parts[0]):02d}:{int(parts[1]):02d}"
        
        # Si c'est un objet time/datetime
        if hasattr(time_val, 'strftime'):
            return time_val.strftime('%H:%M')
        
        return None
    
    def _determine_status(self, check_in, check_out, row) -> str:
        """Détermine le statut de présence"""
        explicit = row.get('status') or row.get('etat')
        if explicit:
            explicit = explicit.strip()
            if explicit in ['Présent', 'Absent', 'En congé', 'Retard', 'Sortie anticipée', 'Demi-journée', 'Jour férié', 'Repos']:
                return explicit
        
        if not check_in and not check_out:
            return 'Absent'
        elif check_in and not check_out:
            return 'Sortie anticipée'
        else:
            return 'Présent'


class AnomalyDetector:
    """Détecteur d'anomalies de pointage"""
    
    ANOMALY_RULES = {
        'absence_unjustified': {'threshold': 0, 'label': 'Absence non justifiée'},
        'late_excessive': {'threshold_minutes': 30, 'label': 'Retard excessif'},
        'early_departure': {'threshold_minutes': 30, 'label': 'Sortie anticipée'},
        'inconsistent_hours': {'label': 'Horaires incohérents'},
        'double_badge': {'label': 'Double badgeage'},
        'missing_checkout': {'label': 'Badgeage sortie manquant'},
        'missing_checkin': {'label': 'Badgeage entrée manquant'},
        'night_shift_error': {'label': 'Erreur quart nuit'},
    }
    
    @classmethod
    def detect(cls, attendance_doc) -> List[str]:
        """Détecte toutes les anomalies pour un document"""
        anomalies = []
        
        # 1. Absence non justifiée
        if attendance_doc.status == 'Absent' and not attendance_doc.notes:
            anomalies.append('Absence non justifiée')
        
        # 2. Retard excessif
        if attendance_doc.late_minutes and attendance_doc.late_minutes > 30:
            anomalies.append('Retard excessif')
        
        # 3. Sortie anticipée
        if attendance_doc.early_departure_minutes and attendance_doc.early_departure_minutes > 30:
            anomalies.append('Sortie anticipée')
        
        # 4. Horaires incohérents
        if attendance_doc.check_in and attendance_doc.check_out:
            from frappe.utils import time_diff_in_hours
            diff = time_diff_in_hours(attendance_doc.check_out, attendance_doc.check_in)
            if diff < 0 and attendance_doc.shift != 'Nuit':
                anomalies.append('Horaires incohérents')
            if diff > 16:  # Plus de 16h
                anomalies.append('Durée excessive')
        
        # 5. Double badgeage
        if not attendance_doc.is_new():
            existing = frappe.db.exists("HR Attendance", {
                "employee": attendance_doc.employee,
                "attendance_date": attendance_doc.attendance_date,
                "shift": attendance_doc.shift,
                "name": ["!=", attendance_doc.name]
            })
            if existing:
                anomalies.append('Double badgeage')
        
        # 6. Badgeage manquant
        if attendance_doc.status == 'Présent':
            if not attendance_doc.check_in:
                anomalies.append('Badgeage entrée manquant')
            if not attendance_doc.check_out:
                anomalies.append('Badgeage sortie manquant')
        
        # 7. Quart nuit mal géré
        if attendance_doc.shift == 'Nuit' and attendance_doc.check_in and attendance_doc.check_out:
            from frappe.utils import time_diff_in_hours
            diff = time_diff_in_hours(attendance_doc.check_out, attendance_doc.check_in)
            if diff < 4 or diff > 14:
                anomalies.append('Erreur quart nuit')
        
        return anomalies
    
    @classmethod
    def scan_daily(cls, date=None) -> Dict[str, Any]:
        """Scan quotidien de toutes les anomalies"""
        from frappe.utils import nowdate
        if not date:
            date = nowdate()
        
        records = frappe.get_all("HR Attendance",
            filters={"attendance_date": date},
            fields=["name", "employee", "employee_name", "department", "shift",
                    "check_in", "check_out", "late_minutes", "early_departure_minutes",
                    "status", "is_anomaly", "anomaly_type"])
        
        total_anomalies = 0
        by_type = {}
        by_dept = {}
        
        for r in records:
            detected = cls.detect(r)
            if detected:
                total_anomalies += 1
                for a in detected:
                    by_type[a] = by_type.get(a, 0) + 1
                dept = r.department or 'Non défini'
                by_dept[dept] = by_dept.get(dept, 0) + 1
        
        return {
            'date': date,
            'total_records': len(records),
            'total_anomalies': total_anomalies,
            'by_type': by_type,
            'by_department': by_dept,
            'anomaly_rate': round(total_anomalies / len(records) * 100, 1) if records else 0
        }
    
    @classmethod
    def scan_monthly(cls, month: int, year: int) -> Dict[str, Any]:
        """Scan mensuel complet"""
        from frappe.utils import get_first_day, get_last_day
        
        start = get_first_day(f"{year}-{month:02d}-01")
        end = get_last_day(start)
        
        records = frappe.get_all("HR Attendance",
            filters={"attendance_date": ["between", [start, end]]},
            fields=["name", "employee", "employee_name", "department", "attendance_date",
                    "shift", "status", "late_minutes", "early_departure_minutes",
                    "working_hours", "overtime_hours"])
        
        # Agrégats par employé
        by_employee = {}
        for r in records:
            emp_key = f"{r.employee} - {r.employee_name}"
            if emp_key not in by_employee:
                by_employee[emp_key] = {
                    'days_worked': 0,
                    'days_absent': 0,
                    'total_late': 0,
                    'total_overtime': 0,
                    'total_hours': 0,
                    'anomalies': 0
                }
            
            if r.status == 'Présent' or r.status == 'Retard':
                by_employee[emp_key]['days_worked'] += 1
                by_employee[emp_key]['total_hours'] += r.working_hours or 0
                by_employee[emp_key]['total_overtime'] += r.overtime_hours or 0
            elif r.status == 'Absent':
                by_employee[emp_key]['days_absent'] += 1
            
            by_employee[emp_key]['total_late'] += r.late_minutes or 0
            
            # Anomalies
            from frappe import get_doc
            doc = get_doc("HR Attendance", r.name)
            if cls.detect(doc):
                by_employee[emp_key]['anomalies'] += 1
        
        return {
            'period': f"{year}-{month:02d}",
            'start_date': start,
            'end_date': end,
            'total_records': len(records),
            'employees_summary': by_employee
        }


@frappe.whitelist()
def import_attendance_file(file_url: str, device_type: str = 'Biométrique') -> Dict[str, Any]:
    """API import fichier pointage"""
    file_doc = frappe.get_doc("File", {"file_url": file_url})
    content = file_doc.get_content()
    
    processor = AttendanceProcessor()
    return processor.process_file(content, file_doc.file_name, device_type)


@frappe.whitelist()
def get_daily_anomalies(date=None) -> Dict[str, Any]:
    """API anomalies du jour"""
    return AnomalyDetector.scan_daily(date)


@frappe.whitelist()
def get_monthly_anomalies(month: int, year: int) -> Dict[str, Any]:
    """API anomalies mensuelles"""
    return AnomalyDetector.scan_monthly(month, year)