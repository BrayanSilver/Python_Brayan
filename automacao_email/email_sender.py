"""
Automação de Envio de Emails
Sistema completo para envio automatizado de emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
from pathlib import Path
from datetime import datetime
import csv


class EmailSender:
    def __init__(self, smtp_server, smtp_port, email, password):
        """
        Inicializa o sistema de envio de emails
        
        Args:
            smtp_server: Servidor SMTP (ex: smtp.gmail.com)
            smtp_port: Porta SMTP (ex: 587)
            email: Seu email
            password: Senha ou app password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.sent_log = []
    
    def connect(self):
        """Conecta ao servidor SMTP"""
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.email, self.password)
            print("✅ Conectado ao servidor SMTP")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do servidor"""
        if hasattr(self, 'server'):
            self.server.quit()
            print("✅ Desconectado do servidor")
    
    def send_email(self, to_email, subject, body, html_body=None, attachments=None):
        """
        Envia um email
        
        Args:
            to_email: Email do destinatário
            subject: Assunto
            body: Corpo do email (texto)
            html_body: Corpo HTML (opcional)
            attachments: Lista de caminhos de arquivos (opcional)
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Adiciona corpo texto
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Adiciona corpo HTML se fornecido
            if html_body:
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Adiciona anexos
            if attachments:
                for filepath in attachments:
                    self._add_attachment(msg, filepath)
            
            # Envia email
            text = msg.as_string()
            self.server.sendmail(self.email, to_email, text)
            
            # Log
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'to': to_email,
                'subject': subject,
                'status': 'sent'
            }
            self.sent_log.append(log_entry)
            
            print(f"✅ Email enviado para: {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'to': to_email,
                'subject': subject,
                'status': 'error',
                'error': str(e)
            }
            self.sent_log.append(log_entry)
            return False
    
    def _add_attachment(self, msg, filepath):
        """Adiciona um anexo ao email"""
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"⚠️  Arquivo não encontrado: {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filepath.name}'
        )
        msg.attach(part)
    
    def send_bulk_emails(self, recipients, subject_template, body_template, html_template=None):
        """
        Envia emails em massa
        
        Args:
            recipients: Lista de dicts com dados dos destinatários
            subject_template: Template do assunto (usa {name}, {email}, etc)
            body_template: Template do corpo (usa {name}, {email}, etc)
            html_template: Template HTML (opcional)
        """
        print(f"📧 Enviando {len(recipients)} emails...\n")
        
        success = 0
        failed = 0
        
        for recipient in recipients:
            try:
                # Substitui variáveis no template
                subject = subject_template.format(**recipient)
                body = body_template.format(**recipient)
                html_body = html_template.format(**recipient) if html_template else None
                
                if self.send_email(
                    recipient['email'],
                    subject,
                    body,
                    html_body
                ):
                    success += 1
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"❌ Erro ao processar {recipient.get('email', 'N/A')}: {e}")
                failed += 1
        
        print(f"\n✅ Enviados: {success} | ❌ Falhas: {failed}")
        return success, failed
    
    def send_from_csv(self, csv_file, subject_template, body_template, html_template=None):
        """Envia emails a partir de um arquivo CSV"""
        recipients = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            recipients = list(reader)
        
        return self.send_bulk_emails(recipients, subject_template, body_template, html_template)
    
    def save_log(self, filename="email_log.json"):
        """Salva o log de emails enviados"""
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.sent_log, f, indent=2, ensure_ascii=False)
        print(f"📝 Log salvo em: {filepath}")


def create_example_csv():
    """Cria um arquivo CSV de exemplo"""
    data = [
        {'name': 'João Silva', 'email': 'joao@example.com', 'company': 'Empresa A'},
        {'name': 'Maria Santos', 'email': 'maria@example.com', 'company': 'Empresa B'},
        {'name': 'Pedro Costa', 'email': 'pedro@example.com', 'company': 'Empresa C'},
    ]
    
    filepath = Path('recipients_example.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'email', 'company'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ Arquivo CSV de exemplo criado: {filepath}")
    return filepath


def main():
    """Interface interativa"""
    print("📧 Sistema de Automação de Emails\n")
    
    # Configuração
    print("Configuração do servidor SMTP:")
    smtp_server = input("Servidor SMTP (ex: smtp.gmail.com): ").strip() or "smtp.gmail.com"
    smtp_port = input("Porta (ex: 587): ").strip() or "587"
    smtp_port = int(smtp_port) if smtp_port.isdigit() else 587
    
    email = input("Seu email: ").strip()
    password = input("Senha/App Password: ").strip()
    
    sender = EmailSender(smtp_server, smtp_port, email, password)
    
    if not sender.connect():
        print("❌ Não foi possível conectar. Verifique as credenciais.")
        return
    
    try:
        print("\n1. Enviar email único")
        print("2. Enviar emails em massa (CSV)")
        print("3. Criar CSV de exemplo")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            to_email = input("Email destinatário: ").strip()
            subject = input("Assunto: ").strip()
            body = input("Corpo do email: ").strip()
            
            sender.send_email(to_email, subject, body)
        
        elif choice == "2":
            csv_file = input("Caminho do arquivo CSV: ").strip()
            if not Path(csv_file).exists():
                print("❌ Arquivo não encontrado.")
                return
            
            subject_template = input("Template do assunto (use {name}, {email}): ").strip()
            body_template = input("Template do corpo (use {name}, {email}): ").strip()
            
            sender.send_from_csv(csv_file, subject_template, body_template)
        
        elif choice == "3":
            create_example_csv()
        
        sender.save_log()
    
    finally:
        sender.disconnect()


if __name__ == "__main__":
    main()
