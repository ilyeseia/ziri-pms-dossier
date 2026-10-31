# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, time_diff_in_hours, flt, nowdate, now_datetime
from frappe import _


class HRAttendance(Document):
	def validate(self):
		self.set_employee_details()
		self.calculate_working_hours()
		self.detect_anomalies()
		self.set_expected_times()

	def set_employee_details(self):
		if self.employee:
			emp = frappe.get_doc("HR Employee", self.employee)
			self.employee_name = emp.employee_name
			self.department = emp.department

	def set_expected_times(self):
		"""Définit les horaires théoriques selon le quart"""
		shift_times = {
			"Matin": ("08:00", "17:00"),
			"Soir": ("14:00", "23:00"),
			"Nuit": ("22:00", "07:00"),
			"Continu": ("08:00", "16:00"),
		}
		if self.shift in shift_times and not self.expected_check_in:
			self.expected_check_in, self.expected_check_out = shift_times[self.shift]

	def calculate_working_hours(self):
		if self.check_in and self.check_out:
			# Calcul heures travaillées
			self.working_hours = flt(time_diff_in_hours(self.check_out, self.check_in))
			
			# Calcul retard
			if self.expected_check_in and self.check_in:
				from frappe.utils import time_diff_in_seconds
				diff = time_diff_in_seconds(self.check_in, self.expected_check_in)
				if diff > 0:
					self.late_minutes = int(diff / 60)
			
			# Calcul sortie anticipée
			if self.expected_check_out and self.check_out:
				from frappe.utils import time_diff_in_seconds
				diff = time_diff_in_seconds(self.expected_check_out, self.check_out)
				if diff > 0:
					self.early_departure_minutes = int(diff / 60)
			
			# Heures sup (au-delà de 8h ou 40h/semaine)
			normal_hours = 8.0
			if self.working_hours > normal_hours:
				self.overtime_hours = flt(self.working_hours - normal_hours)

	def detect_anomalies(self):
		anomalies = []
		
		# Absence non justifiée
		if self.status == "Absent" and not self.notes:
			anomalies.append("Absence non justifiée")
		
		# Retard excessif (> 30 min)
		if self.late_minutes and self.late_minutes > 30:
			anomalies.append("Retard excessif")
		
		# Sortie anticipée (> 30 min)
		if self.early_departure_minutes and self.early_departure_minutes > 30:
			anomalies.append("Sortie anticipée")
		
		# Horaires incohérents (ex: check_out < check_in sans nuit)
		if self.check_in and self.check_out:
			from frappe.utils import time_diff_in_hours
			if time_diff_in_hours(self.check_out, self.check_in) < 0 and self.shift != "Nuit":
				anomalies.append("Horaires incohérents")
		
		# Double badgeage (même employé, même date, même quart)
		if not self.is_new():
			existing = frappe.db.exists("HR Attendance", {
				"employee": self.employee,
				"attendance_date": self.attendance_date,
				"shift": self.shift,
				"name": ["!=", self.name]
			})
			if existing:
				anomalies.append("Double badgeage")
		
		self.is_anomaly = len(anomalies) > 0
		self.anomaly_type = ", ".join(anomalies) if anomalies else ""

	def on_submit(self):
		"""Créer entrée heures sup si applicable"""
		if self.overtime_hours and self.overtime_hours > 0:
			ot = frappe.get_doc({
				"doctype": "HR Overtime",
				"employee": self.employee,
				"date": self.attendance_date,
				"hours": self.overtime_hours,
				"rate_multiplier": 1.25,  # 125% par défaut
				"attendance_ref": self.name,
				"status": "En attente"
			})
			ot.insert(ignore_permissions=True)

	@frappe.whitelist()
	def validate_attendance(self, user=None):
		"""Valider l'anomalie"""
		self.is_anomaly = 0
		self.anomaly_type = ""
		self.validated_by = user or frappe.session.user
		self.validated_on = now_datetime()
		self.save(ignore_permissions=True)


@frappe.whitelist()
def import_attendance_from_file(file_url, device_type="Biométrique"):
	"""Importe pointage depuis fichier CSV/Excel"""
	import csv
	from io import StringIO
	
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	content = file_doc.get_content()
	
	if file_url.endswith(".csv"):
		reader = csv.DictReader(StringIO(content.decode("utf-8")))
		records = list(reader)
	else:
		# Excel - utiliser openpyxl
		import openpyxl
		from io import BytesIO
		wb = openpyxl.load_workbook(BytesIO(content))
		ws = wb.active
		headers = [cell.value for cell in ws[1]]
		records = []
		for row in ws.iter_rows(min_row=2, values_only=True):
			records.append(dict(zip(headers, row)))
	
	created = 0
	errors = []
	
	for row in records:
		try:
			emp_id = row.get("employee_id") or row.get("Matricule")
			emp = frappe.db.get_value("HR Employee", {"employee_id": emp_id}, "name")
			if not emp:
				errors.append(f"Employé non trouvé: {emp_id}")
				continue
			
			att_date = row.get("date") or row.get("Date")
			shift = row.get("shift") or row.get("Quart") or "Matin"
			
			# Vérifier si existe déjà
			exists = frappe.db.exists("HR Attendance", {
				"employee": emp,
				"attendance_date": att_date,
				"shift": shift
			})
			if exists:
				continue
			
			att = frappe.get_doc({
				"doctype": "HR Attendance",
				"employee": emp,
				"attendance_date": att_date,
				"shift": shift,
				"check_in": row.get("check_in") or row.get("Arrivée"),
				"check_out": row.get("check_out") or row.get("Départ"),
				"device_type": device_type,
				"device_id": row.get("device_id") or row.get("Terminal"),
				"status": "Présent"
			})
			att.insert(ignore_permissions=True)
			created += 1
		except Exception as e:
			errors.append(f"Ligne {row}: {str(e)}")
	
	return {"created": created, "errors": errors}

@frappe.whitelist()
def get_daily_anomalies(date=None):
	"""Retourne les anomalies du jour"""
	if not date:
		date = nowdate()
	
	return frappe.get_all("HR Attendance",
		filters={
			"attendance_date": date,
			"is_anomaly": 1
		},
		fields=["name", "employee", "employee_name", "department", "shift", 
				"check_in", "check_out", "late_minutes", "early_departure_minutes",
				"anomaly_type", "status"])

@frappe.whitelist()
def get_monthly_summary(employee, month, year):
	"""Résumé mensuel pour bulletin paie"""
	from frappe.utils import get_first_day, get_last_day
	
	start = get_first_day(f"{year}-{month:02d}-01")
	end = get_last_day(start)
	
	records = frappe.get_all("HR Attendance",
		filters={
			"employee": employee,
			"attendance_date": ["between", [start, end]],
			"status": ["in", ["Présent", "Retard", "Sortie anticipée"]]
		},
		fields=["working_hours", "overtime_hours", "late_minutes", "early_departure_minutes", "shift"])
	
	total_hours = sum(flt(r.working_hours) for r in records)
	total_overtime = sum(flt(r.overtime_hours) for r in records)
	total_late = sum(flt(r.late_minutes) for r in records)
	days_worked = len(records)
	
	return {
		"days_worked": days_worked,
		"total_hours": total_hours,
		"total_overtime": total_overtime,
		"total_late_minutes": total_late,
		"shifts": list(set(r.shift for r in records))
	}