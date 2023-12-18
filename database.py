import os
import pandas as pd

def calcular_media_diaria_por_hora(arquivo):

    # Obtém o caminho do diretório atual
    caminho_atual = os.getcwd()

    # Junta o caminho do diretório atual com o nome do arquivo
    caminho_arquivo = os.path.join(caminho_atual, arquivo)

    # Carregar o arquivo CSV em um DataFrame
    df = pd.read_csv(caminho_arquivo)
    df['hora'] = df['Time stamp'] % 24
    df['temperatura'] = df['Subarray 1 Cell temperature | (C)']
    media_diaria_por_hora = df.groupby(['hora'])['temperatura'].mean()

    # Resetar o índice para obter um DataFrame com as colunas 'hora' e 'temperatura'
    media_diaria_por_hora = media_diaria_por_hora.reset_index()

    # Exibir a média diária por hora
    return(media_diaria_por_hora)
