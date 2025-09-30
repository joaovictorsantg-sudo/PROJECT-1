import pandas as pd
import sqlite3
import os
import glob
import shutil

DB_FILE = 'qualidade.db'
INPUT_FOLDER = 'input'
PROCESSED_FOLDER = 'processed'
ERROR_FOLDER = 'error'

def limpar_nome_colunas(df):
    """
    Remove espaços extras e caracteres especiais dos nomes das colunas.
    """
    df.columns = (
        df.columns.str.strip()
        .str.replace(' ', '_')
        .str.replace(r'[^\w_]', '', regex=True)
        .str.lower()
    )
    return df

def processar_planilhas_excel():
    print("--- Iniciando pipeline universal de dados ---")
    
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(ERROR_FOLDER, exist_ok=True)

    caminho_dos_arquivos = os.path.join(INPUT_FOLDER, '*.xlsx')
    arquivos_para_processar = glob.glob(caminho_dos_arquivos)

    if not arquivos_para_processar:
        print("Nenhum arquivo novo para processar.")
        return

    print(f"Encontrados {len(arquivos_para_processar)} arquivos para processar.")

    for arquivo in arquivos_para_processar:
        try:
            print(f"\nProcessando arquivo: {arquivo}...")
            df = pd.read_excel(arquivo)
            print("Dados lidos com sucesso. Colunas encontradas:", list(df.columns))
            df = limpar_nome_colunas(df)
            print("Nomes das colunas padronizados:", list(df.columns))
            nome_da_tabela = os.path.splitext(os.path.basename(arquivo))[0].lower()
            print(f"Conectando ao banco de dados e salvando na tabela '{nome_da_tabela}'...")
            with sqlite3.connect(DB_FILE) as conexao:
                df.to_sql(nome_da_tabela, conexao, if_exists='replace', index=False)
            print(f"Dados do arquivo '{arquivo}' carregados com sucesso.")

            
            caminho_exportacao = os.path.join(INPUT_FOLDER, f"{nome_da_tabela}_para_bi.csv")
            df.to_csv(caminho_exportacao, index=False)
            print(f"Arquivo de exportação '{caminho_exportacao}' criado para o Power BI.")

            shutil.move(arquivo, os.path.join(PROCESSED_FOLDER, os.path.basename(arquivo)))
            print(f"Arquivo '{os.path.basename(arquivo)}' movido para a pasta de processados.")
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo {arquivo}: {e}")
            shutil.move(arquivo, os.path.join(ERROR_FOLDER, os.path.basename(arquivo)))
            print(f"Arquivo '{os.path.basename(arquivo)}' movido para a pasta de erro.")

    print("\n--- Pipeline concluído ---")

if __name__ == "__main__":
    processar_planilhas_excel()