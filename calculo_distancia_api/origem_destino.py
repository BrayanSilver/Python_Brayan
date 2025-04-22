import pandas as pd
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from tqdm import tqdm

class DistanciaCalculator:
    def __init__(self, caminho_planilha, nome_aba):
        self.caminho_planilha = caminho_planilha
        self.nome_aba = nome_aba
        self.geolocator = Nominatim(user_agent="calc_distancia_cte", timeout=15)
        self.df = None
        self.cache_coordenadas = {}  # Cache para evitar consultas repetidas
    
    def carregar_dados(self):
        """Carrega os dados da planilha Excel."""
        self.df = pd.read_excel(self.caminho_planilha, sheet_name=self.nome_aba)
        return self.df
    
    def get_cidade_uf_por_cep(self, cep):
        """Obtém cidade e UF a partir do CEP usando ViaCEP."""
        cep = str(cep).strip().replace("-", "").replace(".", "")
        if len(cep) != 8 or not cep.isdigit():
            return None
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            if response.status_code == 200 and "erro" not in response.json():
                data = response.json()
                return f"{data['localidade']}, {data['uf']}, Brasil"
        except Exception as e:
            print(f"Erro ao buscar CEP {cep}: {e}")
        return None

    def obter_coordenadas(self, local):
        """Obtém latitude e longitude de um endereço com cache."""
        # Verifica se já temos no cache
        if local in self.cache_coordenadas:
            return self.cache_coordenadas[local]
            
        try:
            location = self.geolocator.geocode(local)
            if location:
                coords = (location.latitude, location.longitude)
                # Salva no cache
                self.cache_coordenadas[local] = coords
                return coords
        except Exception as e:
            print(f"Erro ao geocodificar {local}: {e}")
        return None

    def calcular_distancia(self, origem_cidade, origem_uf, destino_cep):
        """Calcula a distância entre origem (cidade+UF) e destino (CEP)."""
        origem_local = f"{origem_cidade}, {origem_uf}, Brasil"
        destino_local = self.get_cidade_uf_por_cep(destino_cep)
        
        if not destino_local:
            return None
        
        coord_origem = self.obter_coordenadas(origem_local)
        coord_destino = self.obter_coordenadas(destino_local)
        
        if coord_origem and coord_destino:
            return round(geodesic(coord_origem, coord_destino).kilometers, 2)
        return None
    
    def processar_distancias(self):
        """Processa todas as linhas do DataFrame e calcula as distâncias."""
        if self.df is None:
            self.carregar_dados()
            
        # Adiciona coluna de distância
        self.df["Distância Aproximada (km)"] = None
        
        # Processa cada linha com barra de progresso
        for index, row in tqdm(self.df.iterrows(), total=len(self.df), desc="Calculando distâncias"):
            origem_cidade = row["Nome do Município de Origem"]
            origem_uf = row["UF do Município de Origem"]
            destino_cep = row["CEP - Destinatário"]
            
            distancia = self.calcular_distancia(origem_cidade, origem_uf, destino_cep)
            self.df.at[index, "Distância Aproximada (km)"] = distancia
        
        return self.df
    
    def salvar_resultados(self):
        """Salva o DataFrame com distâncias calculadas em uma nova planilha."""
        if self.df is None:
            raise ValueError("Nenhum dado processado. Execute processar_distancias() primeiro.")
            
        novo_caminho = self.caminho_planilha.replace(".xlsx", "_COM_DISTANCIA.xlsx")
        self.df.to_excel(novo_caminho, index=False, sheet_name=self.nome_aba)
        return novo_caminho

# Exemplo de uso
if __name__ == "__main__":
    CAMINHO_PLANILHA = r"\blabla.xlsx"
    NOME_ABA = "Sheet0"
    
    calculator = DistanciaCalculator(CAMINHO_PLANILHA, NOME_ABA)
    df = calculator.carregar_dados()
    
    print("Dados originais:")
    print(df.head())
    
    df_com_distancias = calculator.processar_distancias()
    
    print("\nDados com distâncias calculadas:")
    print(df_com_distancias.head())
    
    novo_caminho = calculator.salvar_resultados()
    print(f"\n✅ Planilha atualizada salva em: {novo_caminho}")
    
    # Análise básica das distâncias
    distancias = df_com_distancias["Distância Aproximada (km)"].dropna()
    if len(distancias) > 0:
        print(f"\nResumo estatístico das distâncias:")
        print(f"Total de distâncias calculadas: {len(distancias)}")
        print(f"Distância média: {distancias.mean():.2f} km")
        print(f"Distância mínima: {distancias.min():.2f} km")
        print(f"Distância máxima: {distancias.max():.2f} km")