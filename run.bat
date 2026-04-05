@echo off
chcp 65001 >nul
title CosyVoice3 WebUI

echo ============================================
echo   CosyVoice3 WebUI Launcher
echo ============================================
echo.

call "%USERPROFILE%\miniconda3\Scripts\activate.bat" cosyvoice3
cd /d "C:\CosyVoice3"

python launcher.py
pause
