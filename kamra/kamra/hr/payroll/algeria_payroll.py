# -*- coding: utf-8 -*-
# Copyright (c) 2026, ZIRI.PMS and contributors
# For license information, please see license.txt

"""
Moteur de paie Algérie - ZIRI.PMS
Calculs conformes à la législation algérienne 2024
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import frappe
from frappe import _

# ============================================================
# CONSTANTES LÉGALES ALGÉRIE 2024
# ============================================================

# Cotisations Sociales
CNSS_EMPLOYER_RATE = Decimal('0.26')      # 26% part patronale
CNSS_EMPLOYEE_RATE = Decimal('0.09')      # 9% part salariale
CNAS_EMPLOYER_RATE = Decimal('0.015')     # 1.5% part patronale
CNAS_EMPLOYEE_RATE = Decimal('0.005')     # 0.5% part salariale

# Plafond CNSS (plafond mensuel de la sécurité sociale)
CNSS_CEILING = Decimal('60000')  # DA/mois (à vérifier selon décret en vigueur)

# SMIG 2024
SMIG_MONTHLY = Decimal('20000')  # DA

# IRG - Tranches 2024 (Revenu Net Imposable Annuel)
IRG_BRACKETS = [
    (Decimal('0'), Decimal('120000'), Decimal('0.00')),
    (Decimal('120000'), Decimal('360000'), Decimal('0.20')),
    (Decimal('360000'), Decimal('1440000'), Decimal('0.30')),
    (Decimal('1440000'), Decimal('Infinity'), Decimal('0.35')),
]

# Abattement professionnel (10% du brut avec plafond)
PROFESSIONAL_ALLOWANCE_RATE = Decimal('0.10')
PROFESSIONAL_ALLOWANCE_MAX = Decimal('300000')  # DA/an

# Heures supplémentaires - Taux majoration
OVERTIME_RATES = {
    'jour': Decimal('1.25'),      # 125% jour
    'nuit': Decimal('1.50'),      # 150% nuit
    'dimanche': Decimal('1.50'),  # 150% dimanche/férié
    'ferie': Decimal('2.00'),     # 200% jour férié travaillé
}

# Congés payés - Indemnité
LEAVE_INDEMNITY_RATE = Decimal('1.0')  # 1/10ème de la rémunération brute


@dataclass
class PayrollComponent:
    """Composant de paie (gain ou retenue)"""
    code: str
    label: str
    amount: Decimal
    is_earning: bool
    is_taxable: bool = True
    is_cnss_base: bool = True
    is_cnas_base: bool = True


@dataclass
class PayrollResult:
    """Résultat calcul paie"""
    employee: str
    employee_name: str
    period: str
    gross_salary: Decimal
    total_earnings: Decimal
    total_deductions: Decimal
    net_salary: Decimal
    
    # Cotisations salariales
    cnss_employee: Decimal
    cnas_employee: Decimal
    irg: Decimal
    other_deductions: Decimal
    
    # Cotisations patronales
    cnss_employer: Decimal
    cnas_employer: Decimal
    total_employer_cost: Decimal
    
    # Détails
    earnings_detail: List[PayrollComponent]
    deductions_detail: List[PayrollComponent]
    working_days: int
    overtime_hours: Decimal
    overtime_amount: Decimal


def round_currency(value: Decimal) -> Decimal:
    """Arrondi monnaie algérienne (au DA près)"""
    return value.quantize(Decimal('1'), rounding=ROUND_HALF_UP)


def calculate_cnss_employee(gross: Decimal) -> Decimal:
    """CNSS part salariale (9% du brut, plafonné)"""
    base = min(gross, CNSS_CEILING)
    return round_currency(base * CNSS_EMPLOYEE_RATE)


def calculate_cnss_employer(gross: Decimal) -> Decimal:
    """CNSS part patronale (26% du brut, plafonné)"""
    base = min(gross, CNSS_CEILING)
    return round_currency(base * CNSS_EMPLOYER_RATE)


def calculate_cnas_employee(gross: Decimal) -> Decimal:
    """CNAS part salariale (0.5% du brut, sans plafond)"""
    return round_currency(gross * CNAS_EMPLOYEE_RATE)


def calculate_cnas_employer(gross: Decimal) -> Decimal:
    """CNAS part patronale (1.5% du brut, sans plafond)"""
    return round_currency(gross * CNAS_EMPLOYER_RATE)


def calculate_irg(taxable_annual: Decimal) -> Decimal:
    """
    Calcul IRG selon tranches 2024
    taxable_annual = (brut - cnss - cnas - abattement) * 12
    """
    tax = Decimal('0')
    remaining = taxable_annual
    
    for bracket_min, bracket_max, rate in IRG_BRACKETS:
        if remaining <= 0:
            break
        taxable_in_bracket = min(remaining, bracket_max - bracket_min)
        tax += taxable_in_bracket * rate
        remaining -= taxable_in_bracket
    
    return round_currency(tax / 12)  # Mensualisé


def calculate_professional_allowance(gross_annual: Decimal) -> Decimal:
    """Abattement professionnel 10% avec plafond"""
    allowance = gross_annual * PROFESSIONAL_ALLOWANCE_RATE
    return min(allowance, PROFESSIONAL_ALLOWANCE_MAX)


def calculate_net_taxable(gross_monthly: Decimal, cnss_emp: Decimal, cnas_emp: Decimal) -> Decimal:
    """Calcul du net imposable mensuel"""
    gross_annual = gross_monthly * 12
    allowance = calculate_professional_allowance(gross_annual)
    taxable_annual = gross_annual - (cnss_emp + cnas_emp) * 12 - allowance
    return max(Decimal('0'), taxable_annual / 12)


def calculate_overtime_pay(hourly_rate: Decimal, hours: Decimal, rate_type: str = 'jour') -> Decimal:
    """Calcul paiement heures supplémentaires"""
    multiplier = OVERTIME_RATES.get(rate_type, OVERTIME_RATES['jour'])
    return round_currency(hourly_rate * hours * multiplier)


def calculate_hourly_rate(monthly_gross: Decimal, weekly_hours: int = 40) -> Decimal:
    """Taux horaire de base (173.33h/mois pour 40h/sem)"""
    monthly_hours = Decimal(str(weekly_hours)) * Decimal('4.3333')
    return round_currency(monthly_gross / monthly_hours)


def calculate_leave_indemnity(gross_monthly: Decimal, days: int) -> Decimal:
    """Indemnité congés payés (1/10ème)"""
    daily_rate = gross_monthly / Decimal('26')  # 26 jours ouvrés
    return round_currency(daily_rate * Decimal(str(days)))


def compute_payslip(
    employee: str,
    period: str,
    gross_salary: Decimal,
    overtime_hours: Decimal = Decimal('0'),
    overtime_rate_type: str = 'jour',
    other_earnings: Optional[List[PayrollComponent]] = None,
    other_deductions: Optional[List[PayrollComponent]] = None,
    working_days: int = 26,
    cnas_category: str = 'Général',
    irg_category: str = 'Célibataire'
) -> PayrollResult:
    """
    Calcule un bulletin de paie complet
    
    Args:
        employee: ID employé
        period: Période paie (YYYY-MM)
        gross_salary: Salaire brut mensuel
        overtime_hours: Heures sup du mois
        overtime_rate_type: jour/nuit/dimanche/ferie
        other_earnings: Autres gains (primes, indemnités...)
        other_deductions: Autres retenues (avances, pénalités...)
        working_days: Jours travaillés
        cnas_category: Catégorie CNAS
        irg_category: Catégorie IRG pour quotient familial
    """
    
    # Récupérer infos employé
    emp = frappe.get_doc("HR Employee", employee)
    
    # 1. Calcul base
    base_gross = gross_salary
    
    # 2. Heures sup
    hourly_rate = calculate_hourly_rate(base_gross)
    overtime_amount = calculate_overtime_pay(hourly_rate, overtime_hours, overtime_rate_type)
    
    # 3. Total gains
    total_earnings = base_gross + overtime_amount
    if other_earnings:
        for e in other_earnings:
            total_earnings += e.amount
    
    # 4. Cotisations salariales
    cnss_employee = calculate_cnss_employee(total_earnings)
    cnas_employee = calculate_cnas_employee(total_earnings)
    
    # 5. Net imposable pour IRG
    net_taxable = calculate_net_taxable(total_earnings, cnss_employee, cnas_employee)
    
    # 6. IRG selon catégorie (quotient familial)
    # Simplifié: ajustement selon catégorie
    irg_adjustment = {
        'Célibataire': 1.0,
        'Marié 1 enfant': 0.85,
        'Marié 2 enfants': 0.75,
        'Marié 3+ enfants': 0.65,
    }.get(irg_category, 1.0)
    
    irg = round_currency(calculate_irg(net_taxable * 12) / 12 * Decimal(str(irg_adjustment)))
    
    # 7. Autres retenues
    other_ded_amount = Decimal('0')
    if other_deductions:
        for d in other_deductions:
            other_ded_amount += d.amount
    
    # 8. Total retenues salariales
    total_deductions = cnss_employee + cnas_employee + irg + other_ded_amount
    
    # 9. Net à payer
    net_salary = total_earnings - total_deductions
    
    # 10. Cotisations patronales
    cnss_employer = calculate_cnss_employer(total_earnings)
    cnas_employer = calculate_cnas_employer(total_earnings)
    total_employer_cost = total_earnings + cnss_employer + cnas_employer
    
    # Construire détails
    earnings_detail = [
        PayrollComponent('BASE', 'Salaire de base', base_gross, True),
        PayrollComponent('OT', f'Heures sup ({overtime_rate_type})', overtime_amount, True),
    ]
    if other_earnings:
        earnings_detail.extend(other_earnings)
    
    deductions_detail = [
        PayrollComponent('CNSS_EMP', 'CNSS Salarial', cnss_employee, False, is_taxable=False, is_cnss_base=False),
        PayrollComponent('CNAS_EMP', 'CNAS Salarial', cnas_employee, False, is_taxable=False, is_cnss_base=False),
        PayrollComponent('IRG', 'IRG', irg, False, is_taxable=False, is_cnss_base=False),
    ]
    if other_deductions:
        deductions_detail.extend(other_deductions)
    
    return PayrollResult(
        employee=employee,
        employee_name=getattr(emp, "employee_name", None) or f"{emp.first_name or ''} {emp.last_name or ''}".strip(),
        period=period,
        gross_salary=total_earnings,
        total_earnings=total_earnings,
        total_deductions=total_deductions,
        net_salary=net_salary,
        cnss_employee=cnss_employee,
        cnas_employee=cnas_employee,
        irg=irg,
        other_deductions=other_ded_amount,
        cnss_employer=cnss_employer,
        cnas_employer=cnas_employer,
        total_employer_cost=total_employer_cost,
        earnings_detail=earnings_detail,
        deductions_detail=deductions_detail,
        working_days=working_days,
        overtime_hours=overtime_hours,
        overtime_amount=overtime_amount
    )


@frappe.whitelist()
def generate_payslip(
    employee: str,
    period: str,
    gross_salary: float,
    overtime_hours: float = 0,
    overtime_rate_type: str = 'jour'
) -> Dict[str, Any]:
    """API pour générer un bulletin"""
    result = compute_payslip(
        employee=employee,
        period=period,
        gross_salary=Decimal(str(gross_salary)),
        overtime_hours=Decimal(str(overtime_hours)),
        overtime_rate_type=overtime_rate_type
    )
    
    return {
        'employee': result.employee,
        'employee_name': result.employee_name,
        'period': result.period,
        'gross_salary': float(result.gross_salary),
        'cnss_employee': float(result.cnss_employee),
        'cnas_employee': float(result.cnas_employee),
        'irg': float(result.irg),
        'net_salary': float(result.net_salary),
        'cnss_employer': float(result.cnss_employer),
        'cnas_employer': float(result.cnas_employer),
        'total_employer_cost': float(result.total_employer_cost),
        'working_days': result.working_days,
        'overtime_hours': float(result.overtime_hours),
        'overtime_amount': float(result.overtime_amount),
        'earnings_detail': [{'code': e.code, 'label': e.label, 'amount': float(e.amount), 'is_earning': e.is_earning} for e in result.earnings_detail],
        'deductions_detail': [{'code': d.code, 'label': d.label, 'amount': float(d.amount), 'is_earning': d.is_earning} for d in result.deductions_detail],
    }


@frappe.whitelist()
def batch_generate_payroll(
    employees: List[str],
    period: str,
    default_gross: float = None
) -> List[Dict[str, Any]]:
    """Génère la paie pour plusieurs employés"""
    results = []
    for emp in employees:
        if default_gross:
            gross = default_gross
        else:
            emp_doc = frappe.get_doc("HR Employee", emp)
            gross = float(emp_doc.salary_gross or emp_doc.salary_base or 0)
        
        # Récupérer heures sup du mois
        ot_hours = get_monthly_overtime(emp, period)
        
        result = generate_payslip(emp, period, gross, ot_hours)
        results.append(result)
    
    return results


def get_monthly_overtime(employee: str, period: str) -> Decimal:
    """Récupère les heures sup du mois depuis pointage"""
    from frappe.utils import get_first_day, get_last_day
    
    start = get_first_day(f"{period}-01")
    end = get_last_day(start)
    
    total = frappe.db.sql("""
        SELECT COALESCE(SUM(overtime_hours), 0)
        FROM `tabHR Attendance`
        WHERE employee = %s AND attendance_date BETWEEN %s AND %s
    """, (employee, start, end))[0][0]
    
    return Decimal(str(total or 0))