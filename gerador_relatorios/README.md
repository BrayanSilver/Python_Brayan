# 📊 Gerador Automático de Relatórios

Sistema completo para gerar relatórios em múltiplos formatos: HTML, texto, CSV e Excel.

## 🚀 Funcionalidades

- ✅ Geração de relatórios em HTML (com estilos)
- ✅ Geração de relatórios em texto
- ✅ Exportação para CSV
- ✅ Exportação para Excel
- ✅ Relatórios resumidos com estatísticas
- ✅ Geração a partir de arquivos JSON
- ✅ Múltiplos estilos CSS para HTML
- ✅ Suporte a dados complexos

## 📦 Instalação

```bash
# Básico (HTML, texto, CSV)
# Não requer dependências!

# Para Excel
pip install pandas openpyxl
```

## 💻 Uso

### Uso Básico

```python
from report_generator import ReportGenerator

# Criar gerador
generator = ReportGenerator("meus_relatorios")

# Dados
data = [
    {'nome': 'João', 'idade': 30, 'salario': 5000},
    {'nome': 'Maria', 'idade': 28, 'salario': 4500},
]

# Gerar HTML
generator.generate_html_report(data, "Relatório de Funcionários", style="modern")

# Gerar texto
generator.generate_text_report(data, "Relatório de Funcionários")

# Gerar CSV
generator.generate_csv_report(data)

# Gerar Excel
generator.generate_excel_report(data, sheet_name="Funcionários")
```

### Executar Interface

```bash
python report_generator.py
```

## 📋 Formatos de Saída

### HTML

```python
generator.generate_html_report(
    data,
    title="Meu Relatório",
    style="modern"  # default, modern, minimal
)
```

### Texto

```python
generator.generate_text_report(
    data,
    title="Meu Relatório"
)
```

### CSV

```python
generator.generate_csv_report(data)
```

### Excel

```python
generator.generate_excel_report(
    data,
    sheet_name="Dados"
)
```

## 📊 Relatório Resumido

```python
# Gera relatório com estatísticas
generator.generate_summary_report(
    data,
    title="Resumo"
)
```

Inclui:
- Total de registros
- Estatísticas de colunas numéricas (min, max, média, total)
- Lista de colunas

## 🎨 Estilos HTML

- **default**: Estilo padrão simples
- **modern**: Estilo moderno com gradientes
- **minimal**: Estilo minimalista

## 📁 Geração de Arquivo JSON

```python
# Gera relatório a partir de arquivo JSON
generator.generate_from_json(
    "dados.json",
    output_format="html"  # html, text, csv, excel
)
```

## 📝 Estrutura de Dados

### Lista de Dicionários (Recomendado)

```python
data = [
    {'coluna1': 'valor1', 'coluna2': 'valor2'},
    {'coluna1': 'valor3', 'coluna2': 'valor4'},
]
```

### Dicionário Simples

```python
data = {
    'chave1': 'valor1',
    'chave2': 'valor2',
}
```

### Lista Simples

```python
data = ['item1', 'item2', 'item3']
```

## 🎯 Casos de Uso

- Relatórios de vendas
- Relatórios de funcionários
- Análise de dados
- Exportação de resultados
- Documentação de processos
- Relatórios financeiros

## 📊 Estatísticas Automáticas

O relatório resumido calcula automaticamente:
- Mínimo
- Máximo
- Média
- Total

Para todas as colunas numéricas.
