@echo off
title Kriptografi Terminali
color 0b

echo ===================================================
echo      KRIPTOGRAFI TERMINALI BASLATILIYOR...
echo ===================================================
echo.

cd /d "%~dp0hill_vernam_projesi"

echo [*] Gerekli kutuphaneler kontrol ediliyor (Flask, Numpy)...
pip install flask numpy >nul 2>&1

echo [*] Sunucu baslatiliyor...
echo.
echo Lutfen tarayicinizda su adrese gidin: http://localhost:5000/
echo (Sunucuyu kapatmak icin bu pencereyi kapatabilirsiniz)
echo ===================================================
echo.

python app.py

pause
