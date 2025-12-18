@echo off
echo ========================================
echo Instalador de Dependencias - Python_Brayan
echo ========================================
echo.
echo Instalando todas as dependencias necessarias...
echo.

pip install psutil requests beautifulsoup4 pandas openpyxl win10toast

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Dependencias instaladas:
echo - psutil (Monitor de Sistema)
echo - requests (Web Scraper, Downloads)
echo - beautifulsoup4 (Web Scraper)
echo - pandas (Gerador de Relatorios)
echo - openpyxl (Gerador de Relatorios - Excel)
echo - win10toast (Notificacoes Desktop)
echo.
pause
