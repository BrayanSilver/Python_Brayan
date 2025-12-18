"""
Organizador Automático de Arquivos
Organiza arquivos por extensão, data ou tipo automaticamente
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json


class FileOrganizer:
    def __init__(self, source_dir, organize_by="extension"):
        """
        Inicializa o organizador de arquivos
        
        Args:
            source_dir: Diretório a organizar
            organize_by: 'extension', 'date', 'type', 'size'
        """
        self.source_dir = Path(source_dir)
        self.organize_by = organize_by
        self.organization_log = []
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {source_dir}")
    
    def get_file_category(self, filepath):
        """Determina a categoria do arquivo"""
        ext = filepath.suffix.lower()
        
        categories = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
            'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb'],
            'spreadsheets': ['.csv', '.xls', '.xlsx', '.ods'],
            'presentations': ['.ppt', '.pptx', '.odp'],
        }
        
        for category, extensions in categories.items():
            if ext in extensions:
                return category
        
        return 'others'
    
    def organize_by_extension(self):
        """Organiza arquivos por extensão"""
        files_by_ext = defaultdict(list)
        
        for filepath in self.source_dir.iterdir():
            if filepath.is_file():
                ext = filepath.suffix.lower() or 'sem_extensao'
                files_by_ext[ext].append(filepath)
        
        for ext, files in files_by_ext.items():
            folder_name = ext[1:] if ext.startswith('.') else ext
            folder_name = f"Arquivos_{folder_name.upper()}"
            target_folder = self.source_dir / folder_name
            target_folder.mkdir(exist_ok=True)
            
            for filepath in files:
                target_path = target_folder / filepath.name
                if not target_path.exists():
                    shutil.move(str(filepath), str(target_path))
                    self.organization_log.append({
                        'file': str(filepath.name),
                        'from': str(filepath.parent),
                        'to': str(target_folder),
                        'method': 'extension'
                    })
                    print(f"✅ Movido: {filepath.name} → {folder_name}/")
    
    def organize_by_type(self):
        """Organiza arquivos por tipo (imagens, vídeos, etc)"""
        files_by_type = defaultdict(list)
        
        for filepath in self.source_dir.iterdir():
            if filepath.is_file():
                category = self.get_file_category(filepath)
                files_by_type[category].append(filepath)
        
        for category, files in files_by_type.items():
            folder_name = category.capitalize()
            target_folder = self.source_dir / folder_name
            target_folder.mkdir(exist_ok=True)
            
            for filepath in files:
                target_path = target_folder / filepath.name
                if not target_path.exists():
                    shutil.move(str(filepath), str(target_path))
                    self.organization_log.append({
                        'file': str(filepath.name),
                        'from': str(filepath.parent),
                        'to': str(target_folder),
                        'method': 'type'
                    })
                    print(f"✅ Movido: {filepath.name} → {folder_name}/")
    
    def organize_by_date(self):
        """Organiza arquivos por data de modificação"""
        files_by_date = defaultdict(list)
        
        for filepath in self.source_dir.iterdir():
            if filepath.is_file():
                mod_time = datetime.fromtimestamp(filepath.stat().st_mtime)
                date_folder = mod_time.strftime("%Y-%m")
                files_by_date[date_folder].append(filepath)
        
        for date_folder, files in files_by_date.items():
            target_folder = self.source_dir / date_folder
            target_folder.mkdir(exist_ok=True)
            
            for filepath in files:
                target_path = target_folder / filepath.name
                if not target_path.exists():
                    shutil.move(str(filepath), str(target_path))
                    self.organization_log.append({
                        'file': str(filepath.name),
                        'from': str(filepath.parent),
                        'to': str(target_folder),
                        'method': 'date'
                    })
                    print(f"✅ Movido: {filepath.name} → {date_folder}/")
    
    def organize_by_size(self, size_ranges=None):
        """Organiza arquivos por tamanho"""
        if not size_ranges:
            size_ranges = {
                'Pequenos (< 1MB)': (0, 1024 * 1024),
                'Medios (1-10MB)': (1024 * 1024, 10 * 1024 * 1024),
                'Grandes (10-100MB)': (10 * 1024 * 1024, 100 * 1024 * 1024),
                'Muito Grandes (> 100MB)': (100 * 1024 * 1024, float('inf'))
            }
        
        files_by_size = defaultdict(list)
        
        for filepath in self.source_dir.iterdir():
            if filepath.is_file():
                size = filepath.stat().st_size
                for folder_name, (min_size, max_size) in size_ranges.items():
                    if min_size <= size < max_size:
                        files_by_size[folder_name].append(filepath)
                        break
        
        for folder_name, files in files_by_size.items():
            target_folder = self.source_dir / folder_name
            target_folder.mkdir(exist_ok=True)
            
            for filepath in files:
                target_path = target_folder / filepath.name
                if not target_path.exists():
                    shutil.move(str(filepath), str(target_path))
                    self.organization_log.append({
                        'file': str(filepath.name),
                        'from': str(filepath.parent),
                        'to': str(target_folder),
                        'method': 'size'
                    })
                    print(f"✅ Movido: {filepath.name} → {folder_name}/")
    
    def organize(self):
        """Executa a organização baseada no método escolhido"""
        print(f"🔄 Organizando arquivos em: {self.source_dir}")
        print(f"📋 Método: {self.organize_by}\n")
        
        if self.organize_by == "extension":
            self.organize_by_extension()
        elif self.organize_by == "type":
            self.organize_by_type()
        elif self.organize_by == "date":
            self.organize_by_date()
        elif self.organize_by == "size":
            self.organize_by_size()
        else:
            raise ValueError(f"Método inválido: {self.organize_by}")
        
        print(f"\n✅ Organização concluída! {len(self.organization_log)} arquivos organizados.")
        self.save_log()
    
    def save_log(self, filename="organization_log.json"):
        """Salva o log de organização"""
        log_file = self.source_dir / filename
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.organization_log, f, indent=2, ensure_ascii=False)
        print(f"📝 Log salvo em: {log_file}")
    
    def get_statistics(self):
        """Retorna estatísticas dos arquivos"""
        stats = {
            'total_files': 0,
            'total_size': 0,
            'by_extension': defaultdict(int),
            'by_type': defaultdict(int)
        }
        
        for filepath in self.source_dir.rglob('*'):
            if filepath.is_file():
                stats['total_files'] += 1
                stats['total_size'] += filepath.stat().st_size
                stats['by_extension'][filepath.suffix.lower() or 'sem_extensao'] += 1
                stats['by_type'][self.get_file_category(filepath)] += 1
        
        stats['total_size_mb'] = round(stats['total_size'] / (1024 * 1024), 2)
        
        return stats


def main():
    """Interface interativa"""
    print("📁 Organizador Automático de Arquivos\n")
    
    source_dir = input("Digite o caminho do diretório a organizar: ").strip()
    if not source_dir:
        print("❌ Caminho inválido.")
        return
    
    print("\nMétodos de organização:")
    print("1. Por extensão (.jpg, .pdf, etc)")
    print("2. Por tipo (Imagens, Vídeos, Documentos, etc)")
    print("3. Por data (YYYY-MM)")
    print("4. Por tamanho")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    methods = {
        '1': 'extension',
        '2': 'type',
        '3': 'date',
        '4': 'size'
    }
    
    method = methods.get(choice, 'extension')
    
    organizer = FileOrganizer(source_dir, organize_by=method)
    
    # Mostra estatísticas antes
    print("\n📊 Estatísticas antes da organização:")
    stats = organizer.get_statistics()
    print(f"  Total de arquivos: {stats['total_files']}")
    print(f"  Tamanho total: {stats['total_size_mb']} MB")
    
    confirm = input("\n⚠️  Continuar? (s/n): ").strip().lower()
    if confirm != 's':
        print("❌ Operação cancelada.")
        return
    
    # Organiza
    organizer.organize()
    
    # Mostra estatísticas depois
    print("\n📊 Organização concluída!")


if __name__ == "__main__":
    main()
