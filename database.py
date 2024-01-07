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
    df['temperatura'] = df['Subarray 1 Cell temperature (steady state) | (C)']
    media_diaria_por_hora = df.groupby(['hora'])['temperatura'].mean()

    # Resetar o índice para obter um DataFrame com as colunas 'hora' e 'temperatura'
    media_diaria_por_hora = media_diaria_por_hora.reset_index()
    temperatura = media_diaria_por_hora['temperatura'].round(2)
    resultado = ' '.join(map(str, temperatura.to_numpy().tolist()))


    # Exibir a média diária por hora
    return "temp = ("+ resultado + ")"

def calcular_potencia_diaria_por_hora(arquivo):

    # Obtém o caminho do diretório atual
    caminho_atual = os.getcwd()

    # Junta o caminho do diretório atual com o nome do arquivo
    caminho_arquivo = os.path.join(caminho_atual, arquivo)

    # Carregar o arquivo CSV em um DataFrame
    df = pd.read_csv(caminho_arquivo)
    df['hora'] = df['Time stamp'] % 24
    df['potencia'] = df['System power generated | (kW)']
    media_diaria_por_hora = df.groupby(['hora'])['potencia'].mean()

    # Resetar o índice para obter um DataFrame com as colunas 'hora' e 'temperatura'
    media_diaria_por_hora = media_diaria_por_hora.reset_index()
    potencia = media_diaria_por_hora['potencia'].round(2)
    resultado = ' '.join(map(str, potencia.to_numpy().tolist()))


    # Exibir a média diária por hora
    return "pot = ("+ resultado + ")"

def calcular_irradiancia_diaria_por_hora(arquivo):

    # Obtém o caminho do diretório atual
    caminho_atual = os.getcwd()

    # Junta o caminho do diretório atual com o nome do arquivo
    caminho_arquivo = os.path.join(caminho_atual, arquivo)

    # Carregar o arquivo CSV em um DataFrame
    df = pd.read_csv(caminho_arquivo)
    df['hora'] = df['Time stamp'] % 24
    df['irradiancia'] = df['Array POA front-side total radiation nominal | (kW)']
    media_diaria_por_hora = df.groupby(['hora'])['irradiancia'].mean()

    # Resetar o índice para obter um DataFrame com as colunas 'hora' e 'temperatura'
    media_diaria_por_hora = media_diaria_por_hora.reset_index()
    irradiancia = media_diaria_por_hora['irradiancia'].round(2)
    resultado = ' '.join(map(str, irradiancia.to_numpy().tolist()))


    # Exibir a média diária por hora
    return "irrad = ("+ resultado + ")"

a = calcular_irradiancia_diaria_por_hora('results.csv')
b = calcular_potencia_diaria_por_hora('results.csv')

print(a)
print(b)