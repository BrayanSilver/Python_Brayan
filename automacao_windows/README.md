# 🪟 Automação de Tarefas Windows

Sistema completo de automação para tarefas comuns do Windows.

## 🚀 Funcionalidades

- ✅ Abrir/fechar aplicativos
- ✅ Gerenciar processos
- ✅ Limpar arquivos temporários
- ✅ Limpar lixeira
- ✅ Verificar espaço em disco
- ✅ Informações do sistema
- ✅ Bloquear tela
- ✅ Desligar/reiniciar computador
- ✅ Agendar tarefas
- ✅ Executar scripts PowerShell

## 📦 Instalação

Usa principalmente bibliotecas padrão do Python. Para algumas funções avançadas:

```bash
pip install pywin32
```

## 💻 Uso

### Uso Básico

```python
from task_automation import WindowsAutomation

automation = WindowsAutomation()

# Abrir aplicativo
automation.open_app("notepad.exe")

# Fechar aplicativo
automation.close_app("notepad.exe")

# Listar processos
processes = automation.list_running_processes()

# Limpar temporários
automation.clean_temp_files()

# Ver espaço em disco
disk_info = automation.get_disk_space("C:")

# Bloquear tela
automation.lock_screen()

# Informações do sistema
info = automation.get_system_info()
```

### Executar Interface

```bash
python task_automation.py
```

## ⚠️ Privilégios de Administrador

Algumas funções requerem privilégios de administrador:
- Desligar/reiniciar computador
- Agendar tarefas
- Algumas operações de sistema

Execute o script como administrador quando necessário.

## 🔧 Funções Disponíveis

### Gerenciamento de Aplicativos
- `open_app()` - Abre aplicativo
- `close_app()` - Fecha processo
- `list_running_processes()` - Lista processos

### Limpeza
- `clean_temp_files()` - Limpa arquivos temporários
- `clean_recycle_bin()` - Limpa lixeira

### Sistema
- `get_disk_space()` - Espaço em disco
- `get_system_info()` - Informações do sistema
- `lock_screen()` - Bloqueia tela

### Controle de Energia
- `shutdown()` - Desliga computador
- `restart()` - Reinicia computador
- `cancel_shutdown()` - Cancela desligamento

### Automação
- `schedule_task()` - Agenda tarefa
- `run_powershell_script()` - Executa PowerShell

## 🎯 Casos de Uso

- Automação de manutenção do sistema
- Limpeza automática de arquivos
- Gerenciamento de processos
- Automação de tarefas repetitivas
- Monitoramento de sistema

## ⚠️ Avisos

- Algumas funções podem afetar o sistema
- Sempre teste em ambiente seguro
- Backup importante antes de limpezas
- Desligar/reiniciar requer confirmação
