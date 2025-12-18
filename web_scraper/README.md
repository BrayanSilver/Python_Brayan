# 🕷️ Web Scraper Automatizado

Sistema completo de web scraping para extrair dados de websites de forma automatizada.

## 🚀 Funcionalidades

- ✅ Extração de links
- ✅ Extração de texto de elementos específicos
- ✅ Extração de tabelas HTML
- ✅ Extração de imagens
- ✅ Extração de emails
- ✅ Scraping de notícias
- ✅ Exportação para JSON e CSV
- ✅ Delay configurável entre requisições
- ✅ Headers personalizados

## 📦 Instalação

```bash
pip install requests beautifulsoup4
```

## 💻 Uso

### Uso Básico

```python
from scraper import WebScraper

# Criar scraper
scraper = WebScraper("https://example.com", delay=1)

# Extrair links
links = scraper.scrape_links("https://example.com")

# Extrair tabela
table_data = scraper.scrape_table("https://example.com/table")

# Extrair imagens
images = scraper.scrape_images("https://example.com")

# Extrair emails
emails = scraper.scrape_emails("https://example.com")

# Salvar dados
scraper.save_to_json(links, "links.json")
scraper.save_to_csv(table_data, "data.csv")
```

### Executar Interface

```bash
python scraper.py
```

## 📝 Exemplo: Scraping de Citações

```python
from scraper import example_scrape_quotes

# Scraping de quotes.toscrape.com
quotes = example_scrape_quotes()
```

## ⚠️ Considerações Éticas

- Sempre verifique os termos de uso do site
- Respeite o robots.txt
- Use delays apropriados entre requisições
- Não sobrecarregue servidores
- Use apenas para fins educacionais e legais

## 🎯 Casos de Uso

- Coleta de dados de pesquisa
- Monitoramento de preços
- Análise de conteúdo
- Extração de informações públicas
- Backup de conteúdo web
