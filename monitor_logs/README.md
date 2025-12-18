# 👁️ Monitor de Logs em Tempo Real

Sistema completo para monitorar arquivos de log em tempo real, detectar padrões e gerar alertas.

## 🚀 Funcionalidades

- ✅ Monitoramento em tempo real
- ✅ Detecção de padrões (regex)
- ✅ Sistema de alertas configurável
- ✅ Busca no histórico
- ✅ Estatísticas de ocorrências
- ✅ Exportação de estatísticas
- ✅ Buffer de linhas recentes

## 📦 Instalação

Não requer dependências externas! Usa apenas bibliotecas padrão do Python.

## 💻 Uso

### Uso Básico

```python
from log_monitor import LogMonitor

# Criar monitor
monitor = LogMonitor("app.log")

# Adicionar padrões
monitor.add_pattern("ERROR", r"ERROR")
monitor.add_pattern("WARNING", r"WARNING")

# Adicionar alerta (dispara após 5 erros)
monitor.add_alert("Muitos Erros", r"ERROR", threshold=5)

# Monitorar em tempo real
monitor.monitor(interval=1)  # Verifica a cada 1 segundo
```

### Executar Interface

```bash
python log_monitor.py
```

## 🔍 Padrões e Alertas

### Adicionar Padrão

```python
# Padrão simples
monitor.add_pattern("ERROR", r"ERROR")

# Padrão com ação
def alert_error(line):
    print(f"🚨 Erro encontrado: {line}")

monitor.add_pattern("ERROR", r"ERROR", action=alert_error)
```

### Adicionar Alerta

```python
# Alerta que dispara após 3 ocorrências
monitor.add_alert("Muitos Erros", r"ERROR", threshold=3)
```

## 📊 Funcionalidades

### Monitoramento Contínuo

```python
# Monitora indefinidamente
monitor.monitor(interval=1)

# Monitora por 60 segundos
monitor.monitor(interval=1, duration=60)
```

### Busca no Log

```python
# Busca padrão no log completo
matches = monitor.search_log(r"ERROR.*timeout", max_results=10)
```

### Estatísticas

```python
# Ver estatísticas
monitor.show_statistics()

# Exportar para JSON
monitor.export_statistics("stats.json")
```

## 📝 Exemplo de Log

```
[2025-01-15 10:00:00] INFO: Sistema iniciado
[2025-01-15 10:00:05] ERROR: Falha na conexão
[2025-01-15 10:00:10] WARNING: Memória baixa
[2025-01-15 10:00:15] INFO: Processo concluído
```

## 🎯 Casos de Uso

- Monitoramento de aplicações
- Detecção de erros em tempo real
- Análise de logs de servidor
- Alertas de sistema
- Debugging de aplicações
- Análise de segurança

## 🔧 Recursos Avançados

- **Regex Patterns**: Suporte completo a expressões regulares
- **Ações Customizadas**: Execute funções quando padrões são encontrados
- **Alertas Inteligentes**: Dispara após N ocorrências
- **Buffer Circular**: Mantém últimas N linhas em memória
- **Exportação**: Salva estatísticas em JSON
