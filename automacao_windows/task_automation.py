"""
Automação de Tarefas Windows
Automatiza tarefas comuns do Windows
"""

import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import json
import winreg
import ctypes
from ctypes import wintypes


class WindowsAutomation:
    def __init__(self):
        """Inicializa o sistema de automação Windows"""
        self.is_admin = self.check_admin()
    
    def check_admin(self):
        """Verifica se está executando como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run_as_admin(self):
        """Solicita elevação de privilégios"""
        if self.is_admin:
            return True
        else:
            print("⚠️  Algumas funções requerem privilégios de administrador")
            return False
    
    def open_app(self, app_name_or_path):
        """Abre um aplicativo"""
        try:
            subprocess.Popen(app_name_or_path, shell=True)
            print(f"✅ Aplicativo aberto: {app_name_or_path}")
            return True
        except Exception as e:
            print(f"❌ Erro ao abrir aplicativo: {e}")
            return False
    
    def close_app(self, process_name):
        """Fecha um aplicativo pelo nome do processo"""
        try:
            subprocess.run(f"taskkill /F /IM {process_name}", shell=True, check=True)
            print(f"✅ Processo encerrado: {process_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Processo não encontrado: {process_name}")
            return False
    
    def list_running_processes(self):
        """Lista processos em execução"""
        try:
            result = subprocess.run(
                "tasklist /FO CSV",
                shell=True,
                capture_output=True,
                text=True,
                encoding='latin-1'
            )
            lines = result.stdout.strip().split('\n')[1:]  # Pula cabeçalho
            
            processes = []
            for line in lines:
                if line.strip():
                    parts = line.split('","')
                    if len(parts) >= 2:
                        name = parts[0].strip('"')
                        pid = parts[1].strip('"')
                        processes.append({'name': name, 'pid': pid})
            
            return processes
        except Exception as e:
            print(f"❌ Erro ao listar processos: {e}")
            return []
    
    def clean_temp_files(self):
        """Limpa arquivos temporários"""
        temp_paths = [
            os.path.join(os.environ.get('TEMP', ''), '*'),
            os.path.join(os.environ.get('TMP', ''), '*'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp', '*'),
        ]
        
        cleaned = 0
        total_size = 0
        
        for temp_path in temp_paths:
            temp_dir = Path(temp_path).parent
            if temp_dir.exists():
                for item in temp_dir.iterdir():
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            item.unlink()
                            cleaned += 1
                            total_size += size
                        elif item.is_dir():
                            shutil.rmtree(item)
                            cleaned += 1
                    except Exception as e:
                        pass  # Ignora arquivos em uso
        
        print(f"✅ Limpeza concluída: {cleaned} itens removidos ({total_size / (1024**2):.2f} MB)")
        return cleaned
    
    def clean_recycle_bin(self):
        """Limpa a lixeira"""
        try:
            subprocess.run(
                "powershell -Command Clear-RecycleBin -Force",
                shell=True,
                check=True
            )
            print("✅ Lixeira limpa")
            return True
        except Exception as e:
            print(f"❌ Erro ao limpar lixeira: {e}")
            return False
    
    def get_disk_space(self, drive='C:'):
        """Obtém espaço em disco"""
        try:
            result = subprocess.run(
                f'wmic logicaldisk where "DeviceID=\\"{drive}\\" get FreeSpace,Size',
                shell=True,
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                values = lines[1].split()
                if len(values) >= 2:
                    free = int(values[0])
                    total = int(values[1])
                    used = total - free
                    return {
                        'total_gb': round(total / (1024**3), 2),
                        'used_gb': round(used / (1024**3), 2),
                        'free_gb': round(free / (1024**3), 2),
                        'percent_used': round((used / total) * 100, 2)
                    }
        except Exception as e:
            print(f"❌ Erro ao obter espaço em disco: {e}")
        return None
    
    def create_shortcut(self, target_path, shortcut_path, description=""):
        """Cria um atalho"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target_path)
            shortcut.Description = description
            shortcut.save()
            print(f"✅ Atalho criado: {shortcut_path}")
            return True
        except ImportError:
            print("⚠️  pywin32 não instalado. Instale com: pip install pywin32")
            return False
        except Exception as e:
            print(f"❌ Erro ao criar atalho: {e}")
            return False
    
    def shutdown(self, delay_seconds=0, message=""):
        """Desliga o computador"""
        if not self.run_as_admin():
            print("❌ Requer privilégios de administrador")
            return False
        
        try:
            cmd = f"shutdown /s /t {delay_seconds}"
            if message:
                cmd += f' /c "{message}"'
            subprocess.run(cmd, shell=True)
            print(f"✅ Computador será desligado em {delay_seconds} segundos")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def restart(self, delay_seconds=0, message=""):
        """Reinicia o computador"""
        if not self.run_as_admin():
            print("❌ Requer privilégios de administrador")
            return False
        
        try:
            cmd = f"shutdown /r /t {delay_seconds}"
            if message:
                cmd += f' /c "{message}"'
            subprocess.run(cmd, shell=True)
            print(f"✅ Computador será reiniciado em {delay_seconds} segundos")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def cancel_shutdown(self):
        """Cancela desligamento/reinício agendado"""
        try:
            subprocess.run("shutdown /a", shell=True)
            print("✅ Desligamento/reinício cancelado")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def lock_screen(self):
        """Bloqueia a tela"""
        try:
            ctypes.windll.user32.LockWorkStation()
            print("✅ Tela bloqueada")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def get_system_info(self):
        """Obtém informações do sistema"""
        info = {
            'computer_name': os.environ.get('COMPUTERNAME', 'N/A'),
            'username': os.environ.get('USERNAME', 'N/A'),
            'os': os.environ.get('OS', 'N/A'),
            'processor': os.environ.get('PROCESSOR_IDENTIFIER', 'N/A'),
            'system_root': os.environ.get('SYSTEMROOT', 'N/A'),
        }
        
        # Espaço em disco
        disk_info = self.get_disk_space('C:')
        if disk_info:
            info['disk'] = disk_info
        
        return info
    
    def run_powershell_script(self, script_content):
        """Executa um script PowerShell"""
        try:
            result = subprocess.run(
                f'powershell -Command "{script_content}"',
                shell=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            print(f"❌ Erro ao executar PowerShell: {e}")
            return None
    
    def schedule_task(self, task_name, command, schedule_time):
        """Agenda uma tarefa (requer admin)"""
        if not self.run_as_admin():
            return False
        
        try:
            # Formato: HH:MM
            cmd = f'schtasks /create /tn "{task_name}" /tr "{command}" /sc once /st {schedule_time}'
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ Tarefa agendada: {task_name} às {schedule_time}")
            return True
        except Exception as e:
            print(f"❌ Erro ao agendar tarefa: {e}")
            return False


def main():
    """Interface interativa"""
    automation = WindowsAutomation()
    
    print("🪟 Automação de Tarefas Windows\n")
    
    while True:
        print("\n" + "="*50)
        print("1. Abrir aplicativo")
        print("2. Fechar aplicativo")
        print("3. Listar processos")
        print("4. Limpar arquivos temporários")
        print("5. Limpar lixeira")
        print("6. Ver espaço em disco")
        print("7. Informações do sistema")
        print("8. Bloquear tela")
        print("9. Desligar computador")
        print("10. Reiniciar computador")
        print("11. Cancelar desligamento")
        print("0. Sair")
        print("="*50)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            app = input("Nome ou caminho do aplicativo: ").strip()
            automation.open_app(app)
        
        elif choice == "2":
            process = input("Nome do processo (ex: notepad.exe): ").strip()
            automation.close_app(process)
        
        elif choice == "3":
            processes = automation.list_running_processes()
            print(f"\n📋 {len(processes)} processos em execução:")
            for proc in processes[:20]:  # Mostra os primeiros 20
                print(f"  - {proc['name']} (PID: {proc['pid']})")
        
        elif choice == "4":
            confirm = input("⚠️  Limpar arquivos temporários? (s/n): ").strip().lower()
            if confirm == 's':
                automation.clean_temp_files()
        
        elif choice == "5":
            confirm = input("⚠️  Limpar lixeira? (s/n): ").strip().lower()
            if confirm == 's':
                automation.clean_recycle_bin()
        
        elif choice == "6":
            drive = input("Drive (ex: C:): ").strip() or "C:"
            disk_info = automation.get_disk_space(drive)
            if disk_info:
                print(f"\n💿 Disco {drive}:")
                print(f"  Total: {disk_info['total_gb']} GB")
                print(f"  Usado: {disk_info['used_gb']} GB ({disk_info['percent_used']}%)")
                print(f"  Livre: {disk_info['free_gb']} GB")
        
        elif choice == "7":
            info = automation.get_system_info()
            print("\n🖥️  Informações do Sistema:")
            for key, value in info.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for k, v in value.items():
                        print(f"    {k}: {v}")
                else:
                    print(f"  {key}: {value}")
        
        elif choice == "8":
            automation.lock_screen()
        
        elif choice == "9":
            delay = input("Delay em segundos (0 para imediato): ").strip()
            delay = int(delay) if delay.isdigit() else 0
            msg = input("Mensagem (opcional): ").strip()
            automation.shutdown(delay, msg)
        
        elif choice == "10":
            delay = input("Delay em segundos (0 para imediato): ").strip()
            delay = int(delay) if delay.isdigit() else 0
            msg = input("Mensagem (opcional): ").strip()
            automation.restart(delay, msg)
        
        elif choice == "11":
            automation.cancel_shutdown()
        
        elif choice == "0":
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    main()
