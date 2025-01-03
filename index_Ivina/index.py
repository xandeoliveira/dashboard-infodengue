import streamlit as st
import pandas as pd
import numpy as np
import locale

# Configura o local para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.sidebar.title("Infodengue")  
city = st.sidebar.selectbox("", ["Página Inicial", "Acarape", "Redenção"])

if city == "Página Inicial":
    st.title("Infodengue Acarape e Redenção")
    info, image = st.columns([1, 1])
    st.info("Dashboard para visualização dos dados de dengue nas cidades de Acarape e Redenção.")
    # with image:
    # st.image("C:\\Users\\Ivina\\Desktop\\LTSM-bolsa\\images\\Data analysis-rafiki.png", width=300)

if city == "Acarape":
    data_acarape = pd.read_csv("acarape_sorted.csv")
    #data_acarape['data'] = pd.to_datetime(data_acarape['data'])  # Converter coluna 'data' para datetime
    st.write(f"Você selecionou: {city}")
    st.divider()
    anos = data_acarape['Ano'].unique()
    meses = range(1, 13)
    
    # Selecionar ano e mês
    ano_selecionado = st.selectbox("Ano", anos)
    mes_selecionado = st.selectbox(
        "Mês",
        meses,
        format_func=lambda x: pd.Timestamp(f"2024-{x:02d}-01").strftime('%B')  # Mostra nome do mês
    )
    st.divider()
    
    # Filtrar os dados com base no ano e mês selecionados
    dados_filtrados = data_acarape[
        (data_acarape['Ano'] == ano_selecionado) & (data_acarape['Mês'] == mes_selecionado)
    ]

    if not dados_filtrados.empty:
        st.write("Dados encontrados:")
        st.dataframe(dados_filtrados)  # Exibe os dados filtrados
    else:
        st.write("Nenhum dado encontrado para o ano e mês selecionados.")
    

if city == "Redenção":
    data_redencao = pd.read_csv("C:\\Users\\Ivina\\Desktop\\LTSM-bolsa\\redenção_sorted.csv") 
    
    st.write(f"Você selecionou: {city}")
    #st.text("Defina a série temporal:")
    st.divider()
    anos = data_redencao['Ano'].unique()
    meses = range(1, 13)
    
    # Selecionar ano e mês
    ano_selecionado = st.selectbox("Ano", anos)
    mes_selecionado = st.selectbox(
        "Mês",
        meses,
        format_func=lambda x: pd.Timestamp(f"2024-{x:02d}-01").strftime('%B')  # Mostra nome do mês
    )
    st.divider()
    
    # Filtrar os dados com base no ano e mês selecionados
    dados_filtrados = data_redencao[
        (data_redencao['Ano'] == ano_selecionado) & (data_redencao['Mês'] == mes_selecionado)
    ]

    if not dados_filtrados.empty:
        st.write("Dados encontrados:")
        st.dataframe(dados_filtrados)  # Exibe os dados filtrados
    else:
        st.write("Nenhum dado encontrado para o ano e mês selecionados.")
    
    
