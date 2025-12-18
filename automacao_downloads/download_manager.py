"""
Automação de Downloads
Gerencia downloads de forma automatizada com organização e validação
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote
from datetime import datetime
import json
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class DownloadManager:
    def __init__(self, download_dir="downloads"):
        """
        Inicializa o gerenciador de downloads
        
        Args:
            download_dir: Diretório padrão para downloads
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.download_history = []
        self.history_file = self.download_dir / "download_history.json"
        self.load_history()
    
    def load_history(self):
        """Carrega histórico de downloads"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.download_history = json.load(f)
            except:
                self.download_history = []
    
    def save_history(self):
        """Salva histórico de downloads"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.download_history, f, indent=2, ensure_ascii=False)
    
    def get_filename_from_url(self, url, default_name="download"):
        """Extrai nome do arquivo da URL"""
        parsed = urlparse(url)
        filename = unquote(os.path.basename(parsed.path))
        
        if not filename or filename == '/':
            filename = default_name
        
        # Adiciona extensão se não tiver
        if '.' not in filename:
            # Tenta obter do Content-Type
            try:
                head = requests.head(url, timeout=5)
                content_type = head.headers.get('Content-Type', '')
                if 'image' in content_type:
                    filename += '.jpg'
                elif 'pdf' in content_type:
                    filename += '.pdf'
                elif 'text' in content_type:
                    filename += '.txt'
            except:
                pass
        
        return filename
    
    def calculate_hash(self, filepath, algorithm='md5'):
        """Calcula hash do arquivo"""
        hash_obj = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    def download_file(self, url, filename=None, folder=None, verify_hash=None):
        """
        Baixa um arquivo
        
        Args:
            url: URL do arquivo
            filename: Nome do arquivo (opcional)
            folder: Pasta de destino (opcional)
            verify_hash: Hash para verificação (opcional)
        """
        if not filename:
            filename = self.get_filename_from_url(url)
        
        # Determina pasta de destino
        if folder:
            dest_folder = self.download_dir / folder
        else:
            dest_folder = self.download_dir
        
        dest_folder.mkdir(exist_ok=True)
        filepath = dest_folder / filename
        
        # Se arquivo já existe, adiciona número
        counter = 1
        original_filepath = filepath
        while filepath.exists():
            stem = original_filepath.stem
            suffix = original_filepath.suffix
            filepath = dest_folder / f"{stem}_{counter}{suffix}"
            counter += 1
        
        print(f"📥 Baixando: {filename}")
        print(f"   De: {url}")
        print(f"   Para: {filepath}")
        
        try:
            start_time = time.time()
            
            # Faz o download
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Mostra progresso
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r   Progresso: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
            
            elapsed = time.time() - start_time
            file_size = filepath.stat().st_size
            
            # Calcula hash
            file_hash = self.calculate_hash(filepath)
            
            # Verifica hash se fornecido
            if verify_hash and file_hash != verify_hash:
                print(f"\n⚠️  Hash não confere! Esperado: {verify_hash}, Obtido: {file_hash}")
                filepath.unlink()
                return None
            
            # Salva no histórico
            download_info = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'filename': filename,
                'filepath': str(filepath),
                'size': file_size,
                'hash': file_hash,
                'elapsed_time': round(elapsed, 2),
                'status': 'success'
            }
            self.download_history.append(download_info)
            self.save_history()
            
            print(f"\n✅ Download concluído!")
            print(f"   Tamanho: {file_size / (1024*1024):.2f} MB")
            print(f"   Tempo: {elapsed:.2f}s")
            print(f"   Hash: {file_hash}")
            
            return filepath
            
        except Exception as e:
            print(f"\n❌ Erro no download: {e}")
            
            download_info = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'filename': filename,
                'status': 'error',
                'error': str(e)
            }
            self.download_history.append(download_info)
            self.save_history()
            
            return None
    
    def download_multiple(self, urls, max_workers=3):
        """Baixa múltiplos arquivos em paralelo"""
        print(f"📥 Baixando {len(urls)} arquivos (máx {max_workers} simultâneos)...\n")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.download_file, url): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append((url, result))
                except Exception as e:
                    print(f"❌ Erro ao baixar {url}: {e}")
                    results.append((url, None))
        
        successful = sum(1 for _, result in results if result)
        print(f"\n✅ Concluído: {successful}/{len(urls)} downloads bem-sucedidos")
        
        return results
    
    def download_from_list(self, list_file):
        """Baixa arquivos de uma lista (um URL por linha)"""
        filepath = Path(list_file)
        if not filepath.exists():
            print(f"❌ Arquivo não encontrado: {list_file}")
            return []
        
        urls = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url and not url.startswith('#'):
                    urls.append(url)
        
        return self.download_multiple(urls)
    
    def organize_downloads(self, organize_by="extension"):
        """Organiza downloads por extensão ou tipo"""
        from pathlib import Path
        
        # Importa organizador (assumindo que está no mesmo nível)
        # Por simplicidade, implementa aqui
        files_by_ext = {}
        
        for filepath in self.download_dir.iterdir():
            if filepath.is_file() and filepath.name != "download_history.json":
                ext = filepath.suffix.lower() or 'sem_extensao'
                if ext not in files_by_ext:
                    files_by_ext[ext] = []
                files_by_ext[ext].append(filepath)
        
        for ext, files in files_by_ext.items():
            folder_name = ext[1:].upper() if ext.startswith('.') else ext.upper()
            folder = self.download_dir / folder_name
            folder.mkdir(exist_ok=True)
            
            for filepath in files:
                new_path = folder / filepath.name
                if not new_path.exists():
                    filepath.rename(new_path)
                    print(f"✅ Movido: {filepath.name} → {folder_name}/")
    
    def get_statistics(self):
        """Retorna estatísticas dos downloads"""
        if not self.download_history:
            return None
        
        successful = [d for d in self.download_history if d.get('status') == 'success']
        failed = [d for d in self.download_history if d.get('status') == 'error']
        
        total_size = sum(d.get('size', 0) for d in successful)
        total_time = sum(d.get('elapsed_time', 0) for d in successful)
        
        return {
            'total_downloads': len(self.download_history),
            'successful': len(successful),
            'failed': len(failed),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'total_time_seconds': round(total_time, 2),
            'average_speed_mbps': round(total_size / (1024 * 1024) / total_time, 2) if total_time > 0 else 0
        }
    
    def list_downloads(self, limit=20):
        """Lista downloads recentes"""
        recent = self.download_history[-limit:]
        recent.reverse()  # Mais recentes primeiro
        
        print(f"\n📋 Últimos {len(recent)} downloads:")
        print("-" * 70)
        
        for download in recent:
            status_icon = "✅" if download.get('status') == 'success' else "❌"
            timestamp = download.get('timestamp', 'N/A')
            filename = download.get('filename', 'N/A')
            size = download.get('size', 0)
            
            print(f"{status_icon} [{timestamp}] {filename}")
            if size > 0:
                print(f"   Tamanho: {size / (1024*1024):.2f} MB")


def main():
    """Interface interativa"""
    manager = DownloadManager()
    
    print("📥 Gerenciador de Downloads\n")
    
    while True:
        print("\n" + "="*50)
        print("1. Baixar arquivo único")
        print("2. Baixar múltiplos arquivos")
        print("3. Baixar de lista (arquivo .txt)")
        print("4. Organizar downloads")
        print("5. Ver histórico")
        print("6. Ver estatísticas")
        print("0. Sair")
        print("="*50)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            url = input("URL do arquivo: ").strip()
            filename = input("Nome do arquivo (Enter para automático): ").strip() or None
            folder = input("Pasta (Enter para padrão): ").strip() or None
            
            manager.download_file(url, filename, folder)
        
        elif choice == "2":
            print("Digite URLs (uma por linha, linha vazia para terminar):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                max_workers = input("Máximo de downloads simultâneos (padrão: 3): ").strip()
                max_workers = int(max_workers) if max_workers.isdigit() else 3
                manager.download_multiple(urls, max_workers)
        
        elif choice == "3":
            list_file = input("Caminho do arquivo de lista: ").strip()
            manager.download_from_list(list_file)
        
        elif choice == "4":
            confirm = input("⚠️  Organizar downloads? (s/n): ").strip().lower()
            if confirm == 's':
                manager.organize_downloads()
        
        elif choice == "5":
            limit = input("Quantos mostrar (padrão: 20): ").strip()
            limit = int(limit) if limit.isdigit() else 20
            manager.list_downloads(limit)
        
        elif choice == "6":
            stats = manager.get_statistics()
            if stats:
                print("\n📊 Estatísticas:")
                print(f"  Total de downloads: {stats['total_downloads']}")
                print(f"  Bem-sucedidos: {stats['successful']}")
                print(f"  Falhas: {stats['failed']}")
                print(f"  Tamanho total: {stats['total_size_mb']} MB")
                print(f"  Tempo total: {stats['total_time_seconds']}s")
                print(f"  Velocidade média: {stats['average_speed_mbps']} MB/s")
            else:
                print("Nenhum download registrado.")
        
        elif choice == "0":
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    main()
