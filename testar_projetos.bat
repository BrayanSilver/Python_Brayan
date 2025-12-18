@echo off
echo ========================================
echo Testador de Projetos - Python_Brayan
echo ========================================
echo.
echo Escolha um projeto para testar:
echo.
echo 1. Sistema de Backup Automatizado
echo 2. Monitor de Sistema
echo 3. Web Scraper Automatizado
echo 4. Automação de Envio de Emails
echo 5. Organizador Automático de Arquivos
echo 6. Automação de Tarefas Windows
echo 7. Monitor de Logs em Tempo Real
echo 8. Automação de Downloads
echo 9. Sistema de Notificações Desktop
echo 10. Gerador Automático de Relatórios
echo 0. Sair
echo.
set /p escolha="Digite o numero do projeto: "

if "%escolha%"=="1" (
    cd backup_automatico
    python backup_system.py
    cd ..
)
if "%escolha%"=="2" (
    cd monitor_sistema
    python monitor.py
    cd ..
)
if "%escolha%"=="3" (
    cd web_scraper
    python scraper.py
    cd ..
)
if "%escolha%"=="4" (
    cd automacao_email
    python email_sender.py
    cd ..
)
if "%escolha%"=="5" (
    cd organizador_arquivos
    python organizer.py
    cd ..
)
if "%escolha%"=="6" (
    cd automacao_windows
    python task_automation.py
    cd ..
)
if "%escolha%"=="7" (
    cd monitor_logs
    python log_monitor.py
    cd ..
)
if "%escolha%"=="8" (
    cd automacao_downloads
    python download_manager.py
    cd ..
)
if "%escolha%"=="9" (
    cd notificacoes_desktop
    python notifier.py
    cd ..
)
if "%escolha%"=="10" (
    cd gerador_relatorios
    python report_generator.py
    cd ..
)
if "%escolha%"=="0" (
    exit
)

pause
