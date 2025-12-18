# 🔄 Sistema de Backup Automatizado

Sistema completo de backup automatizado com compressão, versionamento e gerenciamento de backups.

## 🚀 Funcionalidades

- ✅ Backup automático de arquivos e pastas
- ✅ Compressão em formato ZIP
- ✅ Versionamento automático com timestamps
- ✅ Listagem de todos os backups criados
- ✅ Restauração de backups específicos
- ✅ Limpeza automática de backups antigos
- ✅ Histórico completo em JSON

## 📦 Instalação

Não requer dependências externas! Usa apenas bibliotecas padrão do Python.

## 💻 Uso

### Uso Básico

```python
from backup_system import BackupSystem

# Criar instância do sistema de backup
backup = BackupSystem("caminho/para/pasta", "diretorio_backups")

# Criar backup comprimido
backup.create_backup(compress=True)

# Listar backups
backup.list_backups()

# Restaurar backup (índice 1)
backup.restore_backup(1)

# Limpar backups antigos (manter apenas os últimos 5)
backup.cleanup_old_backups(keep_last=5)
```

### Executar Interface Interativa

```bash
python backup_system.py
```

## 📁 Estrutura

```
backup_automatico/
├── backup_system.py    # Código principal
├── README.md           # Documentação
└── backups/            # Diretório de backups (criado automaticamente)
    ├── backup_*.zip    # Backups comprimidos
    └── backup_config.json  # Histórico de backups
```

## 🔧 Recursos

- **Compressão**: Reduz o tamanho dos backups
- **Versionamento**: Cada backup tem timestamp único
- **Histórico**: Todas as informações são salvas em JSON
- **Restauração**: Restaura backups facilmente
- **Limpeza**: Remove backups antigos automaticamente

## 📝 Exemplo de Saída

```
✅ Backup criado com sucesso: backups/backup_documentos_20250115_143022.zip

📋 Lista de Backups:
------------------------------------------------------------
1. 20250115_143022 - 2.45 MB
   backups/backup_documentos_20250115_143022.zip
2. 20250115_120000 - 1.89 MB
   backups/backup_documentos_20250115_120000.zip
```

## 🎯 Casos de Uso

- Backup diário de documentos importantes
- Backup antes de atualizações de sistema
- Backup de configurações de aplicativos
- Backup de projetos de desenvolvimento
