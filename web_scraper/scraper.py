"""
Web Scraper Automatizado
Extrai dados de websites de forma automatizada
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
from pathlib import Path
import time
import re


class WebScraper:
    def __init__(self, base_url, delay=1):
        """
        Inicializa o web scraper
        
        Args:
            base_url: URL base do site
            delay: Delay entre requisições (segundos)
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.scraped_data = []
    
    def fetch_page(self, url):
        """Busca uma página e retorna o conteúdo"""
        try:
            time.sleep(self.delay)  # Respeita o delay
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Erro ao buscar {url}: {e}")
            return None
    
    def parse_html(self, html_content):
        """Parseia o HTML usando BeautifulSoup"""
        if not html_content:
            return None
        return BeautifulSoup(html_content, 'html.parser')
    
    def scrape_links(self, url, selector='a'):
        """Extrai todos os links de uma página"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        if not soup:
            return []
        
        links = []
        for link in soup.select(selector):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            if href:
                # Converte URL relativa para absoluta
                if href.startswith('/'):
                    href = self.base_url + href
                elif not href.startswith('http'):
                    href = f"{self.base_url}/{href}"
                
                links.append({
                    'text': text,
                    'url': href
                })
        
        return links
    
    def scrape_text(self, url, selectors):
        """
        Extrai texto de elementos específicos
        
        Args:
            url: URL da página
            selectors: Dict com nome:seletor_css
        """
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        if not soup:
            return {}
        
        data = {}
        for name, selector in selectors.items():
            elements = soup.select(selector)
            if elements:
                data[name] = [elem.get_text(strip=True) for elem in elements]
            else:
                data[name] = []
        
        return data
    
    def scrape_table(self, url, table_selector='table'):
        """Extrai dados de uma tabela HTML"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        if not soup:
            return []
        
        tables = soup.select(table_selector)
        if not tables:
            return []
        
        data = []
        for table in tables:
            headers = []
            header_row = table.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
            rows = table.find_all('tr')[1:]  # Pula o cabeçalho
            for row in rows:
                cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                if cells:
                    if headers:
                        data.append(dict(zip(headers, cells)))
                    else:
                        data.append(cells)
        
        return data
    
    def scrape_images(self, url, img_selector='img'):
        """Extrai URLs de imagens"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        if not soup:
            return []
        
        images = []
        for img in soup.select(img_selector):
            src = img.get('src') or img.get('data-src')
            alt = img.get('alt', '')
            if src:
                if src.startswith('/'):
                    src = self.base_url + src
                elif not src.startswith('http'):
                    src = f"{self.base_url}/{src}"
                
                images.append({
                    'url': src,
                    'alt': alt
                })
        
        return images
    
    def scrape_emails(self, url):
        """Extrai emails de uma página"""
        html = self.fetch_page(url)
        if not html:
            return []
        
        # Regex para encontrar emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        return list(set(emails))  # Remove duplicatas
    
    def scrape_news(self, url, title_selector, content_selector, link_selector=None):
        """Extrai notícias de um site"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        if not soup:
            return []
        
        news = []
        titles = soup.select(title_selector)
        contents = soup.select(content_selector)
        links = soup.select(link_selector) if link_selector else []
        
        max_items = min(len(titles), len(contents))
        for i in range(max_items):
            news_item = {
                'title': titles[i].get_text(strip=True),
                'content': contents[i].get_text(strip=True),
                'url': links[i].get('href') if i < len(links) else None
            }
            news.append(news_item)
        
        return news
    
    def save_to_json(self, data, filename=None):
        """Salva dados em JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.json"
        
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dados salvos em: {filepath}")
        return filepath
    
    def save_to_csv(self, data, filename=None):
        """Salva dados em CSV"""
        if not data:
            print("❌ Nenhum dado para salvar.")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.csv"
        
        filepath = Path(filename)
        
        # Se for lista de dicionários
        if isinstance(data, list) and data and isinstance(data[0], dict):
            fieldnames = data[0].keys()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        else:
            # Se for lista simples
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row if isinstance(row, list) else [row])
        
        print(f"✅ Dados salvos em: {filepath}")
        return filepath


def example_scrape_quotes():
    """Exemplo: Scraping de citações do site quotes.toscrape.com"""
    print("📖 Scraping de Citações\n")
    
    scraper = WebScraper("http://quotes.toscrape.com")
    
    quotes = []
    for page in range(1, 3):  # Primeiras 2 páginas
        url = f"http://quotes.toscrape.com/page/{page}/"
        print(f"Buscando: {url}")
        
        html = scraper.fetch_page(url)
        soup = scraper.parse_html(html)
        
        if soup:
            quote_elements = soup.select('.quote')
            for quote_elem in quote_elements:
                text = quote_elem.select_one('.text').get_text()
                author = quote_elem.select_one('.author').get_text()
                tags = [tag.get_text() for tag in quote_elem.select('.tag')]
                
                quotes.append({
                    'quote': text,
                    'author': author,
                    'tags': ', '.join(tags)
                })
    
    print(f"\n✅ {len(quotes)} citações encontradas!")
    scraper.save_to_json(quotes, "quotes.json")
    scraper.save_to_csv(quotes, "quotes.csv")
    
    return quotes


def main():
    """Interface interativa"""
    print("🕷️  Web Scraper Automatizado\n")
    
    print("1. Scraping de links")
    print("2. Scraping de tabela")
    print("3. Scraping de imagens")
    print("4. Scraping de emails")
    print("5. Exemplo: Citações (quotes.toscrape.com)")
    print("6. Scraping customizado")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == "1":
        url = input("Digite a URL: ").strip()
        scraper = WebScraper(url)
        links = scraper.scrape_links(url)
        print(f"\n✅ {len(links)} links encontrados:")
        for link in links[:10]:  # Mostra os primeiros 10
            print(f"  - {link['text']}: {link['url']}")
        scraper.save_to_json(links)
    
    elif choice == "2":
        url = input("Digite a URL: ").strip()
        scraper = WebScraper(url)
        table_data = scraper.scrape_table(url)
        print(f"\n✅ {len(table_data)} linhas encontradas")
        scraper.save_to_csv(table_data)
    
    elif choice == "3":
        url = input("Digite a URL: ").strip()
        scraper = WebScraper(url)
        images = scraper.scrape_images(url)
        print(f"\n✅ {len(images)} imagens encontradas")
        scraper.save_to_json(images)
    
    elif choice == "4":
        url = input("Digite a URL: ").strip()
        scraper = WebScraper(url)
        emails = scraper.scrape_emails(url)
        print(f"\n✅ {len(emails)} emails encontrados:")
        for email in emails:
            print(f"  - {email}")
    
    elif choice == "5":
        example_scrape_quotes()
    
    elif choice == "6":
        url = input("Digite a URL: ").strip()
        selector = input("Digite o seletor CSS: ").strip()
        scraper = WebScraper(url)
        html = scraper.fetch_page(url)
        soup = scraper.parse_html(html)
        if soup:
            elements = soup.select(selector)
            data = [elem.get_text(strip=True) for elem in elements]
            print(f"\n✅ {len(data)} elementos encontrados")
            scraper.save_to_json(data)


if __name__ == "__main__":
    main()
