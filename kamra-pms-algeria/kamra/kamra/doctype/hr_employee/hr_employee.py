# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff, add_years, nowdate
from frappe import _


class HREmployee(Document):
	def validate(self):
		self.validate_dates()
		self.set_employee_name()
		self.validate_cnss_number()
		self.set_user_permissions()

	def validate_dates(self):
		if self.date_of_joining and self.date_of_leaving:
			if getdate(self.date_of_leaving) < getdate(self.date_of_joining):
				frappe.throw(_("La date de sortie ne peut pas être antérieure à la date d'entrée"))

	def set_employee_name(self):
		self.employee_name = f"{self.first_name} {self.last_name}"

	def validate_cnss_number(self):
		if self.cnss_number and not self.cnss_number.isdigit():
			frappe.throw(_("Le numéro CNSS doit contenir uniquement des chiffres"))

	def set_user_permissions(self):
		if self.user_id and not frappe.db.exists("User Permission", {"user": self.user_id, "allow": "HR Employee", "for_value": self.name}):
			frappe.get_doc({
				"doctype": "User Permission",
				"user": self.user_id,
				"allow": "HR Employee",
				"for_value": self.name
			}).insert(ignore_permissions=True)

	def on_submit(self):
		"""Créer l'utilisateur système si email fourni"""
		if self.email and not self.user_id:
			user = frappe.get_doc({
				"doctype": "User",
				"email": self.email,
				"first_name": self.first_name,
				"last_name": self.last_name,
				"phone": self.phone,
				"send_welcome_email": 1
			})
			user.insert(ignore_permissions=True)
			self.user_id = user.name
			self.save()

	def get_age(self):
		if self.date_of_birth:
			return date_diff(nowdate(), self.date_of_birth) // 365
		return 0

	def get_seniority(self):
		if self.date_of_joining:
			end_date = self.date_of_leaving or nowdate()
			return date_diff(end_date, self.date_of_joining) // 365
		return 0

	def is_active(self):
		return self.status == "Actif"

	@frappe.whitelist()
	def get_leave_balance(self, leave_type=None):
		"""Retourne le solde de congés pour un type donné"""
		from frappe.utils import flt
		
		filters = {"employee": self.name, "status": "Approved", "docstatus": 1}
		if leave_type:
			filters["leave_type"] = leave_type
		
		taken = frappe.db.sql("""
			SELECT COALESCE(SUM(total_days), 0) as total
			FROM `tabHR Leave Application`
			WHERE employee = %(employee)s AND status = 'Approved' AND docstatus = 1
		""", {"employee": self.name}, as_dict=True)[0].total or 0
		
		# Récupérer le quota selon le type de congé
		if leave_type:
			quota = frappe.db.get_value("HR Leave Type", leave_type, "max_days") or 0
		else:
			# Quota total (congés annuels par défaut)
			quota = frappe.db.get_value("HR Leave Type", {"leave_type_name": "Congés Annuels"}, "max_days") or 30
		
		return max(0, quota - flt(taken))

	@frappe.whitelist()
	def get_current_contract(self):
		"""Retourne le contrat actif"""
		return frappe.db.get_value("HR Contract", {
			"employee": self.name,
			"status": "Actif",
			"start_date": ["<=", nowdate()],
			"end_date": [">=", nowdate()]
		}, ["name", "contract_type", "salary_gross", "start_date", "end_date"], as_dict=True)


@frappe.whitelist()
def get_employees_by_department(department):
	"""Retourne les employés d'un département"""
	return frappe.get_all("HR Employee", 
		filters={"department": department, "status": "Actif"},
		fields=["name", "employee_id", "first_name", "last_name", "designation", "date_of_joining"])

@frappe.whitelist()
def get_birthdays_this_month():
	"""Retourne les anniversaires du mois"""
	from frappe.utils import nowdate, month_start, month_end
	return frappe.get_all("HR Employee",
		filters={
			"status": "Actif",
			"date_of_birth": ["between", [month_start(nowdate()), month_end(nowdate())]]
		},
		fields=["name", "employee_id", "first_name", "last_name", "date_of_birth", "department"])

@frappe.whitelist()
def get_contracts_expiring(days=30):
	"""Retourne les contrats arrivant à échéance"""
	from frappe.utils import add_days, nowdate
	return frappe.get_all("HR Contract",
		filters={
			"status": "Actif",
			"end_date": ["between", [nowdate(), add_days(nowdate(), days)]]
		},
		fields=["name", "employee", "employee_name", "contract_type", "end_date"])