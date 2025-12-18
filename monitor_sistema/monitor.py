"""
Monitor de Sistema
Monitora CPU, RAM, Disco e processos em tempo real
"""

import psutil
import time
from datetime import datetime
import json
from pathlib import Path


class SystemMonitor:
    def __init__(self, log_file="system_log.json"):
        """Inicializa o monitor de sistema"""
        self.log_file = Path(log_file)
        self.log_data = []
        
    def get_cpu_info(self):
        """Retorna informações sobre CPU"""
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "per_core": psutil.cpu_percent(interval=1, percpu=True)
        }
    
    def get_memory_info(self):
        """Retorna informações sobre memória RAM"""
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent": mem.percent,
            "free_gb": round(mem.free / (1024**3), 2)
        }
    
    def get_disk_info(self):
        """Retorna informações sobre discos"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent
                })
            except PermissionError:
                continue
        return disks
    
    def get_network_info(self):
        """Retorna informações sobre rede"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent_mb": round(net_io.bytes_sent / (1024**2), 2),
            "bytes_recv_mb": round(net_io.bytes_recv / (1024**2), 2),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    def get_top_processes(self, n=10):
        """Retorna os N processos que mais consomem CPU"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Ordena por CPU
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        return processes[:n]
    
    def get_system_info(self):
        """Retorna informações completas do sistema"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "top_processes": self.get_top_processes(5)
        }
    
    def display_info(self):
        """Exibe informações do sistema formatadas"""
        info = self.get_system_info()
        
        print("\n" + "="*60)
        print(f"🖥️  MONITOR DE SISTEMA - {info['timestamp']}")
        print("="*60)
        
        # CPU
        print("\n📊 CPU:")
        print(f"  Uso: {info['cpu']['usage_percent']}%")
        print(f"  Núcleos: {info['cpu']['count']}")
        if info['cpu']['per_core']:
            print(f"  Por núcleo: {', '.join([f'{c:.1f}%' for c in info['cpu']['per_core']])}")
        
        # Memória
        print("\n💾 MEMÓRIA RAM:")
        mem = info['memory']
        print(f"  Total: {mem['total_gb']} GB")
        print(f"  Usado: {mem['used_gb']} GB ({mem['percent']}%)")
        print(f"  Disponível: {mem['available_gb']} GB")
        
        # Disco
        print("\n💿 DISCOS:")
        for disk in info['disk']:
            print(f"  {disk['device']} ({disk['mountpoint']}):")
            print(f"    Usado: {disk['used_gb']} GB / {disk['total_gb']} GB ({disk['percent']}%)")
            print(f"    Livre: {disk['free_gb']} GB")
        
        # Rede
        print("\n🌐 REDE:")
        net = info['network']
        print(f"  Enviado: {net['bytes_sent_mb']} MB")
        print(f"  Recebido: {net['bytes_recv_mb']} MB")
        
        # Top Processos
        print("\n🔥 TOP 5 PROCESSOS (CPU):")
        for i, proc in enumerate(info['top_processes'], 1):
            cpu = proc.get('cpu_percent', 0) or 0
            mem = proc.get('memory_percent', 0) or 0
            name = proc.get('name', 'N/A')
            print(f"  {i}. {name}: CPU {cpu:.1f}% | RAM {mem:.1f}%")
        
        print("\n" + "="*60)
    
    def log_info(self):
        """Salva informações no log"""
        info = self.get_system_info()
        self.log_data.append(info)
        
        # Salva no arquivo
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.log_data, f, indent=2, ensure_ascii=False)
    
    def monitor_continuous(self, interval=5, duration=None):
        """Monitora o sistema continuamente"""
        print(f"🔄 Iniciando monitoramento (intervalo: {interval}s)")
        print("Pressione Ctrl+C para parar\n")
        
        start_time = time.time()
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n--- Iteração {iteration} ---")
                self.display_info()
                self.log_info()
                
                if duration and (time.time() - start_time) >= duration:
                    print(f"\n⏱️  Tempo de monitoramento ({duration}s) concluído.")
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoramento interrompido pelo usuário.")
            print(f"📝 Log salvo em: {self.log_file}")
    
    def check_alerts(self, cpu_threshold=80, memory_threshold=80, disk_threshold=90):
        """Verifica alertas de uso excessivo"""
        info = self.get_system_info()
        alerts = []
        
        if info['cpu']['usage_percent'] > cpu_threshold:
            alerts.append(f"⚠️  ALERTA: CPU em {info['cpu']['usage_percent']:.1f}% (limite: {cpu_threshold}%)")
        
        if info['memory']['percent'] > memory_threshold:
            alerts.append(f"⚠️  ALERTA: RAM em {info['memory']['percent']:.1f}% (limite: {memory_threshold}%)")
        
        for disk in info['disk']:
            if disk['percent'] > disk_threshold:
                alerts.append(f"⚠️  ALERTA: Disco {disk['device']} em {disk['percent']:.1f}% (limite: {disk_threshold}%)")
        
        if alerts:
            print("\n🚨 ALERTAS:")
            for alert in alerts:
                print(f"  {alert}")
        
        return alerts


def main():
    """Exemplo de uso"""
    monitor = SystemMonitor()
    
    print("🖥️  Monitor de Sistema\n")
    print("1. Visualização única")
    print("2. Monitoramento contínuo")
    print("3. Verificar alertas")
    print("4. Ver log")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == "1":
        monitor.display_info()
        monitor.log_info()
    elif choice == "2":
        interval = input("Intervalo em segundos (padrão: 5): ").strip()
        interval = int(interval) if interval.isdigit() else 5
        monitor.monitor_continuous(interval=interval)
    elif choice == "3":
        monitor.check_alerts()
    elif choice == "4":
        if monitor.log_file.exists():
            with open(monitor.log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"\n📝 Total de registros: {len(data)}")
            if data:
                print(f"Último registro: {data[-1]['timestamp']}")
        else:
            print("Nenhum log encontrado.")


if __name__ == "__main__":
    main()
