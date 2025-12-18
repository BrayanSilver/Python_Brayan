"""
Sistema de Backup Automatizado
Automatiza o backup de arquivos e pastas com compressão e versionamento
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
import json


class BackupSystem:
    def __init__(self, source_path, backup_dir="backups"):
        """
        Inicializa o sistema de backup
        
        Args:
            source_path: Caminho da pasta/arquivo a fazer backup
            backup_dir: Diretório onde os backups serão salvos
        """
        self.source_path = Path(source_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.config_file = self.backup_dir / "backup_config.json"
        
    def create_backup(self, compress=True):
        """
        Cria um backup do arquivo/pasta especificado
        
        Args:
            compress: Se True, comprime o backup em ZIP
        """
        if not self.source_path.exists():
            raise FileNotFoundError(f"Arquivo/pasta não encontrado: {self.source_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{self.source_path.name}_{timestamp}"
        
        if compress:
            backup_path = self.backup_dir / f"{backup_name}.zip"
            self._create_zip_backup(backup_path)
        else:
            backup_path = self.backup_dir / backup_name
            if self.source_path.is_file():
                shutil.copy2(self.source_path, backup_path)
            else:
                shutil.copytree(self.source_path, backup_path)
        
        self._save_backup_info(backup_path, timestamp)
        print(f"✅ Backup criado com sucesso: {backup_path}")
        return backup_path
    
    def _create_zip_backup(self, zip_path):
        """Cria um backup comprimido em ZIP"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if self.source_path.is_file():
                zipf.write(self.source_path, self.source_path.name)
            else:
                for root, dirs, files in os.walk(self.source_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(self.source_path.parent)
                        zipf.write(file_path, arcname)
    
    def _save_backup_info(self, backup_path, timestamp):
        """Salva informações do backup em JSON"""
        backup_info = {
            "timestamp": timestamp,
            "backup_path": str(backup_path),
            "source_path": str(self.source_path),
            "size": backup_path.stat().st_size if backup_path.exists() else 0
        }
        
        configs = []
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                configs = json.load(f)
        
        configs.append(backup_info)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)
    
    def list_backups(self):
        """Lista todos os backups criados"""
        if not self.config_file.exists():
            print("Nenhum backup encontrado.")
            return []
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        print("\n📋 Lista de Backups:")
        print("-" * 60)
        for i, backup in enumerate(configs, 1):
            size_mb = backup['size'] / (1024 * 1024)
            print(f"{i}. {backup['timestamp']} - {size_mb:.2f} MB")
            print(f"   {backup['backup_path']}")
        
        return configs
    
    def restore_backup(self, backup_index):
        """Restaura um backup específico"""
        configs = self.list_backups()
        if not configs or backup_index < 1 or backup_index > len(configs):
            print("❌ Índice de backup inválido.")
            return
        
        backup_info = configs[backup_index - 1]
        backup_path = Path(backup_info['backup_path'])
        
        if not backup_path.exists():
            print(f"❌ Arquivo de backup não encontrado: {backup_path}")
            return
        
        restore_dir = self.backup_dir / "restored"
        restore_dir.mkdir(exist_ok=True)
        
        if backup_path.suffix == '.zip':
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(restore_dir)
        else:
            shutil.copytree(backup_path, restore_dir / backup_path.name)
        
        print(f"✅ Backup restaurado em: {restore_dir}")
    
    def cleanup_old_backups(self, keep_last=5):
        """Remove backups antigos, mantendo apenas os últimos N"""
        configs = self.list_backups()
        if len(configs) <= keep_last:
            print("Nenhum backup antigo para remover.")
            return
        
        configs_to_remove = configs[:-keep_last]
        for backup_info in configs_to_remove:
            backup_path = Path(backup_info['backup_path'])
            if backup_path.exists():
                backup_path.unlink()
                print(f"🗑️  Removido: {backup_path.name}")
        
        # Atualiza o arquivo de configuração
        remaining_backups = configs[-keep_last:]
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(remaining_backups, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Limpeza concluída. Mantidos os últimos {keep_last} backups.")


def main():
    """Exemplo de uso"""
    print("🔄 Sistema de Backup Automatizado\n")
    
    # Exemplo: fazer backup de uma pasta
    source = input("Digite o caminho da pasta/arquivo para backup (ou Enter para exemplo): ").strip()
    if not source:
        source = "exemplo"
        Path("exemplo").mkdir(exist_ok=True)
        (Path("exemplo") / "arquivo_teste.txt").write_text("Conteúdo de teste")
    
    backup_system = BackupSystem(source)
    
    while True:
        print("\n" + "="*50)
        print("1. Criar backup")
        print("2. Listar backups")
        print("3. Restaurar backup")
        print("4. Limpar backups antigos")
        print("5. Sair")
        print("="*50)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            backup_system.create_backup(compress=True)
        elif choice == "2":
            backup_system.list_backups()
        elif choice == "3":
            backup_system.list_backups()
            idx = input("\nDigite o número do backup para restaurar: ").strip()
            try:
                backup_system.restore_backup(int(idx))
            except ValueError:
                print("❌ Número inválido.")
        elif choice == "4":
            keep = input("Quantos backups manter? (padrão: 5): ").strip()
            keep = int(keep) if keep.isdigit() else 5
            backup_system.cleanup_old_backups(keep)
        elif choice == "5":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    main()
