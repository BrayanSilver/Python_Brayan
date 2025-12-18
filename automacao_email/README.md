# 📧 Automação de Envio de Emails

Sistema completo para envio automatizado de emails individuais e em massa.

## 🚀 Funcionalidades

- ✅ Envio de emails individuais
- ✅ Envio em massa (bulk)
- ✅ Suporte a HTML
- ✅ Anexos de arquivos
- ✅ Templates personalizados
- ✅ Leitura de destinatários via CSV
- ✅ Logging de envios
- ✅ Suporte a múltiplos servidores SMTP

## 📦 Instalação

Usa apenas bibliotecas padrão do Python! Não requer instalação adicional.

## ⚙️ Configuração

### Gmail

1. Ative a verificação em 2 etapas
2. Gere uma "App Password" em: https://myaccount.google.com/apppasswords
3. Use:
   - Servidor: `smtp.gmail.com`
   - Porta: `587`

### Outlook/Hotmail

- Servidor: `smtp-mail.outlook.com`
- Porta: `587`

### Outros Servidores

Consulte a documentação do seu provedor de email.

## 💻 Uso

### Uso Básico

```python
from email_sender import EmailSender

# Configurar
sender = EmailSender(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    email="seu_email@gmail.com",
    password="sua_app_password"
)

# Conectar
sender.connect()

# Enviar email simples
sender.send_email(
    to_email="destinatario@example.com",
    subject="Assunto do Email",
    body="Corpo do email em texto"
)

# Enviar com HTML
html_body = "<h1>Olá!</h1><p>Este é um email HTML.</p>"
sender.send_email(
    to_email="destinatario@example.com",
    subject="Email HTML",
    body="Versão texto",
    html_body=html_body,
    attachments=["arquivo.pdf"]
)

# Desconectar
sender.disconnect()
```

### Envio em Massa

```python
# Lista de destinatários
recipients = [
    {'name': 'João', 'email': 'joao@example.com'},
    {'name': 'Maria', 'email': 'maria@example.com'},
]

# Templates
subject_template = "Olá {name}!"
body_template = "Olá {name}, este é um email personalizado."

# Enviar
sender.send_bulk_emails(recipients, subject_template, body_template)
```

### Envio via CSV

```csv
name,email,company
João Silva,joao@example.com,Empresa A
Maria Santos,maria@example.com,Empresa B
```

```python
sender.send_from_csv(
    csv_file="recipients.csv",
    subject_template="Olá {name}!",
    body_template="Olá {name} da {company}!"
)
```

## 📝 Exemplo de CSV

Execute o script e escolha a opção 3 para criar um CSV de exemplo.

## 🔒 Segurança

- ⚠️ **NUNCA** commite senhas no código
- Use variáveis de ambiente para credenciais
- Para Gmail, use App Passwords, não a senha principal
- Considere usar serviços como SendGrid para produção

## 🎯 Casos de Uso

- Newsletters
- Notificações automatizadas
- Relatórios periódicos
- Campanhas de marketing
- Lembretes automáticos
