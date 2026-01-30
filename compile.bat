@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo   ClawnSeeker Stealth Build Process (Nuitka)
echo ====================================================

:: Cleanup
if exist "dist" rd /s /q "dist"

echo [OK] Checking for src\main.py...
if not exist "src\main.py" (
    echo [ERROR] Cannot find src\main.py!
    pause
    exit /b
)

:: Build Command
:: --windows-icon-from-ico: Path to your icon file
:: --file-version: Professional versioning
python -m nuitka --standalone ^
       --onefile ^
       --windows-console-mode=disable ^
       --windows-uac-admin ^
       --plugin-enable=tk-inter ^
       --include-package-data=customtkinter ^
       --include-package=interception ^
       --follow-imports ^
       --windows-icon-from-ico=icon.ico ^
       --company-name="ClawnSeeker Lab" ^
       --product-name="ClawnSeeker Hardware" ^
       --file-version=2.0.0 ^
       --output-filename=ClawnSeeker.exe ^
       --output-dir=dist ^
       src/main.py

echo.
echo Build Complete! icon.ico has been embedded.
pause