@echo off
setlocal enabledelagedexpansion

echo ====================================================
echo   ClawnSeeker Stealth Build Process (Nuitka)
echo ====================================================

:: Cleanup
if exist "dist" rd /s /q "dist"

:: Verify main file path (Note: your script says src/main.py, ensure that is correct)
if not exist "main.py" (
    echo [ERROR] Cannot find main.py! 
    echo If it's inside src, change the path below.
    pause
    exit /b
)

:: Build Command
python -m nuitka --standalone ^
       --onefile ^
       --windows-console-mode=disable ^
       --windows-uac-admin ^
       --plugin-enable=tk-inter ^
       --plugin-enable=torch ^
       --include-package-data=customtkinter ^
       --include-package=src ^
       --include-package=interception ^
       --follow-imports ^
       --windows-icon-from-ico=icon.ico ^
       --company-name="ClawnSeeker Lab" ^
       --product-name="ClawnSeeker Hardware" ^
       --file-version=2.0.0 ^
       --output-filename=ClawnSeeker.exe ^
       --output-dir=dist ^
       main.py

echo.
echo Build Complete!
pause