import streamlit as st
from streamlit_folium import folium_static, st_folium
import folium
from folium.plugins import HeatMap

import plotly.express as px
import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent.absolute()

meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

dias = {0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'}

@st.cache_resource
def loadData(servico):
    if servico == "Celulares Subtraídos":
        return pd.read_csv(str(PATH) + "/data/CelularesSubtraidos.csv", sep=";", low_memory=False)
    elif servico == "Veículos Subtraídos":
        return pd.read_csv(str(PATH) +"/data/VeiculosSubtraidos.csv", sep=";", low_memory=False)
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
    
    st.image(str(PATH) + "/images/Logo_SSP.png")

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

    footer_html = """<div style='text-align: left;'>
                        <p>Developed with Streamlit <br>by Daniel Marques </p>
                    </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

    return servico, cidade, bairro, filtered_data


def build_main(servico, cidade, bairro, filtered_data):
    
    with st.spinner("Carregando..."):

        st.markdown("Mapa de calor das ocorrências")
        m = folium.Map(location=[-23.55, -46.63], zoom_start=10)
        HeatMap(data=[[row['LATITUDE'], row['LONGITUDE']] for index, row in filtered_data.iterrows()], radius=10).add_to(m)
        folium_static(m,width=900,height=500)

        col1, col2 = st.columns(2, gap='large')
        col3, col4 = st.columns(2, gap='large')

        filtered_data['DATA_OCORRENCIA_BO'] = pd.to_datetime(filtered_data['DATA_OCORRENCIA_BO'], format='%Y-%m-%d')
        filtered_data['HORA_OCORRENCIA'] = pd.to_datetime(filtered_data['HORA_OCORRENCIA'], format='%H:%M:%S')

        with col1:
            
            filtered_data['MES'] = filtered_data['DATA_OCORRENCIA_BO'].dt.month

            dfMes = filtered_data.groupby(['MES']).size().reset_index(name='Total')
            dfMes = dfMes.sort_values(by='MES')
            dfMes["Mês"] = dfMes['MES'].map(meses)
            
            fig_date = px.bar(dfMes, x="Mês",y="Total",text_auto='.2s',title="Ocorrências ao longo do ano")
            col1.plotly_chart(fig_date,use_container_width=True)

        with col2:
            
            filtered_data['DIA'] = filtered_data['DATA_OCORRENCIA_BO'].dt.dayofweek
            filtered_data['HORA'] = filtered_data['HORA_OCORRENCIA'].dt.hour

            dfDiaHora = filtered_data.groupby(['DIA','HORA']).size().reset_index(name='Total')
            dfDiaHora = dfDiaHora.sort_values(by=['DIA', 'HORA'])
            dfDiaHora = dfDiaHora.rename(columns={'HORA': 'Hora'})            
            dfDiaHora["Dia"] = dfDiaHora['DIA'].map(dias)

            fig_diahora = px.density_heatmap(dfDiaHora,x="Dia",y="Hora",z="Total",histfunc="sum", title="Dias e horários de maiores ocorrências")
            fig_diahora.layout['coloraxis']['colorbar']['title'] = 'Qtde'
            col2.plotly_chart(fig_diahora,use_container_width=True)

        with col3:
            if bairro == "Todos":                
                ocorrenciasPorBairro = filtered_data["BAIRRO"].value_counts().nlargest(15).reset_index().rename(columns={"BAIRRO": "Bairro", "count": "Qtde"})
                ocorrenciasPorBairro = ocorrenciasPorBairro.sort_values(by='Qtde', ascending=True)
                fig_ocorrenciasPorBairro = px.bar(ocorrenciasPorBairro, x="Qtde", y="Bairro", orientation='h',text_auto=True, title="Bairros com maior número de ocorrências")
                col3.plotly_chart(fig_ocorrenciasPorBairro,use_container_width=True)
                
            else:                
                ocorrenciasPorLogradouro = filtered_data["LOGRADOURO"].value_counts().nlargest(15).reset_index().rename(columns={"LOGRADOURO": "Logradouro", "count": "Qtde"})
                ocorrenciasPorLogradouro = ocorrenciasPorLogradouro.sort_values(by='Qtde', ascending=True)
                fig_ocorrenciasPorLogradouro = px.bar(ocorrenciasPorLogradouro, x="Qtde", y="Logradouro", orientation='h',text_auto=True, title="Logradouros com maior número de ocorrências")
                col3.plotly_chart(fig_ocorrenciasPorLogradouro,use_container_width=True)

        with col4:
            if servico == "Veículos Subtraídos":
                veículosSubtraidos = filtered_data["DESCR_MARCA_VEICULO"].value_counts().nlargest(15).reset_index().rename(columns={"DESCR_MARCA_VEICULO": "Marca/Modelo", "count": "Qtde"})                
                veículosSubtraidos = veículosSubtraidos.sort_values(by='Qtde', ascending=True)
                fig_veiculosSubtraidos = px.bar(veículosSubtraidos, x="Qtde", y="Marca/Modelo", orientation='h',text_auto=True, title="Veículos mais subtraídos")
                col4.plotly_chart(fig_veiculosSubtraidos,use_container_width=True)

            elif servico == "Celulares Subtraídos":
                celularesSubtraidos = filtered_data["MARCA_OBJETO"].value_counts().nlargest(15).reset_index().rename(columns={"MARCA_OBJETO": "Aparelho/Modelo", "count": "Qtde"})
                celularesSubtraidos = celularesSubtraidos.sort_values(by='Qtde', ascending=True)
                fig_celularesSubtraidos = px.bar(celularesSubtraidos, x="Qtde", y="Aparelho/Modelo", orientation='h',text_auto=True, title="Celulares mais subtraídos")
                col4.plotly_chart(fig_celularesSubtraidos,use_container_width=True)


st.set_page_config(layout="wide")

with st.sidebar:
    servico, cidade, bairro, filtered_data = build_sidebar()

st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.subheader("Ocorrências - Secretaria de Segurança Pública de São Paulo")

if filtered_data is not None:
    build_main(servico, cidade, bairro, filtered_data)