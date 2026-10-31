# ZIRI.PMS - Deployment Guide

> **ZIRI.PMS** - Hotel Management System for Algeria  
> Based on **Kamra-PMS v2.6.20** with Algeria-specific HR & Payroll module

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ZIRI.PMS Stack                          │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React SPA)     │  /ziri/* routes                  │
│  ├─ Dashboard             │  /ziri/hr (HR Module)            │
│  ├─ POS                   │  /ziri/pos                       │
│  ├─ Tape Chart            │  /ziri/tape-chart                │
│  └─ Housekeeping          │  /ziri/hk                        │
├─────────────────────────────────────────────────────────────┤
│  Backend (Frappe Framework v15+)                            │
│  ├─ Kamra Core            │  Hotel Operations               │
│  ├─ Smart Access          │  Door Locks / Credentials       │
│  ├─ HR Management         │  Algeria Payroll (CNSS/CNAS/IRG)│
│  └─ Payments              │  Payment Gateways               │
├─────────────────────────────────────────────────────────────┤
│  Database (PostgreSQL 15+)  │  Redis (Cache/Queue)          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Deployment

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/ilyeseia/ziri-pms-dossier.git
cd ziri-pms-dossier

# 2. Copy Kamra app to apps directory
mkdir -p apps
cp -r kamra apps/

# 3. Start stack
docker-compose up -d

# 4. Run migrations
docker-compose exec frappe bench --site ziri.local install-app kamra
docker-compose exec frappe bench --site ziri.local migrate

# 5. Access
# http://localhost:8000
```

### Option 2: Manual Frappe Bench

```bash
# 1. Setup Frappe bench (if not exists)
bench init --frappe-branch version-15 frappe-bench
cd frappe-bench

# 2. Get ZIRI.PMS
cd apps
git clone -b master https://github.com/ilyeseia/ziri-pms-dossier.git
cd ziri-pms-dossier
cp -r kamra ../
cd ../..

# 3. Install app
bench --site site-name install-app kamra
bench --site site-name migrate

# 4. Start
bench start
```

### Option 3: Windows Batch Script

```cmd
# Run as Administrator
deploy_ziri_pms.bat ziri.local master
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` in frappe-bench:

```env
# Database
DB_HOST=localhost
DB_USER=frappe
DB_PASSWORD=your_password
DB_NAME=frappe

# Redis
REDIS_CACHE=redis://localhost:6379
REDIS_QUEUE=redis://localhost:6380

# Site
FRAPPE_SITE_NAME=ziri.local

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your@email.com
EMAIL_PASSWORD=your_password

# Tailscale (for remote access)
TAILSCALE_AUTHKEY=your_authkey
```

### HR Module Configuration

After installation, configure Algeria payroll:

```bash
bench --site ziri.local execute "
import frappe

# Create default HR Leave Types
leave_types = [
    {'leave_type_name': 'Congés Annuels', 'max_days': 30, 'is_paid': 1},
    {'leave_type_name': 'Maladie', 'max_days': 90, 'is_paid': 1},
    {'leave_type_name': 'Maternité', 'max_days': 98, 'is_paid': 1},
    {'leave_type_name': 'Exceptionnel', 'max_days': 10, 'is_paid': 0},
]
for lt in leave_types:
    if not frappe.db.exists('HR Leave Type', lt['leave_type_name']):
        frappe.get_doc(lt).insert(ignore_permissions=True)

# Create HR Roles
roles = ['HR Manager', 'HR Payroll Officer', 'HR Staff Officer', 
         'Department Head', 'Employee Self Service']
for r in roles:
    if not frappe.db.exists('Role', r):
        frappe.get_doc({'doctype': 'Role', 'role_name': r, 'desk_access': 0}).insert(ignore_permissions=True)

frappe.db.commit()
"
```

---

## 📋 Post-Installation Checklist

- [ ] **Company Setup**: Create hotel company with Algeria localization (DZD, RC, NIS, AI, NIF)
- [ ] **Property Setup**: Add hotel property with room types, rates, seasons
- [ ] **HR Configuration**: 
  - [ ] CNSS/CNAS rates in HR Salary Structure (26%/1.5% employer, 9%/0.5% employee)
  - [ ] IRG 2024 brackets
  - [ ] Leave types and policies
  - [ ] Work shifts (Matin, Soir, Nuit, Continu)
- [ ] **POS Setup**: Create outlets (Restaurant, Bar, Minibar, Room Service, Spa)
- [ ] **Smart Access**: Configure door locks and staff credentials
- [ ] **Users**: Create users for each department with appropriate roles
- [ ] **Backup**: Configure automated backups

---

## 🔄 Update Process

```bash
# 1. Pull latest changes
cd ziri-pms-dossier
git pull origin master

# 2. Update app
cd ~/frappe-bench
cp -r ziri-pms-dossier/kamra apps/kamra

# 3. Run migrations
bench --site ziri.local migrate

# 4. Clear cache
bench --site ziri.local clear-cache

# 5. Restart
bench restart
```

---

## 🛠️ Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev  # Starts on http://localhost:3000
```

### Backend Development

```bash
# In frappe-bench
bench --site ziri.local console  # Python REPL
bench --site ziri.local shell   # Frappe shell

# Watch for changes
bench watch
```

---

## 🔐 Security

- Change default passwords
- Configure firewall (only 80/443/8000/9000 open)
- Use HTTPS in production (Let's Encrypt via certbot)
- Regular security updates: `bench update`

---

## 📚 Documentation

| Document | Path |
|----------|------|
| Technical Audit | `docs/ziri_audit/01_AUDIT_TECHNIQUE_COMPLET.md` |
| Service Inventory | `docs/hotel/02_INVENTAIRE_DES_SERVICES_HOTELIERS.md` |
| POS Inventory | `docs/hotel/03_INVENTAIRE_DETAILLE_DES_POINTS_DE_VENTE.md` |
| Interface Map | `docs/hotel/04_CARTOGRAPHIE_DES_INTERFACES.md` |
| User Organization | `docs/hotel/05_ORGANISATION_DES_UTILISATEURS.md` |
| Commercial Dossier | `docs/commercial/` |
| HR Module Spec | `docs/technical/HR_MODULE_SPEC.md` |
| Trilingual Glossary | `docs/hotel/01_GLOSSAIRE_TRILINGUE.md` |

---

## 🆘 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | `bench --site ziri.local install-app kamra` |
| Migration failed | Check `bench --site ziri.local migrate --skip-failing` |
| Cache issues | `bench --site ziri.local clear-cache && bench --site ziri.local clear-website-cache` |
| Port conflict | Change ports in `docker-compose.yml` or `sites/conf.json` |
| Permissions | `chown -R frappe:frappe ~/frappe-bench` |

### Logs

```bash
# Frappe logs
bench --site ziri.local logs

# Docker logs
docker-compose logs -f frappe

# Nginx logs
docker-compose logs -f nginx
```

---

## 📞 Support

- **Repository**: https://github.com/ilyeseia/ziri-pms-dossier
- **Issues**: GitHub Issues
- **Documentation**: `/docs` folder

---

## 📄 License

Proprietary - ZIRI.PMS for Algeria market
Based on Kamra-PMS (MIT License)