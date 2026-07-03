#       streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import re
from datetime import datetime
import time

# 1. Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard de Consultoria", page_icon="📊", layout="wide")

# 2. Função para carregar e limpar dados
@st.cache_data(ttl=60)
def load_data():
    # URL de exportação do Google Sheets em formato CSV
    sheet_url = "https://docs.google.com/spreadsheets/d/1tLg2QDEJMcRJT3a8q6jVkJWbYiNHK3tZmJhf8V-rIKs/export?format=csv&gid=1267934545"
    
    df = pd.read_csv(sheet_url)
    
    # Renomear as colunas para facilitar
    col_mapping = {
        'Carimbo de data/hora': 'Timestamp',
        'Data': 'Data',
        'Seu nome aqui !': 'Cliente',
        'Por qual consultor você foi atendido?': 'Consultor',
        'Qual foi o principal objetivo da consultoria?': 'Objetivo',
        'Em uma escala de 1 a 10, quão satisfeito(a) você ficou com a experiência geral da consultoria de hoje?': 'Satisfacao_Geral',
        'Avalie a performance do consultor nos seguintes aspectos: [Conhecimento Técnico e Expertise]': 'Aval_Tecnica',
        'Avalie a performance do consultor nos seguintes aspectos: [Capacidade de Entender as Necessidades do Negócio]': 'Aval_Negocio',
        'Avalie a performance do consultor nos seguintes aspectos: [Proatividade e Sugestão de Soluções Relevantes]': 'Aval_Proatividade',
        'Com que frequência você recomendaria este consultor a outras empresas?': 'Recomendacao',
        'Se houver, quais são as sugestões de melhoria para futuras consultorias?': 'Sugestoes'
    }
    df.rename(columns=col_mapping, inplace=True)
    
    # Função para transformar textos e números misturados em notas reais
    def tratar_nota(valor):
        if pd.isna(valor):
            return None
            
        valor_str = str(valor).lower().strip()
        
        # 1. Primeiro tenta achar algum número na resposta (Ex: "5 - Muito satisfeito" vira 5)
        numeros = re.findall(r'\d+', valor_str)
        if numeros:
            return float(numeros[0])
            
        # 2. Se for só texto, traduz para notas (ajuste as palavras se seu forms for diferente)
        if any(palavra in valor_str for palavra in ['excelente', 'ótimo', 'otimo', 'muito bom', 'concordo totalmente']):
            return 5.0
        if any(palavra in valor_str for palavra in ['bom', 'concordo']):
            return 4.0
        if any(palavra in valor_str for palavra in ['regular', 'neutro', 'médio', 'aceitável']):
            return 3.0
        if any(palavra in valor_str for palavra in ['ruim', 'discordo']):
            return 2.0
        if any(palavra in valor_str for palavra in ['péssimo', 'pessimo', 'muito ruim', 'discordo totalmente']):
            return 1.0
            
        return None # Se não achar nada, deixa vazio
        
    # Aplica a função de limpeza nas colunas de avaliação
    cols_numericas = ['Satisfacao_Geral', 'Aval_Tecnica', 'Aval_Negocio', 'Aval_Proatividade']
    for col in cols_numericas:
        df[col] = df[col].apply(tratar_nota)
        
    return df

# Carregar os dados
df = load_data()

# 3. Interface do Dashboard
st.title("📊 Dashboard de Avaliação de Consultorias")
st.markdown("Acompanhamento das respostas de satisfação e performance dos consultores.")
hora_atualizacao = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
st.caption(f"Última atualização dos dados: {hora_atualizacao}")

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros")
consultores = df['Consultor'].dropna().unique()
consultor_selecionado = st.sidebar.multiselect(
    "Selecione o(s) Consultor(es)", 
    options=consultores, 
    default=consultores
)

# Filtrar o dataframe
df_filtrado = df[df['Consultor'].isin(consultor_selecionado)]

# --- KPIs PRINCIPAIS ---
if not df_filtrado.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Consultorias", len(df_filtrado))
    with col2:
        media_satisfacao = df_filtrado['Satisfacao_Geral'].mean()
        st.metric("Média de Satisfação", f"{media_satisfacao:.1f}" if pd.notna(media_satisfacao) else "-")
    with col3:
        media_tecnica = df_filtrado['Aval_Tecnica'].mean()
        st.metric("Conhecimento Técnico", f"{media_tecnica:.1f}" if pd.notna(media_tecnica) else "-")
    with col4:
        media_proat = df_filtrado['Aval_Proatividade'].mean()
        st.metric("Proatividade", f"{media_proat:.1f}" if pd.notna(media_proat) else "-")

    st.markdown("---")

    # --- GRÁFICOS ---
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Volume de Atendimentos por Consultor")
        contagem = df_filtrado['Consultor'].value_counts().reset_index()
        contagem.columns = ['Consultor', 'Atendimentos']
        fig1 = px.bar(contagem, x='Consultor', y='Atendimentos', color='Consultor', text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col_graf2:
        st.subheader("Principais Objetivos da Consultoria")
        fig2 = px.pie(df_filtrado, names='Objetivo', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.subheader("Performance Média por Consultor")
    
    # Preparar dados para o gráfico de performance
    df_performance = df_filtrado.groupby('Consultor')[['Aval_Tecnica', 'Aval_Negocio', 'Aval_Proatividade']].mean().reset_index()
    
    # Remover linhas onde todas as notas são NaN (para evitar que o gráfico quebre)
    df_performance = df_performance.dropna(subset=['Aval_Tecnica', 'Aval_Negocio', 'Aval_Proatividade'], how='all')
    
    if not df_performance.empty:
        fig3 = px.bar(
            df_performance, 
            x='Consultor', 
            y=['Aval_Tecnica', 'Aval_Negocio', 'Aval_Proatividade'],
            barmode='group',
            labels={'value': 'Nota Média', 'variable': 'Habilidade', 'Consultor': 'Consultor'},
            title="Comparativo de Habilidades (Médias)"
        )
        # Ajusta nomes da legenda
        novos_nomes = {
            'Aval_Tecnica': 'Conhecimento Técnico',
            'Aval_Negocio': 'Visão de Negócio',
            'Aval_Proatividade': 'Proatividade'
        }
        fig3.for_each_trace(lambda t: t.update(name = novos_nomes.get(t.name, t.name)))
        
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Não há notas numéricas suficientes para gerar o gráfico de performance.")

    # --- TABELA DE SUGESTÕES ---
    st.markdown("---")
    st.subheader("Sugestões de Melhoria")
    
    sugestoes = df_filtrado[['Data', 'Consultor', 'Cliente', 'Sugestoes']].dropna(subset=['Sugestoes'])
    sugestoes = sugestoes[sugestoes['Sugestoes'].str.strip() != '']
    
    if not sugestoes.empty:
        st.dataframe(sugestoes, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma sugestão de melhoria registrada.")

else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

# --- ATUALIZAÇÃO AUTOMÁTICA ---
time.sleep(60) # Espera 60 segundos
st.rerun()     # Recarrega a página inteira