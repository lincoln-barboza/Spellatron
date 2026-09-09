import streamlit as st
import pandas as pd
from gtts import gTTS
import os

# Configuração da página
st.set_page_config(page_title="Spelling Bee - Julia", page_icon="🐝")

st.title("🐝 Concurso de Soletração - Treino da Julia")

# Carregar a planilha pulando a linha do título (linha 0) para pegar os cabeçalhos corretos
@st.cache_data
def load_data():
    df = pd.read_excel(
        "Palavras_Soletracao_Julia_4Ano.xlsx", 
        sheet_name="Lista de Palavras", 
        header=1 # Força o pandas a pegar a 2ª linha como cabeçalho das colunas
    )
    # Limpa possíveis espaços extras nos nomes das colunas
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # Filtros na Barra Lateral
    st.sidebar.header("Filtros do Sorteio")
    categorias = st.sidebar.multiselect(
        "Filtrar por Categoria:",
        options=df["Categoria"].unique(),
        default=df["Categoria"].unique()
    )

    dificuldade = st.sidebar.multiselect(
        "Filtrar por Dificuldade:",
        options=df["Dificuldade"].unique(),
        default=df["Dificuldade"].unique()
    )

    # Filtrar dados
    df_filtered = df[(df["Categoria"].isin(categorias)) & (df["Dificuldade"].isin(dificuldade))]

    if df_filtered.empty:
        st.warning("Nenhuma palavra encontrada com os filtros selecionados.")
    else:
        # Estado da sessão para guardar a palavra sorteada
        if "current_word" not in st.session_state:
            st.session_state.current_word = None

        if st.button("🎲 Sortear Nova Palavra") or st.session_state.current_word is None:
            st.session_state.current_word = df_filtered.sample(1).iloc[0]

        word_data = st.session_state.current_word

        st.subheader(f"Categoria: {word_data['Categoria']} | Dificuldade: {word_data['Dificuldade']}")

        # Gerar e tocar áudio da palavra em Inglês
        tts = gTTS(text=str(word_data['Palavra (Inglês)']), lang='en', slow=False)
        tts.save("temp_word.mp3")
        st.audio("temp_word.mp3")

        st.write(f"**Tradução / Significado:** {word_data['Tradução (Português)']}")

        # Esconder/Mostrar a resposta em inglês
        if st.checkbox("Revelar Palavra e Dica de Soletração"):
            st.markdown(f"### 🔤 **{word_data['Palavra (Inglês)']}**")
            st.info(f"💡 **Dica:** {word_data['Dica de Soletração']}")

except Exception as e:
    st.error(f"Ocorreu um erro: {e}")