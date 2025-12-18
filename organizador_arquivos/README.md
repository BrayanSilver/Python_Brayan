# 📁 Organizador Automático de Arquivos

Sistema inteligente para organizar arquivos automaticamente por extensão, tipo, data ou tamanho.

## 🚀 Funcionalidades

- ✅ Organização por extensão (.jpg, .pdf, etc)
- ✅ Organização por tipo (Imagens, Vídeos, Documentos)
- ✅ Organização por data de modificação
- ✅ Organização por tamanho
- ✅ Logging completo de operações
- ✅ Estatísticas de arquivos
- ✅ Categorização inteligente

## 📦 Instalação

Não requer dependências externas! Usa apenas bibliotecas padrão do Python.

## 💻 Uso

### Uso Básico

```python
from organizer import FileOrganizer

# Organizar por extensão
organizer = FileOrganizer("C:/Downloads", organize_by="extension")
organizer.organize()

# Organizar por tipo
organizer = FileOrganizer("C:/Downloads", organize_by="type")
organizer.organize()

# Organizar por data
organizer = FileOrganizer("C:/Downloads", organize_by="date")
organizer.organize()

# Organizar por tamanho
organizer = FileOrganizer("C:/Downloads", organize_by="size")
organizer.organize()
```

### Executar Interface

```bash
python organizer.py
```

## 📋 Métodos de Organização

### 1. Por Extensão
Cria pastas como: `Arquivos_JPG`, `Arquivos_PDF`, etc.

### 2. Por Tipo
Cria pastas como: `Images`, `Videos`, `Documents`, `Code`, etc.

### 3. Por Data
Cria pastas como: `2025-01`, `2025-02`, etc. (baseado na data de modificação)

### 4. Por Tamanho
Cria pastas como:
- `Pequenos (< 1MB)`
- `Medios (1-10MB)`
- `Grandes (10-100MB)`
- `Muito Grandes (> 100MB)`

## 🎯 Categorias de Tipos

- **Images**: .jpg, .png, .gif, .svg, etc.
- **Videos**: .mp4, .avi, .mkv, etc.
- **Audio**: .mp3, .wav, .flac, etc.
- **Documents**: .pdf, .doc, .txt, etc.
- **Archives**: .zip, .rar, .7z, etc.
- **Code**: .py, .js, .html, .css, etc.
- **Spreadsheets**: .csv, .xls, .xlsx
- **Presentations**: .ppt, .pptx
- **Others**: Outros tipos

## 📝 Logging

Todas as operações são registradas em `organization_log.json` com:
- Arquivo movido
- Origem e destino
- Método usado

## ⚠️ Aviso

Este script **move** arquivos, não copia. Certifique-se de ter backup antes de usar em pastas importantes!

## 🎯 Casos de Uso

- Organizar pasta de Downloads
- Limpar área de trabalho
- Organizar fotos e vídeos
- Organizar documentos de projetos
- Preparar arquivos para backup
