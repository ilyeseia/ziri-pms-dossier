#!/bin/bash
# ZIRI.PMS - Deployment Script for Kamra-PMS v2.6.20 with Algeria HR Module
# Usage: ./deploy_ziri_pms.sh [site-name] [branch]

set -e

SITE_NAME=${1:-ziri.local}
BRANCH=${2:-master}
APP_NAME="kamra"
REPO_URL="https://github.com/ilyeseia/ziri-pms-dossier.git"

echo "=== ZIRI.PMS Deployment Script ==="
echo "Site: $SITE_NAME"
echo "Branch: $BRANCH"
echo "App: $APP_NAME"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check if bench exists
if [ ! -d "frappe-bench" ] && [ ! -d "apps" ]; then
    error "Frappe bench not found. Please run this script from frappe-bench directory"
fi

log "Step 1: Updating Kamra-PMS from GitHub..."

# Clone or update repo
if [ -d "ziri-pms-dossier" ]; then
    cd ziri-pms-dossier
    git fetch origin
    git checkout $BRANCH
    git pull origin $BRANCH
    cd ..
else
    git clone -b $BRANCH $REPO_URL ziri-pms-dossier
fi

log "Step 2: Stopping Frappe services..."
bench stop

log "Step 3: Copying Kamra app to frappe-bench..."
mkdir -p ~/frappe-bench/apps
cp -rf ziri-pms-dossier/kamra ~/frappe-bench/apps/

log "Step 4: Installing/Updating Kamra app..."
cd ~/frappe-bench
bench --site $SITE_NAME install-app $APP_NAME

log "Step 5: Running database migrations..."
bench --site $SITE_NAME migrate

log "Step 6: Installing HR Module DocTypes and custom fields..."
# Create HR roles
bench --site $SITE_NAME execute frappe.get_doc({"doctype":"Role","role_name":"HR Manager"}).insert(ignore_permissions=True) || true
bench --site $SITE_NAME execute frappe.get_doc({"doctype":"Role","role_name":"HR Payroll Officer"}).insert(ignore_permissions=True) || true
bench --site $SITE_NAME execute frappe.get_doc({"doctype":"Role","role_name":"HR Staff Officer"}).insert(ignore_permissions=True) || true
bench --site $SITE_NAME execute frappe.get_doc({"doctype":"Role","role_name":"Employee Self Service"}).insert(ignore_permissions=True) || true
bench --site $SITE_NAME execute frappe.get_doc({"doctype":"Role","role_name":"Department Head"}).insert(ignore_permissions=True) || true

log "Step 7: Clearing caches..."
bench --site $SITE_NAME clear-cache
bench --site $SITE_NAME clear-website-cache

log "Step 8: Setting up Algeria payroll configuration..."
# Create default leave types
bench --site $SITE_NAME execute "
from frappe import _
import frappe
leave_types = [
    {'leave_type_name': 'Congés Annuels', 'max_days': 30, 'is_paid': 1},
    {'leave_type_name': 'Maladie', 'max_days': 90, 'is_paid': 1},
    {'leave_type_name': 'Maternité', 'max_days': 98, 'is_paid': 1},
    {'leave_type_name': 'Exceptionnel', 'max_days': 10, 'is_paid': 0},
]
for lt in leave_types:
    if not frappe.db.exists('HR Leave Type', lt['leave_type_name']):
        frappe.get_doc(lt).insert(ignore_permissions=True)
frappe.db.commit()
"

log "Step 9: Starting Frappe services..."
bench start

log "=== Deployment Complete ==="
echo ""
echo "ZIRI.PMS has been successfully deployed!"
echo "Site: $SITE_NAME"
echo "Access: http://$SITE_NAME:8000"
echo ""
echo "HR Module routes:"
echo "  - Dashboard RH: /ziri/hr"
echo "  - Gestion du Personnel: /ziri/hr/employees"
echo "  - Gestion des Congés: /ziri/hr/leaves"
echo "  - Journal de Pointage: /ziri/hr/attendance"
echo "  - Bulletins de Paie: /ziri/hr/payslips"
echo ""
log "Don't forget to:"
echo "  1. Update Site Config if needed"
echo "  2. Configure CNSS/CNAS rates in HR Salary Structure"
echo "  3. Import existing employee data if needed"
echo "  4. Test payroll calculation with sample employee"
