# 📊 Dashboard Interativo - Mercado de TI 2025-2030

Dashboard interativo para visualização de dados do mercado de TI com análise e projeções.

## 🚀 Funcionalidades

- ✅ Visualização de profissões em alta
- ✅ Visualização de profissões em queda
- ✅ Top salários do mercado
- ✅ Habilidades mais demandadas
- ✅ Filtros por subsetor de TI
- ✅ Controle de número de itens exibidos
- ✅ Interface gráfica interativa (Tkinter)
- ✅ Gráficos interativos com matplotlib

## 📦 Instalação

```bash
pip install matplotlib pandas numpy seaborn
```

Ou use o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Executar o Dashboard

```bash
cd dashboard
python index.py
```

## 🎯 Funcionalidades do Dashboard

### Visualizações Disponíveis

1. **Profissões em Alta**
   - Mostra profissões com maior crescimento projetado
   - Exibe crescimento percentual e salário médio
   - Filtro por subsetor de TI

2. **Profissões em Queda**
   - Mostra profissões com redução de demanda
   - Exibe redução percentual e salário médio
   - Filtro por subsetor de TI

3. **Salários Top**
   - Ranking das profissões com maiores salários
   - Visualização em barras verticais

4. **Habilidades Demandadas**
   - Top habilidades técnicas mais procuradas
   - Visualização em gráfico de pizza

### Controles

- **Seletor de Visualização**: Escolha entre as 4 visualizações
- **Filtro por Subsetor**: Filtre por área específica de TI
- **Número de Itens**: Ajuste quantos itens exibir (5-15)

## 📊 Dados

Os dados são baseados em fontes confiáveis:
- Fórum Econômico Mundial
- Brasscom
- ABES
- Robert Half
- Gartner

## 🎨 Interface

- Interface gráfica moderna com Tkinter
- Gráficos interativos com matplotlib
- Estilo seaborn para visualizações elegantes
- Cores diferenciadas por tipo de visualização

## 🔧 Tecnologias

- **Python 3.7+**
- **Tkinter**: Interface gráfica
- **Matplotlib**: Gráficos e visualizações
- **Pandas**: Manipulação de dados
- **NumPy**: Operações numéricas
- **Seaborn**: Estilos e paletas

## 📝 Notas

- O dashboard abre em uma janela separada
- Use os controles na parte superior para navegar
- Os gráficos são interativos (zoom, pan, etc.)
- Dados são projetados para o período 2025-2030

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'matplotlib'"
```bash
pip install matplotlib pandas numpy seaborn
```

### Erro: "'seaborn' is not a valid package style"
- Instale seaborn: `pip install seaborn`
- O código foi atualizado para usar seaborn corretamente

### Janela não abre
- Verifique se o Tkinter está instalado (geralmente vem com Python)
- No Linux: `sudo apt-get install python3-tk`
