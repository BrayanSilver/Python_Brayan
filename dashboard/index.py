import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.gridspec as gridspec
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Configurações de estilo
# Usando seaborn para estilo moderno
try:
    import seaborn as sns
    sns.set_style("whitegrid")
    sns.set_palette("husl")
except ImportError:
    # Se seaborn não estiver disponível, usa estilo padrão
    plt.style.use('default')

plt.rcParams.update({
    'font.family': 'Arial',
    'figure.titlesize': 14,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'grid.color': '#dddddd',
    'grid.linewidth': 0.5,
})

class MarketData:
    def __init__(self):
        # Dados específicos do setor de TI (baseados em fontes confiáveis)
        self.profissoes_alta = {
            'Profissão': ['Especialista IA/ML', 'Engenheiro DevOps', 'Cientista de Dados',
                         'Analista Cibersegurança', 'Arquiteto Cloud', 'Engenheiro de Dados',
                         'Desenvolvedor Full Stack', 'Especialista IoT', 'Product Manager (TI)', 
                         'UX/UI Designer', 'Engenheiro de Blockchain', 'SRE', 
                         'Especialista em RPA', 'Desenvolvedor Mobile', 'Analista de BI'],
            'Crescimento (%)': [35, 32, 30, 28, 25, 22, 20, 18, 15, 12, 22, 24, 16, 14, 10],
            'Salário Médio (R$)': [18000, 15000, 16000, 14000, 17000, 15500, 12000, 13000, 14500, 11000,
                                  16500, 15800, 12500, 11000, 9800],
            'Subsetor': ['IA & Dados', 'Infraestrutura', 'IA & Dados', 'Segurança', 'Infraestrutura', 
                        'IA & Dados', 'Desenvolvimento', 'IoT', 'Gestão', 'Desenvolvimento',
                        'Blockchain', 'Infraestrutura', 'Automação', 'Desenvolvimento', 'IA & Dados']
        }
        
        self.profissoes_queda = {
            'Profissão': ['Operador CAD', 'Programador COBOL', 'Especialista Legacy Systems',
                         'Técnico Hardware PC', 'Técnico Cabeamento', 'Suporte Telefônico TI',
                         'Especialista SOAP', 'DBA SQL Server 2008', 'Administrador Windows Server 2012',
                         'Técnico DataCenter Físico'],
            'Redução (%)': [-40, -60, -55, -45, -35, -50, -65, -48, -38, -30],
            'Salário Médio (R$)': [2100, 5000, 6200, 3500, 2800, 2500, 5500, 6800, 7200, 4000],
            'Subsetor': ['Design', 'Programação Legacy', 'Manutenção', 'Hardware', 'Infraestrutura', 
                        'Suporte', 'Integração', 'Banco de Dados', 'Administração', 'Infraestrutura']
        }
        
        self.top_salarios = {
            'Profissão': ['CIO/CTO', 'Especialista Segurança Ofensiva', 'Arquiteto Big Data',
                         'Cientista de Dados Sênior', 'Líder IA Enterprise', 'Especialista Blockchain',
                         'Gerente DevSecOps', 'Arquiteto Soluções Cloud', 'Consultor SAP',
                         'SRE Especialista'],
            'Salário (R$)': [32000, 28000, 25000, 24000, 23000, 22000, 21000, 20000, 19000, 18500]
        }
        
        self.habilidades_demandadas = {
            'Habilidade': ['Inteligência Artificial', 'Cloud Computing', 'Segurança Cibernética',
                          'Desenvolvimento Ágil', 'Arquitetura Microserviços', 'Infraestrutura como Código',
                          'Análise de Dados', 'CI/CD', 'Blockchain', 'Experiência do Usuário'],
            'Importância (%)': [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]
        }
        
        # Criar DataFrames
        self.df_alta = pd.DataFrame(self.profissoes_alta)
        self.df_queda = pd.DataFrame(self.profissoes_queda)
        self.df_salarios = pd.DataFrame(self.top_salarios)
        self.df_habilidades = pd.DataFrame(self.habilidades_demandadas)

class MarketDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Mercado de TI 2025-2030")
        self.root.geometry("1200x800")
        self.data = MarketData()
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Criar interface
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        self.create_header()
        
        # Painel de controle
        self.create_control_panel()
        
        # Área de visualização
        self.create_view_area()
        
        # Mostrar visualização inicial
        self.update_view()
    
    def create_header(self):
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame,
            text="MERCADO DE TI 2025-2030 - ANÁLISE E PROJEÇÕES",
            style='Header.TLabel'
        ).pack()
        
        ttk.Label(
            header_frame,
            text="Fontes: Fórum Econômico Mundial, Brasscom, ABES, Robert Half, Gartner",
            style='TLabel'
        ).pack()
    
    def create_control_panel(self):
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Seletor de visualização
        ttk.Label(control_frame, text="Visualização:").grid(row=0, column=0, padx=5)
        self.view_var = tk.StringVar(value="alta")
        
        views = [
            ("Profissões em Alta", "alta"),
            ("Profissões em Queda", "queda"),
            ("Salários Top", "salarios"),
            ("Habilidades Demandadas", "habilidades")
        ]
        
        for i, (text, mode) in enumerate(views):
            ttk.Radiobutton(
                control_frame,
                text=text,
                variable=self.view_var,
                value=mode,
                command=self.update_view
            ).grid(row=0, column=i+1, padx=5)
        
        # Filtro por subsetor de TI
        ttk.Label(control_frame, text="Filtrar por Subsetor:").grid(row=1, column=0, pady=10)
        self.sector_var = tk.StringVar(value="Todos")
        
        subsetores = ["Todos"] + sorted(set(self.data.df_alta['Subsetor'].unique().tolist() + 
                                      self.data.df_queda['Subsetor'].unique().tolist()))
        
        self.sector_menu = ttk.OptionMenu(
            control_frame,
            self.sector_var,
            *subsetores,
            command=lambda _: self.update_view()
        )
        self.sector_menu.grid(row=1, column=1, columnspan=2, pady=10)
        
        # Controle de número de itens
        ttk.Label(control_frame, text="Número de Itens:").grid(row=1, column=3, pady=10)
        self.num_items = tk.IntVar(value=10)
        
        ttk.Scale(
            control_frame,
            from_=5,
            to=15,
            variable=self.num_items,
            command=lambda _: self.update_view()
        ).grid(row=1, column=4, columnspan=2, pady=10)
        
        ttk.Label(control_frame, textvariable=self.num_items).grid(row=1, column=6, pady=10)
    
    def create_view_area(self):
        self.view_frame = ttk.Frame(self.main_frame)
        self.view_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para os gráficos
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.view_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Barra de ferramentas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.view_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)
    
    def update_view(self, *args):
        view_mode = self.view_var.get()
        sector = self.sector_var.get()
        num_items = self.num_items.get()
        
        self.figure.clear()
        
        if view_mode == "alta":
            self.show_growth(sector, num_items)
        elif view_mode == "queda":
            self.show_decline(sector, num_items)
        elif view_mode == "salarios":
            self.show_salaries(num_items)
        elif view_mode == "habilidades":
            self.show_skills(num_items)
        
        self.canvas.draw()
    
    def show_growth(self, sector, num_items):
        df = self.data.df_alta.copy()
        
        if sector != "Todos":
            df = df[df['Subsetor'] == sector]
        
        df = df.sort_values('Crescimento (%)', ascending=False).head(num_items)
        
        ax = self.figure.add_subplot(111)
        colors = cm.Greens(np.linspace(0.4, 1, len(df)))
        
        bars = ax.barh(df['Profissão'], df['Crescimento (%)'], color=colors)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{width}%', ha='left', va='center')
        
        ax.set_title(f'Profissões de TI em Alta ({sector}) - Crescimento 2025-2030', pad=20, fontweight='bold')
        ax.set_xlabel('Crescimento Percentual')
        ax.grid(axis='x', alpha=0.3)
        
        for i, (_, row) in enumerate(df.iterrows()):
            ax.text(1.02, i, f"R${row['Salário Médio (R$)']:,.0f}".replace(',', '.'),
                   va='center', transform=ax.get_yaxis_transform())
        
        ax.text(1.02, -0.5, 'Salário Médio:', transform=ax.get_yaxis_transform(), fontweight='bold')
        
        for spine in ['top', 'right', 'left']:
            ax.spines[spine].set_visible(False)
        
        self.figure.tight_layout()
    
    def show_decline(self, sector, num_items):
        df = self.data.df_queda.copy()
        
        if sector != "Todos":
            df = df[df['Subsetor'] == sector]
        
        df = df.sort_values('Redução (%)').head(num_items)
        
        ax = self.figure.add_subplot(111)
        colors = cm.Reds(np.linspace(0.3, 1, len(df)))
        
        bars = ax.barh(df['Profissão'], df['Redução (%)'], color=colors)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width - 1 if width < 0 else width + 1,
                   bar.get_y() + bar.get_height()/2,
                   f'{width}%', ha='left' if width > 0 else 'right', va='center')
        
        ax.set_title(f'Profissões de TI em Queda ({sector}) - Redução 2025-2030', pad=20, fontweight='bold')
        ax.set_xlabel('Redução Percentual')
        ax.axvline(0, color='black', linewidth=0.8)
        ax.grid(axis='x', alpha=0.3)
        
        for i, (_, row) in enumerate(df.iterrows()):
            ax.text(1.02, i, f"R${row['Salário Médio (R$)']:,.0f}".replace(',', '.'),
                   va='center', transform=ax.get_yaxis_transform())
        
        ax.text(1.02, -0.5, 'Salário Médio:', transform=ax.get_yaxis_transform(), fontweight='bold')
        
        for spine in ['top', 'right', 'left']:
            ax.spines[spine].set_visible(False)
        
        self.figure.tight_layout()
    
    def show_salaries(self, num_items):
        df = self.data.df_salarios.sort_values('Salário (R$)', ascending=False).head(num_items)
        
        ax = self.figure.add_subplot(111)
        colors = cm.Blues(np.linspace(0.4, 1, len(df)))
        
        bars = ax.bar(df['Profissão'], df['Salário (R$)'], color=colors)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 200,
                   f"R${height:,.0f}".replace(',', '.'), ha='center', va='bottom')
        
        ax.set_title(f'Top {len(df)} Salários em TI - 2025', pad=20, fontweight='bold')
        ax.set_ylabel('Salário Mensal (R$)')
        ax.tick_params(axis='x', rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        for spine in ['top', 'right', 'left']:
            ax.spines[spine].set_visible(False)
        
        self.figure.tight_layout()
    
    def show_skills(self, num_items):
        df = self.data.df_habilidades.sort_values('Importância (%)', ascending=False).head(num_items)
        
        ax = self.figure.add_subplot(111)
        
        wedges, texts, autotexts = ax.pie(
            df['Importância (%)'],
            labels=df['Habilidade'],
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            colors=cm.Purples(np.linspace(0.3, 1, len(df)))
        )
        
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        ax.set_title(f'Top {len(df)} Habilidades Técnicas Demandadas em TI 2025-2030', pad=20, fontweight='bold')
        
        self.figure.tight_layout()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarketDashboard(root)
    root.mainloop()