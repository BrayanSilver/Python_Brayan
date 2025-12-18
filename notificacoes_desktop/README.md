# 🔔 Sistema de Notificações Desktop

Sistema completo para enviar notificações desktop no Windows com agendamento e monitoramento.

## 🚀 Funcionalidades

- ✅ Notificações desktop (Windows 10+)
- ✅ Notificações agendadas
- ✅ Notificações recorrentes
- ✅ Monitoramento de arquivos
- ✅ Monitoramento de sistema
- ✅ Notificações condicionais
- ✅ Histórico completo
- ✅ Estatísticas

## 📦 Instalação

```bash
pip install win10toast
```

Opcional (para monitoramento de sistema):
```bash
pip install psutil
```

## 💻 Uso

### Uso Básico

```python
from notifier import DesktopNotifier

# Criar notificador
notifier = DesktopNotifier()

# Enviar notificação simples
notifier.notify(
    title="Tarefa Concluída",
    message="O processamento foi finalizado!",
    duration=5
)

# Notificação agendada (5 segundos)
notifier.notify_scheduled(
    title="Lembrete",
    message="Não se esqueça!",
    delay_seconds=5
)

# Notificações recorrentes (a cada 60 segundos)
notifier.notify_recurring(
    title="Checkpoint",
    message="Verifique o progresso",
    interval_seconds=60,
    count=5  # ou None para infinito
)
```

### Executar Interface

```bash
python notifier.py
```

## 🔔 Tipos de Notificações

### Notificação Simples

```python
notifier.notify(
    title="Título",
    message="Mensagem",
    duration=5,  # segundos
    icon_path="icon.ico"  # opcional
)
```

### Notificação Agendada

```python
# Envia após 10 segundos
notifier.notify_scheduled(
    title="Lembrete",
    message="Fazer backup",
    delay_seconds=10
)
```

### Notificações Recorrentes

```python
# A cada 30 segundos, 10 vezes
notifier.notify_recurring(
    title="Status",
    message="Sistema funcionando",
    interval_seconds=30,
    count=10
)
```

### Monitoramento de Arquivo

```python
# Notifica quando arquivo é modificado
notifier.notify_file_change(
    filepath="dados.json",
    check_interval=5  # verifica a cada 5 segundos
)
```

### Monitoramento de Sistema

```python
# Notifica se CPU ou RAM estiverem altos
notifier.notify_system_status()
```

### Notificação Condicional

```python
def check_condition():
    # Sua lógica aqui
    return some_condition_is_true

notifier.notify_on_condition(
    title="Condição Atendida",
    message="A condição foi satisfeita!",
    condition_func=check_condition,
    check_interval=5
)
```

## 📊 Histórico e Estatísticas

```python
# Ver histórico
notifier.list_notifications(limit=20)

# Ver estatísticas
stats = notifier.get_statistics()
print(f"Total: {stats['total']}")
print(f"Taxa de sucesso: {stats['success_rate']}%")
```

## 🎯 Casos de Uso

- Lembretes de tarefas
- Notificações de processos concluídos
- Alertas de sistema
- Monitoramento de arquivos
- Notificações de backup
- Alertas de erro
- Lembretes periódicos

## ⚙️ Configurações

- **duration**: Duração da notificação (padrão: 5 segundos)
- **icon_path**: Caminho do ícone personalizado
- **threaded**: Executa em thread separada (padrão: True)

## 📝 Logging

Todas as notificações são registradas em `notifications_log.json` com:
- Timestamp
- Título e mensagem
- Status (sent/error)
