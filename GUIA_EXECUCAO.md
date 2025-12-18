# 🚀 Guia de Execução dos Projetos

Este guia mostra como executar cada projeto no seu PC Windows.

## 📋 Pré-requisitos

1. **Python instalado** (versão 3.7 ou superior)
   - Verifique: `python --version` ou `python -V`
   - Baixe em: https://www.python.org/downloads/

2. **pip** (geralmente vem com Python)
   - Verifique: `pip --version`

## 🔧 Instalação Geral

### 1. Clone ou baixe o repositório

Se ainda não tem o código localmente:

```bash
git clone https://github.com/BrayanSilver/Python_Brayan.git
cd Python_Brayan
```

### 2. Instale as dependências globais

Alguns projetos precisam de bibliotecas externas. Instale todas de uma vez:

```bash
# Instala todas as dependências necessárias
pip install psutil requests beautifulsoup4 pandas openpyxl win10toast
```

Ou instale por projeto conforme necessário.

---

## 📁 Como Executar Cada Projeto

### 1. 🔄 Sistema de Backup Automatizado

**Dependências**: Nenhuma (usa apenas bibliotecas padrão)

```bash
cd backup_automatico
python backup_system.py
```

**Teste rápido:**
1. Execute o script
2. Digite o caminho de uma pasta (ex: `C:\Users\SeuNome\Documents`)
3. Escolha opção 1 para criar backup
4. Veja o backup criado na pasta `backups/`

---

### 2. 🖥️ Monitor de Sistema

**Dependências**: `psutil`

```bash
# Instale a dependência
pip install psutil

# Execute
cd monitor_sistema
python monitor.py
```

**Teste rápido:**
1. Execute o script
2. Escolha opção 1 para visualização única
3. Veja informações de CPU, RAM, Disco e processos

---

### 3. 🕷️ Web Scraper Automatizado

**Dependências**: `requests`, `beautifulsoup4`

```bash
# Instale as dependências
pip install requests beautifulsoup4

# Execute
cd web_scraper
python scraper.py
```

**Teste rápido:**
1. Execute o script
2. Escolha opção 5 (Exemplo: Citações)
3. Veja os arquivos `quotes.json` e `quotes.csv` gerados

---

### 4. 📧 Automação de Envio de Emails

**Dependências**: Nenhuma (usa bibliotecas padrão)

```bash
cd automacao_email
python email_sender.py
```

**Configuração necessária:**
- Para Gmail: Ative "App Password" em https://myaccount.google.com/apppasswords
- Servidor: `smtp.gmail.com`
- Porta: `587`

**Teste rápido:**
1. Execute o script
2. Configure seu email e senha/app password
3. Escolha opção 1 para enviar email de teste

---

### 5. 📁 Organizador Automático de Arquivos

**Dependências**: Nenhuma

```bash
cd organizador_arquivos
python organizer.py
```

**Teste rápido:**
1. Execute o script
2. Digite o caminho de uma pasta com arquivos (ex: `C:\Users\SeuNome\Downloads`)
3. Escolha método de organização (1, 2, 3 ou 4)
4. Confirme e veja os arquivos organizados

⚠️ **Cuidado**: Este script move arquivos! Teste primeiro em uma pasta de teste.

---

### 6. 🪟 Automação de Tarefas Windows

**Dependências**: Nenhuma (opcional: `pywin32` para funções avançadas)

```bash
cd automacao_windows
python task_automation.py
```

**Teste rápido:**
1. Execute o script
2. Escolha opção 3 para listar processos
3. Escolha opção 6 para ver informações do sistema

---

### 7. 👁️ Monitor de Logs em Tempo Real

**Dependências**: Nenhuma

```bash
cd monitor_logs
python log_monitor.py
```

**Teste rápido:**
1. Execute o script
2. Pressione Enter para criar log de exemplo
3. Escolha opção 1 para monitorar em tempo real
4. Abra outro terminal e adicione linhas ao arquivo `example.log`

---

### 8. 📥 Automação de Downloads

**Dependências**: `requests`

```bash
# Instale a dependência
pip install requests

# Execute
cd automacao_downloads
python download_manager.py
```

**Teste rápido:**
1. Execute o script
2. Escolha opção 1
3. Digite uma URL de download (ex: `https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe`)
4. Veja o download com barra de progresso

---

### 9. 🔔 Sistema de Notificações Desktop

**Dependências**: `win10toast` (opcional: `psutil`)

```bash
# Instale a dependência
pip install win10toast

# Execute
cd notificacoes_desktop
python notifier.py
```

**Teste rápido:**
1. Execute o script
2. Escolha opção 1
3. Digite título e mensagem
4. Veja a notificação aparecer no Windows!

---

### 10. 📊 Gerador Automático de Relatórios

**Dependências**: `pandas`, `openpyxl` (para Excel)

```bash
# Instale as dependências
pip install pandas openpyxl

# Execute
cd gerador_relatorios
python report_generator.py
```

**Teste rápido:**
1. Execute o script
2. Escolha opção 1 para gerar relatório HTML
3. Abra o arquivo gerado em `reports/` no navegador

---

## 🎯 Script de Instalação Rápida

Crie um arquivo `instalar_dependencias.bat`:

```batch
@echo off
echo Instalando todas as dependencias dos projetos...
pip install psutil requests beautifulsoup4 pandas openpyxl win10toast
echo.
echo Instalacao concluida!
pause
```

Execute clicando duas vezes no arquivo `.bat`.

---

## 🐛 Solução de Problemas Comuns

### Erro: "pip não é reconhecido"
- Use: `python -m pip install [biblioteca]`
- Ou adicione Python ao PATH do Windows

### Erro: "Módulo não encontrado"
- Instale a dependência: `pip install [nome_do_modulo]`
- Verifique se está no diretório correto do projeto

### Erro de permissão
- Execute o terminal como Administrador
- Ou use: `pip install --user [biblioteca]`

### Erro no Windows com caracteres especiais
- Certifique-se de usar UTF-8 no terminal
- Ou execute: `chcp 65001` antes de rodar scripts

---

## 📝 Exemplos de Uso Rápido

### Testar Backup
```bash
cd backup_automatico
python backup_system.py
# Digite: C:\Users\SeuNome\Documents
# Escolha: 1
```

### Testar Monitor de Sistema
```bash
cd monitor_sistema
pip install psutil
python monitor.py
# Escolha: 1
```

### Testar Notificações
```bash
cd notificacoes_desktop
pip install win10toast
python notifier.py
# Escolha: 1
# Título: Teste
# Mensagem: Funcionou!
```

### Testar Downloads
```bash
cd automacao_downloads
pip install requests
python download_manager.py
# Escolha: 1
# URL: https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
```

---

## 🎓 Dicas

1. **Sempre teste em ambiente seguro** - Alguns scripts modificam arquivos
2. **Leia o README de cada projeto** - Tem exemplos específicos
3. **Use ambientes virtuais** (opcional mas recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install [dependencias]
   ```

4. **Verifique Python instalado**:
   ```bash
   python --version
   ```

---

## ✅ Checklist Rápido

- [ ] Python instalado (`python --version`)
- [ ] pip funcionando (`pip --version`)
- [ ] Dependências instaladas (`pip install psutil requests beautifulsoup4 pandas openpyxl win10toast`)
- [ ] Navegou até a pasta do projeto (`cd nome_do_projeto`)
- [ ] Executou o script (`python arquivo.py`)

---

## 🆘 Precisa de Ajuda?

1. Verifique se todas as dependências estão instaladas
2. Leia o README.md específico de cada projeto
3. Verifique se está no diretório correto
4. Execute como Administrador se necessário

---

**Boa sorte testando os projetos! 🚀**
