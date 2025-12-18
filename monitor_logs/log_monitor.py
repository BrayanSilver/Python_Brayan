"""
Monitor de Logs em Tempo Real
Monitora arquivos de log em tempo real e detecta padrões
"""

import os
import time
from pathlib import Path
from datetime import datetime
import re
from collections import deque
import json


class LogMonitor:
    def __init__(self, log_file, buffer_size=100):
        """
        Inicializa o monitor de logs
        
        Args:
            log_file: Caminho do arquivo de log
            buffer_size: Tamanho do buffer de linhas
        """
        self.log_file = Path(log_file)
        self.buffer_size = buffer_size
        self.last_position = 0
        self.patterns = {}
        self.alerts = []
        self.line_buffer = deque(maxlen=buffer_size)
        
        if not self.log_file.exists():
            print(f"⚠️  Arquivo não encontrado: {log_file}")
            print("Criando arquivo...")
            self.log_file.touch()
    
    def add_pattern(self, name, pattern, action=None):
        """
        Adiciona um padrão para monitorar
        
        Args:
            name: Nome do padrão
            pattern: Regex pattern ou string simples
            action: Função a executar quando encontrado (opcional)
        """
        self.patterns[name] = {
            'pattern': re.compile(pattern) if isinstance(pattern, str) else pattern,
            'action': action,
            'count': 0,
            'matches': []
        }
    
    def add_alert(self, name, pattern, threshold=1):
        """
        Adiciona um alerta que dispara após N ocorrências
        
        Args:
            name: Nome do alerta
            pattern: Padrão a procurar
            threshold: Número de ocorrências para disparar
        """
        self.alerts.append({
            'name': name,
            'pattern': re.compile(pattern) if isinstance(pattern, str) else pattern,
            'threshold': threshold,
            'count': 0
        })
    
    def read_new_lines(self):
        """Lê novas linhas do arquivo de log"""
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                # Vai para a última posição conhecida
                f.seek(self.last_position)
                
                new_lines = []
                for line in f:
                    new_lines.append(line.rstrip('\n\r'))
                    self.line_buffer.append(line.rstrip('\n\r'))
                
                # Atualiza posição
                self.last_position = f.tell()
                
                return new_lines
        except Exception as e:
            print(f"❌ Erro ao ler log: {e}")
            return []
    
    def check_patterns(self, lines):
        """Verifica padrões nas linhas"""
        for line in lines:
            for name, pattern_info in self.patterns.items():
                if pattern_info['pattern'].search(line):
                    pattern_info['count'] += 1
                    pattern_info['matches'].append({
                        'timestamp': datetime.now().isoformat(),
                        'line': line
                    })
                    
                    # Executa ação se definida
                    if pattern_info['action']:
                        pattern_info['action'](line)
    
    def check_alerts(self, lines):
        """Verifica alertas"""
        for line in lines:
            for alert in self.alerts:
                if alert['pattern'].search(line):
                    alert['count'] += 1
                    
                    if alert['count'] >= alert['threshold']:
                        print(f"🚨 ALERTA: {alert['name']} - {alert['count']} ocorrências!")
                        alert['count'] = 0  # Reset contador
    
    def monitor(self, interval=1, duration=None):
        """
        Monitora o log continuamente
        
        Args:
            interval: Intervalo entre verificações (segundos)
            duration: Duração do monitoramento (None = infinito)
        """
        print(f"👁️  Monitorando: {self.log_file}")
        print(f"⏱️  Intervalo: {interval}s")
        if duration:
            print(f"⏰ Duração: {duration}s")
        print("Pressione Ctrl+C para parar\n")
        
        start_time = time.time()
        iteration = 0
        
        try:
            while True:
                iteration += 1
                new_lines = self.read_new_lines()
                
                if new_lines:
                    print(f"\n--- Novas linhas ({len(new_lines)}) ---")
                    for line in new_lines:
                        print(f"  {line}")
                    
                    # Verifica padrões
                    self.check_patterns(new_lines)
                    
                    # Verifica alertas
                    self.check_alerts(new_lines)
                
                # Mostra estatísticas periodicamente
                if iteration % 10 == 0:
                    self.show_statistics()
                
                # Verifica duração
                if duration and (time.time() - start_time) >= duration:
                    print(f"\n⏱️  Tempo de monitoramento ({duration}s) concluído.")
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoramento interrompido.")
            self.show_statistics()
    
    def show_statistics(self):
        """Mostra estatísticas dos padrões encontrados"""
        if not self.patterns:
            return
        
        print("\n📊 Estatísticas de Padrões:")
        print("-" * 50)
        for name, pattern_info in self.patterns.items():
            print(f"  {name}: {pattern_info['count']} ocorrências")
    
    def search_log(self, pattern, max_results=10):
        """Busca padrão no log completo"""
        matches = []
        pattern_re = re.compile(pattern) if isinstance(pattern, str) else pattern
        
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if pattern_re.search(line):
                        matches.append({
                            'line_number': line_num,
                            'content': line.rstrip('\n\r')
                        })
                        if len(matches) >= max_results:
                            break
        except Exception as e:
            print(f"❌ Erro ao buscar: {e}")
        
        return matches
    
    def get_recent_lines(self, n=10):
        """Retorna as últimas N linhas"""
        return list(self.line_buffer)[-n:]
    
    def export_statistics(self, filename="log_statistics.json"):
        """Exporta estatísticas para JSON"""
        stats = {
            'log_file': str(self.log_file),
            'timestamp': datetime.now().isoformat(),
            'patterns': {}
        }
        
        for name, pattern_info in self.patterns.items():
            stats['patterns'][name] = {
                'count': pattern_info['count'],
                'recent_matches': pattern_info['matches'][-10:]  # Últimas 10
            }
        
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Estatísticas exportadas: {filepath}")


def create_example_log():
    """Cria um arquivo de log de exemplo"""
    log_file = Path("example.log")
    
    messages = [
        "INFO: Sistema iniciado",
        "ERROR: Falha na conexão",
        "WARNING: Memória baixa",
        "INFO: Processo concluído",
        "ERROR: Timeout na requisição",
        "INFO: Backup realizado",
        "ERROR: Arquivo não encontrado",
        "WARNING: Disco quase cheio",
    ]
    
    with open(log_file, 'w', encoding='utf-8') as f:
        for msg in messages:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg}\n")
    
    print(f"✅ Log de exemplo criado: {log_file}")
    return log_file


def main():
    """Interface interativa"""
    print("👁️  Monitor de Logs em Tempo Real\n")
    
    log_file = input("Caminho do arquivo de log (ou Enter para exemplo): ").strip()
    
    if not log_file:
        log_file = create_example_log()
    
    monitor = LogMonitor(log_file)
    
    # Adiciona padrões comuns
    monitor.add_pattern("ERROR", r"ERROR", lambda line: print(f"  ⚠️  Erro detectado: {line}"))
    monitor.add_pattern("WARNING", r"WARNING")
    monitor.add_pattern("INFO", r"INFO")
    
    # Adiciona alerta
    monitor.add_alert("Muitos Erros", r"ERROR", threshold=3)
    
    print("\n1. Monitorar em tempo real")
    print("2. Buscar padrão no log")
    print("3. Ver últimas linhas")
    print("4. Ver estatísticas")
    print("5. Exportar estatísticas")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == "1":
        interval = input("Intervalo em segundos (padrão: 1): ").strip()
        interval = float(interval) if interval.replace('.', '').isdigit() else 1.0
        
        duration = input("Duração em segundos (Enter para infinito): ").strip()
        duration = float(duration) if duration.replace('.', '').isdigit() else None
        
        monitor.monitor(interval=interval, duration=duration)
    
    elif choice == "2":
        pattern = input("Padrão a buscar (regex): ").strip()
        max_results = input("Máximo de resultados (padrão: 10): ").strip()
        max_results = int(max_results) if max_results.isdigit() else 10
        
        matches = monitor.search_log(pattern, max_results=max_results)
        print(f"\n✅ {len(matches)} correspondências encontradas:")
        for match in matches:
            print(f"  Linha {match['line_number']}: {match['content']}")
    
    elif choice == "3":
        n = input("Quantas linhas (padrão: 10): ").strip()
        n = int(n) if n.isdigit() else 10
        
        lines = monitor.get_recent_lines(n)
        print(f"\n📋 Últimas {len(lines)} linhas:")
        for line in lines:
            print(f"  {line}")
    
    elif choice == "4":
        monitor.show_statistics()
    
    elif choice == "5":
        monitor.export_statistics()


if __name__ == "__main__":
    main()
