import pandas as pd
import requests
import time
import os
from thefuzz import process
from tqdm import tqdm

BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros"

def get_json_blindado(url, tentativas_max=3):
    #
    # Tenta buscar. Se der erro 429, 
    # ele espera e tenta de novo. 
    #
    
    for i in range(tentativas_max):
        try:
            response = requests.get(url)
            
            
            if response.status_code == 429:
                tqdm.write(f"API pediu calma (429). Esperando {tempo_espera}s...")
                time.sleep(tempo_espera)
                tempo_espera *= 2 
                continue 
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            if i == tentativas_max - 1:
                tqdm.write(f"Erro fatal após tentativas: {e}")
                return None
            time.sleep(1)
            
    return None

def encontrar_match(nome_entrada, lista_candidatos):
    if not lista_candidatos: return None, 0
    
    nomes_api = [item['nome'] for item in lista_candidatos]
    melhor_match, score = process.extractOne(str(nome_entrada), nomes_api)
    
    for item in lista_candidatos:
        if item['nome'] == melhor_match:
            return item, score
    return None, 0

def processar_planilha(arquivo_entrada):
    print(f"\nIniciando Modo Blindado em: {arquivo_entrada}")

    try:
        df = pd.read_excel(arquivo_entrada)
    except Exception as e:
        print(f"Erro ao abrir arquivo: {e}")
        return
    
    res_fipe_nome = []
    res_valor = []
    res_codigo = []

    print("Baixando lista de marcas...")
    todas_marcas = get_json_blindado(f"{BASE_URL}/marcas")
    
    if not todas_marcas:
        print("Erro fatal: Não consegui baixar nem as marcas iniciais. API fora do ar?")
        return

    
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Consultando"):
        
        try:
            
            marca_match, _ = encontrar_match(row['Marca'], todas_marcas)
            if not marca_match: raise Exception("Marca não encontrada")
            id_marca = marca_match['codigo']

           
            dados_modelos = get_json_blindado(f"{BASE_URL}/marcas/{id_marca}/modelos")
            if not dados_modelos or 'modelos' not in dados_modelos:
                raise Exception("Falha ao buscar modelos")
                
            modelos_lista = dados_modelos['modelos']
            modelo_match, score_mod = encontrar_match(row['Modelo'], modelos_lista)
            if not modelo_match: raise Exception("Modelo não encontrado")
            
            id_modelo = modelo_match['codigo']
            nome_oficial = modelo_match['nome']

            
            anos_lista = get_json_blindado(f"{BASE_URL}/marcas/{id_marca}/modelos/{id_modelo}/anos")
            if not anos_lista: raise Exception("Falha ao buscar anos")
            
            ano_match, _ = encontrar_match(str(row['Ano_Modelo']), anos_lista)
            if not ano_match: raise Exception("Ano não encontrado")
            id_ano = ano_match['codigo']

            
            final = get_json_blindado(f"{BASE_URL}/marcas/{id_marca}/modelos/{id_modelo}/anos/{id_ano}")
            if not final: raise Exception("Falha ao pegar preço final")
            
            valor = final['Valor']
            codigo = final['CodigoFipe']
            
            
            res_fipe_nome.append(nome_oficial)
            res_valor.append(valor)
            res_codigo.append(codigo)

        except Exception as e:
            tqdm.write(f"Falha linha {index}: {e}") 
            res_fipe_nome.append("Erro/Não Encontrado")
            res_valor.append("R$ 0,00")
            res_codigo.append("-")
        
        
        time.sleep(1.0)

    
    df['FIPE_Modelo'] = res_fipe_nome
    df['FIPE_Codigo'] = res_codigo
    df['FIPE_Valor'] = res_valor
    
    arquivo_saida = "resultado_final_blindado.xlsx"
    df.to_excel(arquivo_saida, index=False)
    print(f"\nFinalizado! Se houve erros 429, o script esperou e continuou. Arquivo: {arquivo_saida}")

if __name__ == "__main__":
    arquivo = input("Digite o nome do arquivo (ex: carros_100_especificos.xlsx): ")
    if os.path.exists(arquivo):
        processar_planilha(arquivo)
    else:
        print("Arquivo não encontrado!")