# Imports do App
import streamlit as st
import datetime
import yfinance as yf
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(initial_sidebar_state='expanded', page_title="Indices")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Conteúdo Sidebar

image=Image.open("./images/obinveste.png")

with st.sidebar:
    st.sidebar.image(image, width=200)
    st.divider()
    icon_info = '''                                                                                                                                                       
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

    <i class="fa-solid fa-circle-info" style="font-size: 1rem; color: #34A69D"></i> 
    <span style="font-size: 1.5rem; font-weight: 600;">&nbsp;Sobre</span>
    '''

    st.write(
        icon_info,
        unsafe_allow_html=True,
        ) 
    st.subheader('Índices das principais bolsas')
    st.write('Esta aplicação tem o intuito de comparar os índices das principais bolsas e da ibovespa. Com isso, é possível analisar a porcentagem de valorização e desvalorização, além de ver o contador de variações positivas e negativas.')
    with st.expander(':computer: Desenvolvedores'):
        st.markdown('''
        Luiz Fernando | Mateus Rangel | Pedro Cantanhêde | Raphael Santos
        
        ''')
    icon_social = '''                                                                                                                                                       
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

    <div style="text-align: center; bottom: 0; position: fixed; width: 20rem; margin-bottom: 1rem;">
        <p>Nos sigam nas <span style="color: #34A69D;">redes sociais!</span></p>
        <a href="https://www.facebook.com/obinvestbrasil"><i class="fa-brands fa-facebook-f" style="font-size: 1.2rem; color: #34A69D; margin-right: 1.3rem;"></i></a>
        <a href="https://www.instagram.com/obinvestbrasil/"><i class="fa-brands fa-instagram" style="font-size: 1.2rem; color: #34A69D; margin-right: 1.3rem;"></i></a>
        <a href="https://twitter.com/obinvestbrasil"><i class="fa-brands fa-twitter" style="font-size: 1rem; color: #34A69D"></i></a> 
    </div>
    '''

    st.write(
        icon_social, 
        unsafe_allow_html=True,
        ) 

# Conteúdo Principal - Header

st.write('')
text_header = '''                                                                                                                                                       
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Code&display=swap" rel="stylesheet">                                                                                                

<p style="font-family: 'Fira Code', monospace; color: #34A69D; font-size: 1rem; margin-bottom: 3rem;">Aprenda sobre investimentos e educação financeira!</p>
'''

st.write(text_header, unsafe_allow_html=True)


icon_chart = '''                                                                                                                                                       
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

<i class="fa-solid fa-chart-gantt" style="font-size: 4rem; color: #34A69D"></i>
'''

st.write(icon_chart, unsafe_allow_html=True)

st.subheader('Índices')

# Tabs (Navegação de abas para cada funcionalidade)

tab1, tab2, tab3, tab4 = st.tabs(["Variação Semanal", "Variação por Período", "Contador Semanal", "Contador Período"])

with tab1:
    st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>Variação Percentual em Relação a <span style='color: #34A69D;'>Semana Anterior</span>",
             unsafe_allow_html=True)
    mpl.rc('text', color='white')
    mpl.rc('axes', labelcolor='white')
    mpl.rc('xtick', color='white')
    mpl.rc('ytick', color='white')

    indices = {'^HSI': 'Hong Kong 50', '^FCHI': 'CAC 40', '^GSPTSE': 'S&P/TSX Composite', '^FTSE': 'FTSE 100', '^N100': 'Euro Stoxx 100', '^GDAXI': 'DAX', '^DJI': 'Dow Jones', '^MXX': 'IPC', '^BVSP': 'Bovespa', '^GSPC': 'S&P 500', '^N225': 'Nikkei 225', '^MERV': 'MERVAL', 'IMOEX.ME': 'MOEX Russia Index', '^BSESN': 'BSE Sensex', '^IXIC': 'NASDAQ Composite'}

    # Obter o mês atual
    data_atual = datetime.datetime.now()
    data_inicio = datetime.datetime(data_atual.year, data_atual.month, 1)
    data_inicio_str = data_inicio.strftime("%Y-%m-%d")
    data_atual_str = data_atual.strftime("%Y-%m-%d")

    data = yf.download(list(indices.keys()), start=data_inicio_str, end=data_atual_str)['Close']

    weekly_returns = data.pct_change(periods=5) * 100

    sorted_returns = weekly_returns.iloc[-1].sort_values(ascending=False)

    sorted_indices = sorted_returns.index

    positive_returns = sorted_returns[sorted_returns >= 0]
    negative_returns = sorted_returns[sorted_returns < 0]

    fig, ax = plt.subplots(figsize=(5, 6))
    fig.patch.set_facecolor('#2c2c32')
    ax.barh([indices[idx] for idx in positive_returns.index], positive_returns, color='#34A69D')
    ax.barh([indices[idx] for idx in negative_returns.index], negative_returns, color='#ce1c5b')
    ax.axvline(x=0, color='white', linestyle='--')

    ax.set_facecolor("#2c2c32")

    plt.xlabel('% Variação')
    plt.ylabel('Índices')

    # Adiciona as porcentagens ao lado de cada barra
    for i, (index, value) in enumerate(zip(positive_returns.index, positive_returns)):
        ax.text(0, i, f'{value:.2f}%', ha='right', va='center', color='white', fontweight='bold')
        y = i
    for i, (index, value) in enumerate(zip(negative_returns.index, negative_returns)):
        ax.text(0, y+1+i, f'{value:.2f}%', ha='left', va='center', color='white', fontweight='bold')

    st.pyplot(fig)

    st.divider()

    st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>IBOV - Variação Percentual em Relação a <span style='color: #34A69D;'>Semana Anterior</span>",
             unsafe_allow_html=True)
    mpl.rc('text', color='white')
    mpl.rc('axes', labelcolor='white')
    mpl.rc('xtick', color='white')
    mpl.rc('ytick', color='white')

    indices = {"RRRP3.SA": "3R PETROLEUM", "ALSO3.SA": "ALIANSCSONAE", "ALPA4.SA": "ALPARGATAS", "ABEV3.SA": "AMBEV S/A", "ARZZ3.SA": "AREZZO CO", "ASAI3.SA": "ASSAI", "AZUL4.SA": "AZUL", "B3SA3.SA": "B3", "BBSE3.SA": "BBSEGURIDADE", "BBDC3.SA": "BRADESCO", "BBDC4.SA": "BRADESCO", "BRAP4.SA": "BRADESPAR", "BBAS3.SA": "BRASIL", "BRKM5.SA": "BRASKEM", "BRFS3.SA": "BRF SA", "BPAC11.SA": "BTGP BANCO", "CRFB3.SA": "CARREFOUR BR", "CCRO3.SA": "CCR SA", "CMIG4.SA": "CEMIG", "CIEL3.SA": "CIELO", "COGN3.SA": "COGNA ON", "CPLE6.SA": "COPEL", "CSAN3.SA": "COSAN", "CPFE3.SA": "CPFL ENERGIA", "CMIN3.SA": "CSNMINERACAO", "CVCB3.SA": "CVC BRASIL", "CYRE3.SA": "CYRELA REALT", "DXCO3.SA": "DEXCO", "ELET3.SA": "ELETROBRAS", "ELET6.SA": "ELETROBRAS", "EMBR3.SA": "EMBRAER", "ENBR3.SA": "ENERGIAS BR", "ENGI11.SA": "ENERGISA", "ENEV3.SA": "ENEVA", "EGIE3.SA": "ENGIE BRASIL", "EQTL3.SA": "EQUATORIAL", "EZTC3.SA": "EZTEC", "FLRY3.SA": "FLEURY", "GGBR4.SA": "GERDAU", "GOAU4.SA": "GERDAU MET", "GOLL4.SA": "GOL", "NTCO3.SA": "GRUPO NATURA", "SOMA3.SA": "GRUPO SOMA", "HAPV3.SA": "HAPVIDA", "HYPE3.SA": "HYPERA", "IGTI11.SA": "IGUATEMI S.A", "IRBR3.SA": "IRBBRASIL RE", "ITSA4.SA": "ITAUSA", "ITUB4.SA": "ITAUUNIBANCO", "JBSS3.SA": "JBS", "KLBN11.SA": "KLABIN S/A", "RENT3.SA": "LOCALIZA", "LWSA3.SA": "LOCAWEB", "LREN3.SA": "LOJAS RENNER", "MGLU3.SA": "MAGAZ LUIZA", "MRFG3.SA": "MARFRIG", "CASH3.SA": "MELIUZ", "BEEF3.SA": "MINERVA", "MRVE3.SA": "MRV", "MULT3.SA": "MULTIPLAN", "PCAR3.SA": "P.ACUCAR-CBD", "PETR3.SA": "PETROBRAS", "PETR4.SA": "PETROBRAS", "PRIO3.SA": "PETRORIO", "PETZ3.SA": "PETZ", "RADL3.SA": "RAIADROGASIL", "RAIZ4.SA": "RAIZEN", "RDOR3.SA": "REDE D OR", "RAIL3.SA": "RUMO S.A.", "SBSP3.SA": "SABESP", "SANB11.SA": "SANTANDER BR", "SMTO3.SA": "SAO MARTINHO", "CSNA3.SA": "SID NACIONAL", "SLCE3.SA": "SLC AGRICOLA", "SUZB3.SA": "SUZANO S.A.", "TAEE11.SA": "TAESA", "VIVT3.SA": "TELEF BRASIL", "TIMS3.SA": "TIM", "TOTS3.SA": "TOTVS", "UGPA3.SA": "ULTRAPAR", "USIM5.SA": "USIMINAS", "VALE3.SA": "VALE", "VIIA3.SA": "VIA", "VBBR3.SA": "VIBRA", "WEGE3.SA": "WEG", "YDUQ3.SA": "YDUQS PART"}

    data = yf.download(list(indices.keys()), start='2023-05-01', end='2023-05-29')['Close']

    weekly_returns = data.pct_change(periods=5) * 100

    sorted_returns = weekly_returns.iloc[-1].sort_values(ascending=False)

    sorted_indices = sorted_returns.index

    positive_returns = sorted_returns[sorted_returns >= 0]
    negative_returns = sorted_returns[sorted_returns < 0]

    fig, ax = plt.subplots(figsize=(6, 50))
    fig.patch.set_facecolor('#2c2c32')
    ax.barh([indices[idx] for idx in positive_returns.index], positive_returns, color='#34A69D')
    ax.barh([indices[idx] for idx in negative_returns.index], negative_returns, color='#ce1c5b')
    ax.axvline(x=0, color='white', linestyle='--')

    ax.set_facecolor("#2c2c32")

    plt.xlabel('% Variação')
    plt.ylabel('Índices')

    # Adiciona as porcentagens ao lado de cada barra
    for i, (index, value) in enumerate(zip(positive_returns.index, positive_returns)):
        ax.text(0, i, f'{value:.2f}%', ha='right', va='center', color='white', fontweight='bold')
        y = i
    for i, (index, value) in enumerate(zip(negative_returns.index, negative_returns)):
        ax.text(0, y+1+i, f'{value:.2f}%', ha='left', va='center', color='white', fontweight='bold')

    fig_all, ax = plt.subplots(figsize=(60, 20))
    fig_all.patch.set_facecolor('#2c2c32')
    ax.barh([indices[idx] for idx in positive_returns.index], positive_returns, color='#34A69D')
    ax.barh([indices[idx] for idx in negative_returns.index], negative_returns, color='#ce1c5b')
    ax.axvline(x=0, color='#2c2c32', linestyle='--')

    ax.set_facecolor("#2c2c32")

    plt.xlabel('% Variação')
    plt.ylabel('Índices')

    # Adiciona as porcentagens ao lado de cada barra
    for i, (index, value) in enumerate(zip(positive_returns.index, positive_returns)):
        ax.text(0, i, f'{value:.2f}%', ha='right', va='center', color='#2c2c32', fontweight='bold')
        y = i
    for i, (index, value) in enumerate(zip(negative_returns.index, negative_returns)):
        ax.text(0, y+1+i, f'{value:.2f}%', ha='left', va='center', color='#2c2c32', fontweight='bold')

    st.pyplot(fig_all)
    st.pyplot(fig)
   
with tab2:
   # Conteúdo Principal - Input
   st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>Variação Percentual em Relação ao <span style='color: #34A69D;'>Período</span>",
             unsafe_allow_html=True)
   
   mpl.rc('text', color='white')
   mpl.rc('axes', labelcolor='white')
   mpl.rc('xtick', color='white')
   mpl.rc('ytick', color='white')

   # Input das datas
   # Primeira Data
   icon_date = '''                                                                                                                                                       
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

<i class="fa-regular fa-calendar" style="font-size: 1rem; color: #34A69D"></i>
'''

   st.write(
    icon_date + '&nbsp;Informe a primeira data', 
    unsafe_allow_html=True,
    )
   start_date = st.date_input('Data de início', datetime.date(2023, 1, 1), label_visibility="collapsed", key="start")

   # Última Data
   icon_date = '''                                                                                                                                                       
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

<i class="fa-regular fa-calendar" style="font-size: 1rem; color: #34A69D"></i>
'''

   st.write(
    icon_date + '&nbsp;Informe a segunda data', 
    unsafe_allow_html=True,
    )
   end_date = st.date_input('Data de fim', label_visibility="collapsed", key="end")

   # Download dos dados
   indices = {'^HSI': 'Hong Kong 50', '^FCHI': 'CAC 40', '^GSPTSE': 'S&P/TSX Composite', '^FTSE': 'FTSE 100', '^N100': 'Euro Stoxx 100', '^GDAXI': 'DAX', '^DJI': 'Dow Jones', '^MXX': 'IPC', '^BVSP': 'Bovespa', '^GSPC': 'S&P 500', '^N225': 'Nikkei 225', '^MERV': 'MERVAL', 'IMOEX.ME': 'MOEX Russia Index', '^BSESN': 'BSE Sensex', '^IXIC': 'NASDAQ Composite'}
   data = yf.download(list(indices.keys()), start=start_date, end=end_date)['Close']

   # Cálculo das variações percentuais semanais
   weekly_returns = data.pct_change(periods=5) * 100

   # Ordenação dos índices pela variação percentual mais recente
   sorted_returns = weekly_returns.iloc[-1].sort_values(ascending=False)
   sorted_indices = sorted_returns.index

   # Separação entre variações positivas e negativas
   positive_returns = sorted_returns[sorted_returns >= 0]
   negative_returns = sorted_returns[sorted_returns < 0]

   # Plot dos gráficos
   fig, ax = plt.subplots(figsize=(5, 6))
   fig.patch.set_facecolor('#2c2c32')

   ax.barh([indices[idx] for idx in positive_returns.index], positive_returns, color='#34A69D')
   ax.barh([indices[idx] for idx in negative_returns.index], negative_returns, color='#ce1c5b')
   ax.axvline(x=0, color='white', linestyle='--')

   ax.set_facecolor("#2c2c32")

   plt.xlabel('% Variação')
   plt.ylabel('Índices')

   # Adiciona as porcentagens ao lado de cada barra
   for i, (index, value) in enumerate(zip(positive_returns.index, positive_returns)):
       ax.text(0, i, f'{value:.2f}%', ha='right', va='center', color='white', fontweight='bold')
       y = i
   for i, (index, value) in enumerate(zip(negative_returns.index, negative_returns)):
       ax.text(0, y+1+i, f'{value:.2f}%', ha='left', va='center', color='white', fontweight='bold')

   # Exibe o gráfico no Streamlit
   st.pyplot(fig)

   st.divider()

   #IBOV

   # Conteúdo Principal - Input
   st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>IBOV - Variação Percentual em Relação ao <span style='color: #34A69D;'>Período</span>",
             unsafe_allow_html=True)
   
   mpl.rc('text', color='white')
   mpl.rc('axes', labelcolor='white')
   mpl.rc('xtick', color='white')
   mpl.rc('ytick', color='white')

   # Input das datas
   # Primeira Data
   icon_date = '''                                                                                                                                                       
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

<i class="fa-regular fa-calendar" style="font-size: 1rem; color: #34A69D"></i>
'''

   st.write(
    icon_date + '&nbsp;Informe a primeira data', 
    unsafe_allow_html=True,
    )
   start_date = st.date_input('Data de início', datetime.date(2023, 1, 1), label_visibility="collapsed", key="start_ibov")

   # Última Data
   icon_date = '''                                                                                                                                                       
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

<i class="fa-regular fa-calendar" style="font-size: 1rem; color: #34A69D"></i>
'''

   st.write(
    icon_date + '&nbsp;Informe a segunda data', 
    unsafe_allow_html=True,
    )
   end_date = st.date_input('Data de fim', label_visibility="collapsed", key="end_ibov")

   # Download dos dados
   indices = {"RRRP3.SA": "3R PETROLEUM", "ALSO3.SA": "ALIANSCSONAE", "ALPA4.SA": "ALPARGATAS", "ABEV3.SA": "AMBEV S/A", "ARZZ3.SA": "AREZZO CO", "ASAI3.SA": "ASSAI", "AZUL4.SA": "AZUL", "B3SA3.SA": "B3", "BBSE3.SA": "BBSEGURIDADE", "BBDC3.SA": "BRADESCO", "BBDC4.SA": "BRADESCO", "BRAP4.SA": "BRADESPAR", "BBAS3.SA": "BRASIL", "BRKM5.SA": "BRASKEM", "BRFS3.SA": "BRF SA", "BPAC11.SA": "BTGP BANCO", "CRFB3.SA": "CARREFOUR BR", "CCRO3.SA": "CCR SA", "CMIG4.SA": "CEMIG", "CIEL3.SA": "CIELO", "COGN3.SA": "COGNA ON", "CPLE6.SA": "COPEL", "CSAN3.SA": "COSAN", "CPFE3.SA": "CPFL ENERGIA", "CMIN3.SA": "CSNMINERACAO", "CVCB3.SA": "CVC BRASIL", "CYRE3.SA": "CYRELA REALT", "DXCO3.SA": "DEXCO", "ELET3.SA": "ELETROBRAS", "ELET6.SA": "ELETROBRAS", "EMBR3.SA": "EMBRAER", "ENBR3.SA": "ENERGIAS BR", "ENGI11.SA": "ENERGISA", "ENEV3.SA": "ENEVA", "EGIE3.SA": "ENGIE BRASIL", "EQTL3.SA": "EQUATORIAL", "EZTC3.SA": "EZTEC", "FLRY3.SA": "FLEURY", "GGBR4.SA": "GERDAU", "GOAU4.SA": "GERDAU MET", "GOLL4.SA": "GOL", "NTCO3.SA": "GRUPO NATURA", "SOMA3.SA": "GRUPO SOMA", "HAPV3.SA": "HAPVIDA", "HYPE3.SA": "HYPERA", "IGTI11.SA": "IGUATEMI S.A", "IRBR3.SA": "IRBBRASIL RE", "ITSA4.SA": "ITAUSA", "ITUB4.SA": "ITAUUNIBANCO", "JBSS3.SA": "JBS", "KLBN11.SA": "KLABIN S/A", "RENT3.SA": "LOCALIZA", "LWSA3.SA": "LOCAWEB", "LREN3.SA": "LOJAS RENNER", "MGLU3.SA": "MAGAZ LUIZA", "MRFG3.SA": "MARFRIG", "CASH3.SA": "MELIUZ", "BEEF3.SA": "MINERVA", "MRVE3.SA": "MRV", "MULT3.SA": "MULTIPLAN", "PCAR3.SA": "P.ACUCAR-CBD", "PETR3.SA": "PETROBRAS", "PETR4.SA": "PETROBRAS", "PRIO3.SA": "PETRORIO", "PETZ3.SA": "PETZ", "RADL3.SA": "RAIADROGASIL", "RAIZ4.SA": "RAIZEN", "RDOR3.SA": "REDE D OR", "RAIL3.SA": "RUMO S.A.", "SBSP3.SA": "SABESP", "SANB11.SA": "SANTANDER BR", "SMTO3.SA": "SAO MARTINHO", "CSNA3.SA": "SID NACIONAL", "SLCE3.SA": "SLC AGRICOLA", "SUZB3.SA": "SUZANO S.A.", "TAEE11.SA": "TAESA", "VIVT3.SA": "TELEF BRASIL", "TIMS3.SA": "TIM", "TOTS3.SA": "TOTVS", "UGPA3.SA": "ULTRAPAR", "USIM5.SA": "USIMINAS", "VALE3.SA": "VALE", "VIIA3.SA": "VIA", "VBBR3.SA": "VIBRA", "WEGE3.SA": "WEG", "YDUQ3.SA": "YDUQS PART"}
   data = yf.download(list(indices.keys()), start=start_date, end=end_date)['Close']

   # Cálculo das variações percentuais semanais
   weekly_returns = data.pct_change(periods=5) * 100

   # Ordenação dos índices pela variação percentual mais recente
   sorted_returns = weekly_returns.iloc[-1].sort_values(ascending=False)
   sorted_indices = sorted_returns.index

   # Separação entre variações positivas e negativas
   positive_returns = sorted_returns[sorted_returns >= 0]
   negative_returns = sorted_returns[sorted_returns < 0]

   # Plot dos gráficos
   fig, ax = plt.subplots(figsize=(6, 50))
   fig.patch.set_facecolor('#2c2c32')

   ax.barh([indices[idx] for idx in positive_returns.index], positive_returns, color='#34A69D')
   ax.barh([indices[idx] for idx in negative_returns.index], negative_returns, color='#ce1c5b')
   ax.axvline(x=0, color='white', linestyle='--')

   ax.set_facecolor("#2c2c32")

   plt.xlabel('% Variação')
   plt.ylabel('Índices')

   # Adiciona as porcentagens ao lado de cada barra
   for i, (index, value) in enumerate(zip(positive_returns.index, positive_returns)):
       ax.text(0, i, f'{value:.2f}%', ha='right', va='center', color='white', fontweight='bold')
       y = i
   for i, (index, value) in enumerate(zip(negative_returns.index, negative_returns)):
       ax.text(0, y+1+i, f'{value:.2f}%', ha='left', va='center', color='white', fontweight='bold')

   # Exibe o gráfico no Streamlit
   st.pyplot(fig) 

with tab3:
   st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>Contagem de Variações <span style='color: #34A69D;'>Positivas</span> e <span style='color: #ce1c5b'>Negativas</span> por Dia</h3>",
             unsafe_allow_html=True)
   
   indices = {'^HSI': 'Hong Kong 50', '^FCHI': 'CAC 40', '^GSPTSE': 'S&P/TSX Composite', '^FTSE': 'FTSE 100', '^N100': 'Euro Stoxx 100', '^GDAXI': 'DAX', '^DJI': 'Dow Jones', '^MXX': 'IPC', '^BVSP': 'Bovespa', '^GSPC': 'S&P 500', '^N225': 'Nikkei 225', '^MERV': 'MERVAL', 'IMOEX.ME': 'MOEX Russia Index', '^BSESN': 'BSE Sensex', '^IXIC': 'NASDAQ Composite'}

   data = yf.download(list(indices.keys()), start='2022-05-01', end='2023-05-29')['Close']

   weekly_returns = data.pct_change(periods=30) * 100

   # Contagem de positivos e negativos por dia
   positive_counts = weekly_returns[weekly_returns >= 0].count(axis=1)
   negative_counts = weekly_returns[weekly_returns < 0].count(axis=1)

   # Positivos
   # Aumentar a largura da imagem
   fig_positive = plt.figure(figsize=(24, 6))
   fig_positive.patch.set_facecolor('#2c2c32')

   ax = plt.axes()

   # Plotagem do gráfico em linha
   plt.plot(positive_counts.index, positive_counts, label='Positivos', color='#34A69D')

   plt.xlabel('Data')
   plt.ylabel('Contagem')

   ax.set_facecolor('#2c2c32')

   st.markdown("<span style='color: #34A69D'>Positivos</span>",
             unsafe_allow_html=True)
   st.pyplot(fig_positive)

   # Negativos
   # Aumentar a largura da imagem
   fig_negative = plt.figure(figsize=(24, 6))
   fig_negative.patch.set_facecolor('#2c2c32')

   ax = plt.axes()

   # Plotagem do gráfico em linha
   plt.plot(negative_counts.index, negative_counts, label='Negativos', color='#ce1c5b')

   plt.xlabel('Data')
   plt.ylabel('Contagem')

   ax.set_facecolor('#2c2c32')

   st.markdown("<span style='color: #ce1c5b'>Negativos</span>",
             unsafe_allow_html=True)
   st.pyplot(fig_negative)

   st.divider()

   st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>IBOV - Contagem de Variações <span style='color: #34A69D;'>Positivas</span> e <span style='color: #ce1c5b'>Negativas</span> por Dia</h3>",
             unsafe_allow_html=True)

   indices_ibov = {"RRRP3.SA": "3R PETROLEUM", "ALSO3.SA": "ALIANSCSONAE", "ALPA4.SA": "ALPARGATAS", "ABEV3.SA": "AMBEV S/A", "ARZZ3.SA": "AREZZO CO", "ASAI3.SA": "ASSAI", "AZUL4.SA": "AZUL", "B3SA3.SA": "B3", "BBSE3.SA": "BBSEGURIDADE", "BBDC3.SA": "BRADESCO", "BBDC4.SA": "BRADESCO", "BRAP4.SA": "BRADESPAR", "BBAS3.SA": "BRASIL", "BRKM5.SA": "BRASKEM", "BRFS3.SA": "BRF SA", "BPAC11.SA": "BTGP BANCO", "CRFB3.SA": "CARREFOUR BR", "CCRO3.SA": "CCR SA", "CMIG4.SA": "CEMIG", "CIEL3.SA": "CIELO", "COGN3.SA": "COGNA ON", "CPLE6.SA": "COPEL", "CSAN3.SA": "COSAN", "CPFE3.SA": "CPFL ENERGIA", "CMIN3.SA": "CSNMINERACAO", "CVCB3.SA": "CVC BRASIL", "CYRE3.SA": "CYRELA REALT", "DXCO3.SA": "DEXCO", "ELET3.SA": "ELETROBRAS", "ELET6.SA": "ELETROBRAS", "EMBR3.SA": "EMBRAER", "ENBR3.SA": "ENERGIAS BR", "ENGI11.SA": "ENERGISA", "ENEV3.SA": "ENEVA", "EGIE3.SA": "ENGIE BRASIL", "EQTL3.SA": "EQUATORIAL", "EZTC3.SA": "EZTEC", "FLRY3.SA": "FLEURY", "GGBR4.SA": "GERDAU", "GOAU4.SA": "GERDAU MET", "GOLL4.SA": "GOL", "NTCO3.SA": "GRUPO NATURA", "SOMA3.SA": "GRUPO SOMA", "HAPV3.SA": "HAPVIDA", "HYPE3.SA": "HYPERA", "IGTI11.SA": "IGUATEMI S.A", "IRBR3.SA": "IRBBRASIL RE", "ITSA4.SA": "ITAUSA", "ITUB4.SA": "ITAUUNIBANCO", "JBSS3.SA": "JBS", "KLBN11.SA": "KLABIN S/A", "RENT3.SA": "LOCALIZA", "LWSA3.SA": "LOCAWEB", "LREN3.SA": "LOJAS RENNER", "MGLU3.SA": "MAGAZ LUIZA", "MRFG3.SA": "MARFRIG", "CASH3.SA": "MELIUZ", "BEEF3.SA": "MINERVA", "MRVE3.SA": "MRV", "MULT3.SA": "MULTIPLAN", "PCAR3.SA": "P.ACUCAR-CBD", "PETR3.SA": "PETROBRAS", "PETR4.SA": "PETROBRAS", "PRIO3.SA": "PETRORIO", "PETZ3.SA": "PETZ", "RADL3.SA": "RAIADROGASIL", "RAIZ4.SA": "RAIZEN", "RDOR3.SA": "REDE D OR", "RAIL3.SA": "RUMO S.A.", "SBSP3.SA": "SABESP", "SANB11.SA": "SANTANDER BR", "SMTO3.SA": "SAO MARTINHO", "CSNA3.SA": "SID NACIONAL", "SLCE3.SA": "SLC AGRICOLA", "SUZB3.SA": "SUZANO S.A.", "TAEE11.SA": "TAESA", "VIVT3.SA": "TELEF BRASIL", "TIMS3.SA": "TIM", "TOTS3.SA": "TOTVS", "UGPA3.SA": "ULTRAPAR", "USIM5.SA": "USIMINAS", "VALE3.SA": "VALE", "VIIA3.SA": "VIA", "VBBR3.SA": "VIBRA", "WEGE3.SA": "WEG", "YDUQ3.SA": "YDUQS PART"}

   data = yf.download(list(indices_ibov.keys()), start='2022-05-01', end='2023-05-29')['Close']

   weekly_returns = data.pct_change(periods=30) * 100

   # Contagem de positivos e negativos por dia
   positive_counts = weekly_returns[weekly_returns >= 0].count(axis=1)
   negative_counts = weekly_returns[weekly_returns < 0].count(axis=1)

   # Positivos
   # Aumentar a largura da imagem
   fig_ibov_positive = plt.figure(figsize=(24, 6))
   fig_ibov_positive.patch.set_facecolor('#2c2c32')

   ax_ibov = plt.axes()

   # Plotagem do gráfico em linha
   plt.plot(positive_counts.index, positive_counts, label='Positivos', color='#34A69D')

   plt.xlabel('Data')
   plt.ylabel('Contagem')

   ax_ibov.set_facecolor('#2c2c32')

   st.markdown("<span style='color: #34A69D'>Positivos</span>",
             unsafe_allow_html=True)
   st.pyplot(fig_ibov_positive)

   # Negativos
   # Aumentar a largura da imagem
   fig_ibov_negative = plt.figure(figsize=(24, 6))
   fig_ibov_negative.patch.set_facecolor('#2c2c32')

   ax_ibov = plt.axes()

   # Plotagem do gráfico em linha
   plt.plot(negative_counts.index, negative_counts, label='Negativos', color='#ce1c5b')

   plt.xlabel('Data')
   plt.ylabel('Contagem')

   ax_ibov.set_facecolor('#2c2c32')

   st.markdown("<span style='color: #ce1c5b'>Negativos</span>",
             unsafe_allow_html=True)
   st.pyplot(fig_ibov_negative)

with tab4:
    st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>Contagem de Variações <span style='color: #34A69D;'>Positivas</span> e <span style='color: #ce1c5b'>Negativas</span> por Período</h3>",
             unsafe_allow_html=True)
    
    indices = {'^HSI': 'Hong Kong 50', '^FCHI': 'CAC 40', '^GSPTSE': 'S&P/TSX Composite', '^FTSE': 'FTSE 100', '^N100': 'Euro Stoxx 100', '^GDAXI': 'DAX', '^DJI': 'Dow Jones', '^MXX': 'IPC', '^BVSP': 'Bovespa', '^GSPC': 'S&P 500', '^N225': 'Nikkei 225', '^MERV': 'MERVAL', 'IMOEX.ME': 'MOEX Russia Index', '^BSESN': 'BSE Sensex', '^IXIC': 'NASDAQ Composite'}

    data = yf.download(list(indices.keys()), start='2023-05-01', end='2023-05-12')['Close']

    daily_returns = data.pct_change() * 100

    # Positivos

    # Contagem de positivos por dia
    positive_counts = (daily_returns >= 0).sum(axis=1)

    # Aumentar a largura da imagem
    fig_positive = plt.figure(figsize=(24, 6))
    fig_positive.patch.set_facecolor('#2c2c32')

    ax_positive = plt.axes()

    ax_positive.set_facecolor('#2c2c32')

    # Plotagem do gráfico em linha
    plt.plot(positive_counts.index, positive_counts, label='Positivos', color='#34A69D')

    plt.xlabel('Data')
    plt.ylabel('Contagem')

    st.markdown("<span style='color: #34A69D'>Positivos</span>",
             unsafe_allow_html=True)
    st.pyplot(fig_positive)

    # Negativos

    # Contagem de negativos por dia
    negative_counts = (daily_returns < 0).sum(axis=1)

    # Aumentar a largura da imagem
    fig_negative = plt.figure(figsize=(24, 6))
    fig_negative.patch.set_facecolor('#2c2c32')

    ax_negative = plt.axes()

    ax_negative.set_facecolor('#2c2c32')

    # Plotagem do gráfico em linha
    plt.plot(negative_counts.index, negative_counts, label='Negativos', color='#ce1c5b')

    plt.xlabel('Data')
    plt.ylabel('Contagem')

    st.markdown("<span style='color: #ce1c5b'>Negativos</span>",
             unsafe_allow_html=True)
    st.pyplot(fig_negative)

    st.divider()

    # IBOV

    st.markdown("<h3 style='margin-bottom: 2rem; text-align: center;'>IBOV - Contagem de Variações <span style='color: #34A69D;'>Positivas</span> e <span style='color: #ce1c5b'>Negativas</span> por Período</h3>",
             unsafe_allow_html=True)
    
    indices = {"RRRP3.SA": "3R PETROLEUM", "ALSO3.SA": "ALIANSCSONAE", "ALPA4.SA": "ALPARGATAS", "ABEV3.SA": "AMBEV S/A", "ARZZ3.SA": "AREZZO CO", "ASAI3.SA": "ASSAI", "AZUL4.SA": "AZUL", "B3SA3.SA": "B3", "BBSE3.SA": "BBSEGURIDADE", "BBDC3.SA": "BRADESCO", "BBDC4.SA": "BRADESCO", "BRAP4.SA": "BRADESPAR", "BBAS3.SA": "BRASIL", "BRKM5.SA": "BRASKEM", "BRFS3.SA": "BRF SA", "BPAC11.SA": "BTGP BANCO", "CRFB3.SA": "CARREFOUR BR", "CCRO3.SA": "CCR SA", "CMIG4.SA": "CEMIG", "CIEL3.SA": "CIELO", "COGN3.SA": "COGNA ON", "CPLE6.SA": "COPEL", "CSAN3.SA": "COSAN", "CPFE3.SA": "CPFL ENERGIA", "CMIN3.SA": "CSNMINERACAO", "CVCB3.SA": "CVC BRASIL", "CYRE3.SA": "CYRELA REALT", "DXCO3.SA": "DEXCO", "ELET3.SA": "ELETROBRAS", "ELET6.SA": "ELETROBRAS", "EMBR3.SA": "EMBRAER", "ENBR3.SA": "ENERGIAS BR", "ENGI11.SA": "ENERGISA", "ENEV3.SA": "ENEVA", "EGIE3.SA": "ENGIE BRASIL", "EQTL3.SA": "EQUATORIAL", "EZTC3.SA": "EZTEC", "FLRY3.SA": "FLEURY", "GGBR4.SA": "GERDAU", "GOAU4.SA": "GERDAU MET", "GOLL4.SA": "GOL", "NTCO3.SA": "GRUPO NATURA", "SOMA3.SA": "GRUPO SOMA", "HAPV3.SA": "HAPVIDA", "HYPE3.SA": "HYPERA", "IGTI11.SA": "IGUATEMI S.A", "IRBR3.SA": "IRBBRASIL RE", "ITSA4.SA": "ITAUSA", "ITUB4.SA": "ITAUUNIBANCO", "JBSS3.SA": "JBS", "KLBN11.SA": "KLABIN S/A", "RENT3.SA": "LOCALIZA", "LWSA3.SA": "LOCAWEB", "LREN3.SA": "LOJAS RENNER", "MGLU3.SA": "MAGAZ LUIZA", "MRFG3.SA": "MARFRIG", "CASH3.SA": "MELIUZ", "BEEF3.SA": "MINERVA", "MRVE3.SA": "MRV", "MULT3.SA": "MULTIPLAN", "PCAR3.SA": "P.ACUCAR-CBD", "PETR3.SA": "PETROBRAS", "PETR4.SA": "PETROBRAS", "PRIO3.SA": "PETRORIO", "PETZ3.SA": "PETZ", "RADL3.SA": "RAIADROGASIL", "RAIZ4.SA": "RAIZEN", "RDOR3.SA": "REDE D OR", "RAIL3.SA": "RUMO S.A.", "SBSP3.SA": "SABESP", "SANB11.SA": "SANTANDER BR", "SMTO3.SA": "SAO MARTINHO", "CSNA3.SA": "SID NACIONAL", "SLCE3.SA": "SLC AGRICOLA", "SUZB3.SA": "SUZANO S.A.", "TAEE11.SA": "TAESA", "VIVT3.SA": "TELEF BRASIL", "TIMS3.SA": "TIM", "TOTS3.SA": "TOTVS", "UGPA3.SA": "ULTRAPAR", "USIM5.SA": "USIMINAS", "VALE3.SA": "VALE", "VIIA3.SA": "VIA", "VBBR3.SA": "VIBRA", "WEGE3.SA": "WEG", "YDUQ3.SA": "YDUQS PART"}

    data = yf.download(list(indices_ibov.keys()), start='2023-05-01', end='2023-05-12')['Close']

    daily_returns = data.pct_change() * 100

    # Positivos

    # Contagem de positivos por dia
    positive_counts = (daily_returns >= 0).sum(axis=1)

    # Aumentar a largura da imagem
    fig_positive_ibov = plt.figure(figsize=(24, 6))
    fig_positive_ibov.patch.set_facecolor('#2c2c32')

    ax_positive = plt.axes()

    ax_positive.set_facecolor('#2c2c32')

    # Plotagem do gráfico em linha
    plt.plot(positive_counts.index, positive_counts, label='Positivos', color='#34A69D')

    plt.xlabel('Data')
    plt.ylabel('Contagem')

    st.markdown("<span style='color: #34A69D'>Positivos</span>",
             unsafe_allow_html=True)
    st.pyplot(fig_positive_ibov)

    # Negativos

    # Contagem de negativos por dia
    negative_counts = (daily_returns < 0).sum(axis=1)

    # Aumentar a largura da imagem
    fig_negative_ibov = plt.figure(figsize=(24, 6))
    fig_negative_ibov.patch.set_facecolor('#2c2c32')

    ax_negative = plt.axes()

    ax_negative.set_facecolor('#2c2c32')

    # Plotagem do gráfico em linha
    plt.plot(negative_counts.index, negative_counts, label='Negativos', color='#ce1c5b')

    plt.xlabel('Data')
    plt.ylabel('Contagem')

    st.markdown("<span style='color: #ce1c5b'>Negativos</span>",
             unsafe_allow_html=True)
    st.pyplot(fig_negative_ibov)

   