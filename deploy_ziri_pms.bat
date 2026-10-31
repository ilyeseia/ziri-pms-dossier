@echo off
REM ZIRI.PMS - Deployment Script for Windows
REM Usage: deploy_ziri_pms.bat [site-name] [branch]

set SITE_NAME=%1
if "%SITE_NAME%"=="" set SITE_NAME=ziri.local

set BRANCH=%2
if "%BRANCH%"=="" set BRANCH=master

echo === ZIRI.PMS Deployment Script ===
echo Site: %SITE_NAME%
echo Branch: %BRANCH%
echo.

echo Step 1: Updating Kamra-PMS from GitHub...
if exist ziri-pms-dossier (
    cd ziri-pms-dossier
    git fetch origin
    git checkout %BRANCH%
    git pull origin %BRANCH%
    cd ..
) else (
    git clone -b %BRANCH% https://github.com/ilyeseia/ziri-pms-dossier.git ziri-pms-dossier
)

echo Step 2: Copying Kamra app to frappe-bench...
if not exist "C:\frappe-bench\apps" mkdir "C:\frappe-bench\apps"
xcopy /E /I /Y ziri-pms-dossier\kamra "C:\frappe-bench\apps\kamra"

echo Step 3: Installing/Updating Kamra app...
cd C:\frappe-bench
bench --site %SITE_NAME% install-app kamra

echo Step 4: Running database migrations...
bench --site %SITE_NAME% migrate

echo Step 5: Clearing caches...
bench --site %SITE_NAME% clear-cache
bench --site %SITE_NAME% clear-website-cache

echo Step 6: Starting Frappe services...
start bench start

echo ===
echo ZIRI.PMS has been successfully deployed!
echo Site: %SITE_NAME%
echo Access: http://%SITE_NAME%:8000
echo.
echo HR Module routes:
echo   - Dashboard RH: /ziri/hr
echo   - Gestion du Personnel: /ziri/hr/employees
echo   - Gestion des Congés: /ziri/hr/leaves
echo   - Journal de Pointage: /ziri/hr/attendance
echo   - Bulletins de Paie: /ziri/hr/payslips
echo.
pause
