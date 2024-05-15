import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap

import pandas as pd
import altair as alt
import calendar

meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

@st.cache_resource
def loadData(servico):
    if servico == "Celulares Subtraídos":
        return pd.read_csv("./data/CelularesSubtraidos_2023.csv", sep="|", low_memory=False)
    elif servico == "Veículos Subtraídos":
        return pd.read_csv("./data/VeiculosSubtraidos_2023.csv", sep="|", low_memory=False)
    else:
        return None
    
def getFiltroPorCidade(data, cidade):
    return data[(data["CIDADE"] == cidade) & (~data["LATITUDE"].isnull()) & (~data["LONGITUDE"].isnull())]

def getBairros(data, cidade):
    bairros = data[data["CIDADE"] == cidade]["BAIRRO"].dropna().astype(str).unique()
    bairros = sorted(bairros)
    bairros.insert(0, "Todos")  # Adicionando a opção "Todos" no início da lista
    return bairros

def build_sidebar():

    servico = None
    cidade = None
    bairro = None
    filtered_data = None

    st.image("./images/Logo_SSP.png")
    servico = st.sidebar.selectbox("Selecione o serviço:", ["Veículos Subtraídos","Celulares Subtraídos"])

    if servico:
        data = loadData(servico)
        
        cidade = st.sidebar.selectbox("Selecione a cidade:", data["CIDADE"].unique())

        if cidade:
            
            bairros = getBairros(data=data, cidade=cidade)
            bairro = st.sidebar.selectbox("Selecione o bairro:", bairros)

            filtered_data = getFiltroPorCidade(data, cidade)

            if bairro and bairro != "Todos":
                filtered_data = filtered_data[filtered_data["BAIRRO"] == bairro]

    return servico, cidade, bairro, filtered_data


def build_main(servico, cidade, bairro, filtered_data):

    with st.spinner("Carregando..."):

        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.markdown("Mapa de calor das ocorrências")
            m = folium.Map(location=[-23.55, -46.63], zoom_start=10)
            HeatMap(data=[[row['LATITUDE'], row['LONGITUDE']] for index, row in filtered_data.iterrows()], radius=10).add_to(m)
            folium_static(m)

        with col2:
            st.markdown("Evolução das ocorrências ao longo do ano")

            monthly_counts = filtered_data.groupby("MES").size()
            monthly_counts = monthly_counts.reset_index().rename(columns={"MES": "Mês", 0: "Quantidade"})
            monthly_counts = monthly_counts.sort_values(by='Mês')            
            monthly_counts["Display"] = monthly_counts['Mês'].map(meses)

            chart = alt.Chart(monthly_counts).mark_bar().encode(
                x=alt.X('Display', title='Mês',sort=list(meses.values())),
                y=alt.Y('Quantidade', title='Quantidade')
            ).properties(width=680, height=550)
            st.altair_chart(chart)
        

        col21, col22 = st.columns(2, gap='large')
        with col21:

            if bairro == "Todos":
                st.write("Bairros com maior número de ocorrências")
                ocorrenciasPorBairro = filtered_data["BAIRRO"].value_counts().reset_index().rename(columns={"BAIRRO": "Bairro", "count": "Quantidade"})
                st.dataframe(ocorrenciasPorBairro,hide_index=True,use_container_width=True)
            else:
                st.write(f"Endereços com maiores ocorrências no bairro {bairro}")
                ocorrenciasPorLogradouro = filtered_data["LOGRADOURO"].value_counts().reset_index().rename(columns={"LOGRADOURO": "Logradouro", "count": "Quantidade"})
                st.dataframe(ocorrenciasPorLogradouro,hide_index=True,use_container_width=True)

        with col22:
            if servico == "Veículos Subtraídos":
                st.markdown("Automóveis mais subtraídos")
                veículosMaisRoubados = filtered_data["DESCR_MARCA_VEICULO"].value_counts().nlargest(15).reset_index()
                veículosMaisRoubados.columns = ["Marca/Modelo", "Qtde"]
                st.dataframe(veículosMaisRoubados,hide_index=True,use_container_width=True)

            elif servico == "Celulares Subtraídos":
                st.markdown("Celulares mais subtraídos")
                celularesMaisRoubados = filtered_data["MARCA_OBJETO"].value_counts().nlargest(15).reset_index()
                celularesMaisRoubados.columns = ["Aparelho/Modelo", "Qtde"]
                st.dataframe(celularesMaisRoubados,hide_index=True,use_container_width=True)


st.set_page_config(layout="wide")

with st.sidebar:
    servico, cidade, bairro, filtered_data = build_sidebar()

st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.header("Ocorrências 2023 - Secretaria de Segurança Pública de São Paulo")

if filtered_data is not None:
    build_main(servico, cidade, bairro, filtered_data)