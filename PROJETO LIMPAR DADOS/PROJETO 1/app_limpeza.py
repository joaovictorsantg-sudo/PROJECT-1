import streamlit as st
import pandas as pd

# --- Funções de Limpeza (as mesmas de antes) ---
def limpar_e_padronizar_colunas(df, maiusculo=False):
    df_copia = df.copy()
    if maiusculo:
        df_copia.columns = (
            df_copia.columns.str.strip()
            .str.upper()
            .str.replace(' ', '_')
            .str.replace(r'[^\w_]', '', regex=True)
        )
    else:
        df_copia.columns = (
            df_copia.columns.str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace(r'[^\w_]', '', regex=True)
        )
    return df_copia

def tratar_colunas_texto(df, colunas):
    df_copia = df.copy()
    for coluna in colunas:
        if coluna in df_copia.columns:
            df_copia[coluna] = (
                df_copia[coluna]
                .astype(str)
                .str.strip()
                .str.title()
                .replace('nan', 'N/A')
                .fillna('N/A')
            )
    return df_copia

# --- Configuração da Página ---
st.set_page_config(page_title="Ferramenta de Limpeza VW", page_icon="🧹", layout="wide")

# --- Interface do Usuário ---
st.title("🧹 Ferramenta de Limpeza e Preparação de Dados")
st.markdown("Faça o upload da sua planilha Excel para limpar e selecionar as colunas desejadas.")

# 1. Upload do Arquivo
st.sidebar.header("1. Carregue seu arquivo")
arquivo_carregado = st.sidebar.file_uploader("Selecione uma planilha Excel:", type=['xlsx'])

# --- Lógica Principal do App com Otimização ---
if arquivo_carregado is not None:
    try:
        # MUDANÇA 1: Usamos o session_state para guardar o DataFrame
        # Ele só vai ler o arquivo de novo se você carregar um novo arquivo.
        if 'df_bruto' not in st.session_state or st.session_state.nome_arquivo != arquivo_carregado.name:
            st.session_state.df_bruto = pd.read_excel(arquivo_carregado)
            st.session_state.nome_arquivo = arquivo_carregado.name
        df_bruto = st.session_state.df_bruto
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        st.stop()

    st.sidebar.success("Arquivo carregado com sucesso!")
    
    st.markdown("---")
    st.subheader("Pré-visualização dos Dados Brutos")
    st.dataframe(df_bruto.head())

    # 2. Seleção de Colunas (agora muito mais rápida)
    st.sidebar.header("2. Selecione as Colunas")
    st.sidebar.info("Selecione apenas as colunas que você deseja manter no arquivo final.")
    colunas_disponiveis = df_bruto.columns.tolist()
    colunas_selecionadas = st.sidebar.multiselect(
        "Escolha as colunas que você quer manter:",
        options=colunas_disponiveis,
        default=[]  # Nenhuma selecionada por padrão
    )

    maiusculo = st.sidebar.checkbox("Padronizar nomes das colunas em MAIÚSCULO", value=False)

    if colunas_selecionadas:
        df_filtrado = df_bruto[colunas_selecionadas]
        
        # 3. Processamento e Limpeza
        df_limpo = limpar_e_padronizar_colunas(df_filtrado, maiusculo=maiusculo)
        colunas_texto_selecionadas = [col for col in df_limpo.columns if df_limpo[col].dtype == 'object']
        df_limpo = tratar_colunas_texto(df_limpo, colunas_texto_selecionadas)

        st.markdown("---")
        st.subheader("Dados Limpos e Padronizados")
        st.dataframe(df_limpo)
        
        # 4. Download
        st.markdown("---")
        st.subheader("Baixe seus Dados Limpos")
        
        @st.cache_data
        def converter_df_para_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv_limpo = converter_df_para_csv(df_limpo)
        st.download_button(
            label="📥 Baixar como CSV",
            data=csv_limpo,
            file_name='dados_limpos.csv',
            mime='text/csv',
        )
    else:
        st.sidebar.warning("Por favor, selecione pelo menos uma coluna.")
else:
    st.info("Aguardando o upload de uma planilha Excel...")