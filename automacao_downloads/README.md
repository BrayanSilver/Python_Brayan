# 📥 Automação de Downloads

Sistema completo para gerenciar downloads de forma automatizada com organização, validação e histórico.

## 🚀 Funcionalidades

- ✅ Download de arquivos únicos
- ✅ Download múltiplo em paralelo
- ✅ Download de lista de URLs
- ✅ Verificação de hash (MD5)
- ✅ Barra de progresso
- ✅ Organização automática
- ✅ Histórico completo
- ✅ Estatísticas de downloads
- ✅ Detecção automática de nome de arquivo

## 📦 Instalação

```bash
pip install requests
```

## 💻 Uso

### Uso Básico

```python
from download_manager import DownloadManager

# Criar gerenciador
manager = DownloadManager("meus_downloads")

# Baixar arquivo único
manager.download_file("https://example.com/file.pdf")

# Baixar com nome customizado
manager.download_file(
    "https://example.com/file.pdf",
    filename="documento.pdf",
    folder="documentos"
)

# Baixar múltiplos arquivos
urls = [
    "https://example.com/file1.pdf",
    "https://example.com/file2.jpg",
]
manager.download_multiple(urls, max_workers=3)
```

### Executar Interface

```bash
python download_manager.py
```

## 📋 Funcionalidades

### Download Único

```python
manager.download_file(
    url="https://example.com/file.pdf",
    filename="documento.pdf",  # Opcional
    folder="documentos",       # Opcional
    verify_hash="abc123..."    # Opcional (MD5)
)
```

### Download Múltiplo

```python
urls = ["url1", "url2", "url3"]
results = manager.download_multiple(urls, max_workers=3)
```

### Download de Lista

Crie um arquivo `urls.txt`:
```
https://example.com/file1.pdf
https://example.com/file2.jpg
# Comentários são ignorados
https://example.com/file3.zip
```

```python
manager.download_from_list("urls.txt")
```

### Organização

```python
# Organiza downloads por extensão
manager.organize_downloads(organize_by="extension")
```

### Estatísticas

```python
stats = manager.get_statistics()
print(f"Total: {stats['total_downloads']}")
print(f"Tamanho: {stats['total_size_mb']} MB")
```

## 🔒 Verificação de Hash

```python
# Baixa e verifica hash MD5
manager.download_file(
    url="https://example.com/file.zip",
    verify_hash="5d41402abc4b2a76b9719d911017c592"
)
```

## 📊 Histórico

Todos os downloads são registrados em `download_history.json` com:
- Timestamp
- URL
- Nome do arquivo
- Tamanho
- Hash
- Tempo de download
- Status (success/error)

## 🎯 Casos de Uso

- Download de arquivos grandes
- Backup de recursos web
- Download de datasets
- Sincronização de arquivos
- Download de mídia

## ⚙️ Configurações

- **download_dir**: Diretório padrão (padrão: "downloads")
- **max_workers**: Downloads simultâneos (padrão: 3)
- **chunk_size**: Tamanho do chunk (padrão: 8192 bytes)
