import pandas as pd
import os
import shutil
import glob

PROCESSED_FOLDER = 'processed'
ERROR_FOLDER = 'error'
ARQUIVO_SAIDA_NOME = 'falhas_limpo_para_bi.csv'

# Lista das colunas que devem ser mantidas (em maiúsculo e sem espaços)
COLUNAS_MANTER = [
    'DESC_FALHA', 'DESC_LOCAL', 'DATA1', 'QUANTIDADE', 'KW', 'TURNO', 'CHASSI3', 'MODELO'
]

def encontrar_arquivo_mais_recente(pasta, padrao='*_para_bi.csv'):
    arquivos = glob.glob(os.path.join(pasta, padrao))
    if not arquivos:
        return None
    return max(arquivos, key=os.path.getctime)

def limpar_e_padronizar_colunas(df):
    df.columns = (
        df.columns.str.strip()
        .str.upper()
        .str.replace(' ', '_')
        .str.replace(r'[^\w_]', '', regex=True)
    )
    return df

def tratar_colunas_texto(df, colunas):
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = (
                df[coluna]
                .astype(str)
                .str.strip()
                .str.title()
                .replace('nan', 'N/A')
                .fillna('N/A')
            )
    return df

def processar_dados_qualidade_final():
    arquivo_entrada_path = encontrar_arquivo_mais_recente(PROCESSED_FOLDER, '*_para_bi.csv')
    if not arquivo_entrada_path:
        print(f"ERRO: Nenhum arquivo *_para_bi.csv encontrado na pasta '{PROCESSED_FOLDER}'.")
        return

    arquivo_saida_path = os.path.join(PROCESSED_FOLDER, ARQUIVO_SAIDA_NOME)
    print(f"--- Iniciando processamento do arquivo: {arquivo_entrada_path} ---")

    try:
        os.makedirs(PROCESSED_FOLDER, exist_ok=True)
        os.makedirs(ERROR_FOLDER, exist_ok=True)

        df = pd.read_csv(arquivo_entrada_path, encoding='latin1')
        print("Arquivo lido com sucesso.")

        df = limpar_e_padronizar_colunas(df)

        # Mantém apenas as colunas desejadas
        colunas_existentes = [col for col in COLUNAS_MANTER if col in df.columns]
        df = df[colunas_existentes]

        if 'DATA1' in df.columns:
            df['DATA1'] = pd.to_datetime(df['DATA1'], errors='coerce')

        print("Limpeza e padronização dos dados concluídas.")

        df.to_csv(arquivo_saida_path, index=False)
        print(f"\n--- Processamento concluído! ---")
        print(f"Arquivo limpo e pronto para análise salvo em: {arquivo_saida_path}")

        shutil.move(arquivo_entrada_path, os.path.join(PROCESSED_FOLDER, os.path.basename(arquivo_entrada_path)))
        print(f"Arquivo bruto '{os.path.basename(arquivo_entrada_path)}' movido para a pasta '{PROCESSED_FOLDER}'.")

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{arquivo_entrada_path}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        if arquivo_entrada_path and os.path.exists(arquivo_entrada_path):
            shutil.move(arquivo_entrada_path, os.path.join(ERROR_FOLDER, os.path.basename(arquivo_entrada_path)))
            print(f"Arquivo bruto '{os.path.basename(arquivo_entrada_path)}' movido para a pasta de erro para análise.")

if __name__ == "__main__":
    processar_dados_qualidade_final()