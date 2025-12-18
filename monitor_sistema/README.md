# 🖥️ Monitor de Sistema

Monitor completo de recursos do sistema: CPU, RAM, Disco, Rede e Processos em tempo real.

## 🚀 Funcionalidades

- ✅ Monitoramento de CPU (uso geral e por núcleo)
- ✅ Monitoramento de Memória RAM
- ✅ Monitoramento de Discos (todos os volumes)
- ✅ Monitoramento de Rede (tráfego)
- ✅ Top processos (maior uso de CPU)
- ✅ Alertas automáticos de uso excessivo
- ✅ Logging em JSON
- ✅ Monitoramento contínuo

## 📦 Instalação

```bash
pip install psutil
```

## 💻 Uso

### Uso Básico

```python
from monitor import SystemMonitor

# Criar monitor
monitor = SystemMonitor()

# Visualizar informações uma vez
monitor.display_info()

# Monitorar continuamente (a cada 5 segundos)
monitor.monitor_continuous(interval=5)

# Verificar alertas
monitor.check_alerts(cpu_threshold=80, memory_threshold=80)
```

### Executar Interface

```bash
python monitor.py
```

## 📊 Exemplo de Saída

```
============================================================
🖥️  MONITOR DE SISTEMA - 2025-01-15T14:30:22
============================================================

📊 CPU:
  Uso: 45.2%
  Núcleos: 8
  Por núcleo: 12.3%, 15.6%, 8.9%, 10.2%

💾 MEMÓRIA RAM:
  Total: 16.0 GB
  Usado: 8.5 GB (53.1%)
  Disponível: 7.5 GB

💿 DISCOS:
  C:\ (C:\):
    Usado: 120.5 GB / 500.0 GB (24.1%)
    Livre: 379.5 GB

🔥 TOP 5 PROCESSOS (CPU):
  1. chrome.exe: CPU 15.2% | RAM 8.5%
  2. code.exe: CPU 5.3% | RAM 4.2%
```

## 🔔 Alertas

O sistema pode alertar quando:
- CPU ultrapassa 80% (configurável)
- RAM ultrapassa 80% (configurável)
- Disco ultrapassa 90% (configurável)

## 📝 Logging

Todas as informações são salvas em `system_log.json` para análise posterior.

## 🎯 Casos de Uso

- Monitoramento de servidores
- Diagnóstico de performance
- Identificação de processos problemáticos
- Análise de uso de recursos
