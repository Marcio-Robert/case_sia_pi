# Bibliotecas
import streamlit as st
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
from nltk.corpus import stopwords

# --- DOWNLOAD DAS STOPWORDS (só acontece na primeira vez) ---
try:
    stopwords.words('portuguese')
except LookupError:
    st.info("Baixando recursos de linguagem necessários (stopwords). Isso só acontece uma vez.")
    nltk.download('stopwords')

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Monitor de Percepção sobre IA no Piauí",
    page_icon="🤖",
    layout="wide"
)

# --- FUNÇÕES ---

# Carregar os dados


@st.cache_data
def carregar_dados(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo)
        return df
    except FileNotFoundError:
        st.error(
            f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado. Execute o script 'coleta_noticias.py' primeiro.")
        return None

# Limpar textos simples


def limpar_texto(texto):
    # Pegando a lista nltk
    stopwords_pt = stopwords.words('portuguese')
    # Adicionando palavras sem valor
    stopwords_pt.extend(['piauí', 'teresina', 'marcio',
                        'robert', 'sobre', 'terá', 'ainda', 'diz'])

    texto = texto.lower()
    texto = re.sub(r'[^a-zA-Z\s]', '', texto)
    palavras = [palavra for palavra in texto.split()
                if palavra not in stopwords_pt]
    return " ".join(palavras)

# Analisar sentimento baseado em regras


def analisar_sentimento(texto, palavras_positivas, palavras_negativas):
    score = 0
    palavras = texto.split()
    for palavra in palavras:
        if palavra in palavras_positivas:
            score += 1
        elif palavra in palavras_negativas:
            score -= 1

    if score > 0:
        return 'Positivo'
    elif score < 0:
        return 'Negativo'
    else:
        return 'Neutro'

# --- LÓGICA PRINCIPAL DO DASHBOARD ---


# Título
st.title("🤖 Monitor de Percepção Pública sobre IA no Piauí")
st.markdown("Dashboard simplificado para monitorar menções sobre 'Inteligência Artificial no Piauí' em fontes de notícias públicas.")

# Carregando dados
df_noticias = carregar_dados('noticias.csv')

if df_noticias is not None:
    # Processamento do case
    # Limpando os títulos para análise
    df_noticias['titulo_limpo'] = df_noticias['titulo'].apply(limpar_texto)

    # Criando listas de palavras para análise de sentimento
    palavras_positivas = [
        'avanço', 'crescimento', 'inova', 'desenvolvimento', 'oportunidade', 'melhora', 'beneficia', 'investimento',
        'solução', 'positivo', 'expansão', 'parceria', 'fortalece', 'impulso', 'moderniza', 'otimiza', 'eficiência',
        'qualidade', 'aprimora', 'incentivo', 'fomento', 'sucesso', 'destaque', 'potencial'
    ]
    palavras_negativas = [
        'risco', 'perigo', 'problema', 'desemprego', 'crise', 'ameaça', 'negativo', 'corte', 'dificuldade',
        'preocupação', 'alerta', 'impacto', 'desafio', 'fraude', 'golpe', 'ilegal', 'atraso', 'falha', 'insegurança',
        'vulnerabilidade', 'prejuízo', 'polêmica'
    ]
    # Aplicando a análise de sentimento
    df_noticias['sentimento'] = df_noticias['titulo_limpo'].apply(
        lambda texto: analisar_sentimento(texto, palavras_positivas, palavras_negativas))

    # --- Visualização do case ---
    st.header("Análise de Sentimento das Notícias")

    # Layout em duas colunas para os gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de Pizza com a distribuição de sentimentos
        sentimento_counts = df_noticias['sentimento'].value_counts()
        fig_pie = px.pie(
            sentimento_counts,
            values=sentimento_counts.values,
            names=sentimento_counts.index,
            title="Distribuição de Sentimentos",
            color=sentimento_counts.index,
            color_discrete_map={'Positivo': 'green',
                                'Negativo': 'red', 'Neutro': 'blue'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Nuvem de palavras com os termos mais frequentes
        st.subheader("Nuvem de Palavras-Chave")
        texto_completo = " ".join(
            titulo for titulo in df_noticias['titulo_limpo'])

        # Gerar a nuvem de palavras se houver texto
        if texto_completo.strip():
            wordcloud = WordCloud(
                background_color="white",
                width=800,
                height=400,
                colormap='viridis',
                max_words=100
            ).generate(texto_completo)

            fig_wc, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig_wc)
        else:
            st.write("Não há texto suficiente para gerar a nuvem de palavras.")

    # Tabela interativa com os dados coletados e classificados
    st.header("Detalhes das Notícias Coletadas")
    st.dataframe(
        df_noticias[['titulo', 'sentimento', 'link', 'descricao']],
        column_config={
            "link": st.column_config.LinkColumn(
                "Link da Notícia",
                help="Clique para abrir a notícia original em uma nova aba"
            )
        },
        hide_index=True
    )
    # --- Ética e Transparência do case ---
    st.markdown("---")
    st.caption("Esta análise de sentimento é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos. O objetivo é oferecer uma visão geral e automatizada da percepção pública.")
