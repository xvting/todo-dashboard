@echo off
chcp 65001 >nul
echo ========================================
echo   TODO Dashboard Update Tool
echo ========================================
echo.

echo [1/3] Building dashboard...
python build.py
if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Committing to Git...
git add dist/
git commit -m "Update dashboard" >nul 2>&1
if errorlevel 1 (
    echo No changes to commit
) else (
    echo Commit successful
)

echo.
echo [3/3] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo Push failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Update complete! Refresh in 30s
echo ========================================
pause
