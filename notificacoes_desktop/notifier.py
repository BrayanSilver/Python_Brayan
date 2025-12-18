"""
Sistema de Notificações Desktop
Sistema completo para enviar notificações no Windows
"""

import os
import json
from pathlib import Path
from datetime import datetime
import time
try:
    from win10toast import ToastNotifier
    WIN10TOAST_AVAILABLE = True
except ImportError:
    WIN10TOAST_AVAILABLE = False
    print("⚠️  win10toast não instalado. Instale com: pip install win10toast")


class DesktopNotifier:
    def __init__(self):
        """Inicializa o sistema de notificações"""
        self.notifications_log = []
        self.log_file = Path("notifications_log.json")
        
        if WIN10TOAST_AVAILABLE:
            self.toaster = ToastNotifier()
        else:
            self.toaster = None
            print("⚠️  Usando notificações básicas (instale win10toast para melhor experiência)")
    
    def notify(self, title, message, duration=5, icon_path=None, threaded=True):
        """
        Envia uma notificação desktop
        
        Args:
            title: Título da notificação
            message: Mensagem
            duration: Duração em segundos
            icon_path: Caminho do ícone (opcional)
            threaded: Executa em thread separada
        """
        timestamp = datetime.now().isoformat()
        
        try:
            if self.toaster:
                # Usa win10toast (Windows 10+)
                self.toaster.show_toast(
                    title,
                    message,
                    duration=duration,
                    icon_path=icon_path,
                    threaded=threaded
                )
            else:
                # Fallback: usa notificação básica do Windows
                self._notify_basic(title, message)
            
            # Log
            notification_info = {
                'timestamp': timestamp,
                'title': title,
                'message': message,
                'status': 'sent'
            }
            self.notifications_log.append(notification_info)
            self.save_log()
            
            print(f"✅ Notificação enviada: {title}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar notificação: {e}")
            notification_info = {
                'timestamp': timestamp,
                'title': title,
                'message': message,
                'status': 'error',
                'error': str(e)
            }
            self.notifications_log.append(notification_info)
            return False
    
    def _notify_basic(self, title, message):
        """Notificação básica usando PowerShell"""
        try:
            import subprocess
            ps_script = f'''
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
            
            $toastXml = [Windows.Data.Xml.Dom.XmlDocument]::new()
            $toastXml.LoadXml(@"
            <toast>
                <visual>
                    <binding template="ToastText02">
                        <text id="1">{title}</text>
                        <text id="2">{message}</text>
                    </binding>
                </visual>
            </toast>
"@)
            
            $toast = [Windows.UI.Notifications.ToastNotification]::new($toastXml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Python").Show($toast)
            '''
            
            subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True
            )
        except:
            # Último recurso: apenas print
            print(f"\n🔔 {title}: {message}\n")
    
    def notify_scheduled(self, title, message, delay_seconds, icon_path=None):
        """Agenda uma notificação"""
        print(f"⏰ Notificação agendada para {delay_seconds} segundos")
        
        def send_after_delay():
            time.sleep(delay_seconds)
            self.notify(title, message, icon_path=icon_path)
        
        import threading
        thread = threading.Thread(target=send_after_delay)
        thread.daemon = True
        thread.start()
        
        return thread
    
    def notify_recurring(self, title, message, interval_seconds, count=None, icon_path=None):
        """
        Envia notificações recorrentes
        
        Args:
            title: Título
            message: Mensagem
            interval_seconds: Intervalo entre notificações
            count: Número de notificações (None = infinito)
            icon_path: Caminho do ícone
        """
        print(f"🔄 Notificações recorrentes a cada {interval_seconds}s")
        
        def send_recurring():
            sent = 0
            while count is None or sent < count:
                self.notify(title, message, icon_path=icon_path)
                sent += 1
                if count is None or sent < count:
                    time.sleep(interval_seconds)
        
        import threading
        thread = threading.Thread(target=send_recurring)
        thread.daemon = True
        thread.start()
        
        return thread
    
    def notify_on_condition(self, title, message, condition_func, check_interval=5, icon_path=None):
        """
        Envia notificação quando uma condição for verdadeira
        
        Args:
            title: Título
            message: Mensagem
            condition_func: Função que retorna True quando deve notificar
            check_interval: Intervalo de verificação (segundos)
            icon_path: Caminho do ícone
        """
        print(f"👁️  Monitorando condição (verifica a cada {check_interval}s)")
        
        def check_condition():
            while True:
                if condition_func():
                    self.notify(title, message, icon_path=icon_path)
                    break
                time.sleep(check_interval)
        
        import threading
        thread = threading.Thread(target=check_condition)
        thread.daemon = True
        thread.start()
        
        return thread
    
    def notify_system_status(self):
        """Notifica status do sistema"""
        try:
            import psutil
            
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            if cpu > 80:
                self.notify(
                    "⚠️ CPU Alta",
                    f"Uso de CPU: {cpu:.1f}%",
                    duration=10
                )
            
            if memory.percent > 80:
                self.notify(
                    "⚠️ Memória Alta",
                    f"Uso de RAM: {memory.percent:.1f}%",
                    duration=10
                )
        except ImportError:
            print("⚠️  psutil não instalado. Instale para monitoramento de sistema.")
    
    def notify_file_change(self, filepath, check_interval=5):
        """Notifica quando arquivo é modificado"""
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"❌ Arquivo não encontrado: {filepath}")
            return
        
        last_modified = filepath.stat().st_mtime
        
        def check_file():
            nonlocal last_modified
            while True:
                try:
                    current_modified = filepath.stat().st_mtime
                    if current_modified > last_modified:
                        self.notify(
                            "📝 Arquivo Modificado",
                            f"{filepath.name} foi modificado",
                            duration=10
                        )
                        last_modified = current_modified
                except:
                    pass
                time.sleep(check_interval)
        
        import threading
        thread = threading.Thread(target=check_file)
        thread.daemon = True
        thread.start()
        
        return thread
    
    def save_log(self):
        """Salva log de notificações"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.notifications_log, f, indent=2, ensure_ascii=False)
    
    def get_statistics(self):
        """Retorna estatísticas de notificações"""
        if not self.notifications_log:
            return None
        
        total = len(self.notifications_log)
        successful = sum(1 for n in self.notifications_log if n.get('status') == 'sent')
        failed = sum(1 for n in self.notifications_log if n.get('status') == 'error')
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': round((successful / total) * 100, 2) if total > 0 else 0
        }
    
    def list_notifications(self, limit=20):
        """Lista notificações recentes"""
        recent = self.notifications_log[-limit:]
        recent.reverse()
        
        print(f"\n📋 Últimas {len(recent)} notificações:")
        print("-" * 60)
        
        for notif in recent:
            status_icon = "✅" if notif.get('status') == 'sent' else "❌"
            timestamp = notif.get('timestamp', 'N/A')
            title = notif.get('title', 'N/A')
            
            print(f"{status_icon} [{timestamp}] {title}")


def main():
    """Interface interativa"""
    notifier = DesktopNotifier()
    
    print("🔔 Sistema de Notificações Desktop\n")
    
    while True:
        print("\n" + "="*50)
        print("1. Enviar notificação")
        print("2. Notificação agendada")
        print("3. Notificações recorrentes")
        print("4. Monitorar arquivo")
        print("5. Status do sistema")
        print("6. Ver histórico")
        print("7. Ver estatísticas")
        print("0. Sair")
        print("="*50)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            title = input("Título: ").strip()
            message = input("Mensagem: ").strip()
            duration = input("Duração em segundos (padrão: 5): ").strip()
            duration = int(duration) if duration.isdigit() else 5
            
            notifier.notify(title, message, duration=duration)
        
        elif choice == "2":
            title = input("Título: ").strip()
            message = input("Mensagem: ").strip()
            delay = input("Delay em segundos: ").strip()
            delay = int(delay) if delay.isdigit() else 5
            
            notifier.notify_scheduled(title, message, delay)
            print("✅ Notificação agendada!")
        
        elif choice == "3":
            title = input("Título: ").strip()
            message = input("Mensagem: ").strip()
            interval = input("Intervalo em segundos: ").strip()
            interval = int(interval) if interval.isdigit() else 60
            count = input("Quantas vezes (Enter para infinito): ").strip()
            count = int(count) if count.isdigit() else None
            
            notifier.notify_recurring(title, message, interval, count)
            print("✅ Notificações recorrentes iniciadas!")
            input("Pressione Enter para parar...")
        
        elif choice == "4":
            filepath = input("Caminho do arquivo: ").strip()
            interval = input("Intervalo de verificação (padrão: 5s): ").strip()
            interval = int(interval) if interval.isdigit() else 5
            
            notifier.notify_file_change(filepath, interval)
            print("✅ Monitoramento iniciado!")
            input("Pressione Enter para parar...")
        
        elif choice == "5":
            notifier.notify_system_status()
        
        elif choice == "6":
            limit = input("Quantas mostrar (padrão: 20): ").strip()
            limit = int(limit) if limit.isdigit() else 20
            notifier.list_notifications(limit)
        
        elif choice == "7":
            stats = notifier.get_statistics()
            if stats:
                print("\n📊 Estatísticas:")
                print(f"  Total: {stats['total']}")
                print(f"  Bem-sucedidas: {stats['successful']}")
                print(f"  Falhas: {stats['failed']}")
                print(f"  Taxa de sucesso: {stats['success_rate']}%")
            else:
                print("Nenhuma notificação registrada.")
        
        elif choice == "0":
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    main()
