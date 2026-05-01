@echo off
echo ============================================
echo  LBAS - Reset Demo Data
echo ============================================
echo This will WIPE all users/books and re-seed demo data.
echo.
set /p confirm=Type YES to continue: 
if /i "%confirm%" NEQ "YES" (
    echo Cancelled.
    pause
    exit /b
)
python manage.py flush --no-input
python manage.py seed_demo
echo.
echo Done! Demo data restored.
echo Admin login: ID=admin / Password=admin
pause
