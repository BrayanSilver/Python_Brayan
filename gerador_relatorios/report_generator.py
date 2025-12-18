"""
Gerador Automático de Relatórios
Gera relatórios em PDF, HTML, Excel e texto a partir de dados
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️  pandas não instalado. Instale para suporte a Excel: pip install pandas openpyxl")


class ReportGenerator:
    def __init__(self, output_dir="reports"):
        """
        Inicializa o gerador de relatórios
        
        Args:
            output_dir: Diretório de saída
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_text_report(self, data, title="Relatório", filename=None):
        """
        Gera relatório em texto
        
        Args:
            data: Dados (dict, list ou string)
            title: Título do relatório
            filename: Nome do arquivo (opcional)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.txt"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"{title}\n")
            f.write("=" * 70 + "\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 70 + "\n\n")
            
            if isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"{key}:\n")
                    if isinstance(value, (list, dict)):
                        f.write(json.dumps(value, indent=2, ensure_ascii=False))
                    else:
                        f.write(f"  {value}\n")
                    f.write("\n")
            elif isinstance(data, list):
                for i, item in enumerate(data, 1):
                    f.write(f"{i}. {item}\n")
            else:
                f.write(str(data))
            
            f.write("\n" + "=" * 70 + "\n")
        
        print(f"✅ Relatório texto gerado: {filepath}")
        return filepath
    
    def generate_html_report(self, data, title="Relatório", filename=None, style="default"):
        """
        Gera relatório em HTML
        
        Args:
            data: Dados (dict, list ou string)
            title: Título do relatório
            filename: Nome do arquivo (opcional)
            style: Estilo CSS (default, modern, minimal)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        # Estilos CSS
        styles = {
            'default': """
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #4CAF50; color: white; }
                tr:hover { background-color: #f5f5f5; }
            """,
            'modern': """
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); max-width: 1200px; margin: 0 auto; }
                h1 { color: #667eea; border-bottom: 3px solid #764ba2; padding-bottom: 15px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 15px; text-align: left; border-bottom: 1px solid #e0e0e0; }
                th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                tr:hover { background-color: #f8f9fa; }
            """,
            'minimal': """
                body { font-family: Georgia, serif; margin: 40px; background: white; }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { color: #333; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
                th { font-weight: bold; }
            """
        }
        
        css = styles.get(style, styles['default'])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p><strong>Data:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <hr>
""")
            
            if isinstance(data, dict):
                f.write("<table>\n")
                for key, value in data.items():
                    f.write(f"<tr><th>{key}</th><td>")
                    if isinstance(value, (list, dict)):
                        f.write(f"<pre>{json.dumps(value, indent=2, ensure_ascii=False)}</pre>")
                    else:
                        f.write(str(value))
                    f.write("</td></tr>\n")
                f.write("</table>\n")
            
            elif isinstance(data, list):
                if data and isinstance(data[0], dict):
                    # Lista de dicionários = tabela
                    f.write("<table>\n<thead><tr>")
                    for key in data[0].keys():
                        f.write(f"<th>{key}</th>")
                    f.write("</tr></thead><tbody>\n")
                    
                    for item in data:
                        f.write("<tr>")
                        for value in item.values():
                            f.write(f"<td>{value}</td>")
                        f.write("</tr>\n")
                    f.write("</tbody></table>\n")
                else:
                    # Lista simples
                    f.write("<ul>\n")
                    for item in data:
                        f.write(f"<li>{item}</li>\n")
                    f.write("</ul>\n")
            else:
                f.write(f"<p>{str(data)}</p>\n")
            
            f.write("""
    </div>
</body>
</html>
""")
        
        print(f"✅ Relatório HTML gerado: {filepath}")
        return filepath
    
    def generate_csv_report(self, data, filename=None):
        """
        Gera relatório em CSV
        
        Args:
            data: Lista de dicionários ou lista de listas
            filename: Nome do arquivo (opcional)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        if not data:
            print("❌ Nenhum dado para exportar")
            return None
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if isinstance(data[0], dict):
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(f)
                writer.writerows(data)
        
        print(f"✅ Relatório CSV gerado: {filepath}")
        return filepath
    
    def generate_excel_report(self, data, filename=None, sheet_name="Dados"):
        """
        Gera relatório em Excel
        
        Args:
            data: Lista de dicionários ou DataFrame
            filename: Nome do arquivo (opcional)
            sheet_name: Nome da planilha
        """
        if not PANDAS_AVAILABLE:
            print("❌ pandas não instalado. Instale com: pip install pandas openpyxl")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        try:
            if isinstance(data, list) and data and isinstance(data[0], dict):
                df = pd.DataFrame(data)
            elif isinstance(data, pd.DataFrame):
                df = data
            else:
                print("❌ Formato de dados não suportado para Excel")
                return None
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ Relatório Excel gerado: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro ao gerar Excel: {e}")
            return None
    
    def generate_summary_report(self, data, title="Resumo", filename=None):
        """
        Gera relatório resumido com estatísticas
        
        Args:
            data: Lista de dicionários
            title: Título
            filename: Nome do arquivo (opcional)
        """
        if not data or not isinstance(data, list) or not isinstance(data[0], dict):
            print("❌ Dados inválidos para relatório resumido")
            return None
        
        summary = {
            'total_registros': len(data),
            'colunas': list(data[0].keys()),
            'estatisticas': {}
        }
        
        # Calcula estatísticas para colunas numéricas
        for col in data[0].keys():
            values = [item.get(col) for item in data if item.get(col) is not None]
            if values and isinstance(values[0], (int, float)):
                summary['estatisticas'][col] = {
                    'min': min(values),
                    'max': max(values),
                    'media': sum(values) / len(values),
                    'total': sum(values)
                }
        
        # Gera relatório em múltiplos formatos
        reports = {}
        
        # Texto
        reports['text'] = self.generate_text_report(summary, title, filename.replace('.txt', '_summary.txt') if filename else None)
        
        # HTML
        reports['html'] = self.generate_html_report(summary, title, filename.replace('.html', '_summary.html') if filename else None)
        
        return reports
    
    def generate_from_json(self, json_file, output_format='html'):
        """
        Gera relatório a partir de arquivo JSON
        
        Args:
            json_file: Caminho do arquivo JSON
            output_format: Formato de saída (html, text, csv, excel)
        """
        json_path = Path(json_file)
        if not json_path.exists():
            print(f"❌ Arquivo não encontrado: {json_file}")
            return None
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        title = f"Relatório - {json_path.stem}"
        
        if output_format == 'html':
            return self.generate_html_report(data, title)
        elif output_format == 'text':
            return self.generate_text_report(data, title)
        elif output_format == 'csv':
            return self.generate_csv_report(data if isinstance(data, list) else [data])
        elif output_format == 'excel':
            return self.generate_excel_report(data if isinstance(data, list) else [data])
        else:
            print(f"❌ Formato inválido: {output_format}")
            return None


def create_sample_data():
    """Cria dados de exemplo"""
    return [
        {'nome': 'João Silva', 'idade': 30, 'cargo': 'Desenvolvedor', 'salario': 5000},
        {'nome': 'Maria Santos', 'idade': 28, 'cargo': 'Designer', 'salario': 4500},
        {'nome': 'Pedro Costa', 'idade': 35, 'cargo': 'Gerente', 'salario': 8000},
        {'nome': 'Ana Oliveira', 'idade': 26, 'cargo': 'Analista', 'salario': 4000},
    ]


def main():
    """Interface interativa"""
    generator = ReportGenerator()
    
    print("📊 Gerador Automático de Relatórios\n")
    
    # Dados de exemplo
    sample_data = create_sample_data()
    
    print("1. Gerar relatório HTML")
    print("2. Gerar relatório texto")
    print("3. Gerar relatório CSV")
    print("4. Gerar relatório Excel")
    print("5. Gerar relatório resumido")
    print("6. Gerar de arquivo JSON")
    print("7. Usar dados de exemplo")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == "1":
        data = sample_data
        generator.generate_html_report(data, "Relatório de Funcionários", style="modern")
    
    elif choice == "2":
        data = sample_data
        generator.generate_text_report(data, "Relatório de Funcionários")
    
    elif choice == "3":
        data = sample_data
        generator.generate_csv_report(data)
    
    elif choice == "4":
        data = sample_data
        generator.generate_excel_report(data, sheet_name="Funcionários")
    
    elif choice == "5":
        data = sample_data
        generator.generate_summary_report(data, "Resumo de Funcionários")
    
    elif choice == "6":
        json_file = input("Caminho do arquivo JSON: ").strip()
        format_choice = input("Formato (html/text/csv/excel): ").strip() or "html"
        generator.generate_from_json(json_file, format_choice)
    
    elif choice == "7":
        print("\n📋 Dados de exemplo:")
        for item in sample_data:
            print(f"  {item}")
        print("\n✅ Use as opções 1-5 para gerar relatórios com esses dados")


if __name__ == "__main__":
    main()
