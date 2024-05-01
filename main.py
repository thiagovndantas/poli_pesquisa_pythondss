import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import py_dss_interface

from Parameters.parametersgen import create_circuit
from Parameters.parametersgen import create_file

analise = int(input("Qual será a análise?\n0 - Sem nada ou\n1 - Com pvsystem ou\n2 - Com pvsystem e baterias\nSua resposta: "))

# puxando o resultado, usando como input o número de simulações

resultados = []

simulator_path = os.path.join(os.path.dirname(__file__),"simulator")

def create_simulacoes(simulacoes,analise):
    for i in range(0,simulacoes):
        num_cargas = 100
        num_pvs = int(num_cargas/simulacoes*i) if analise != 0 else 0
        pmpp = 40
        num_baterias = int(num_cargas/simulacoes*i) if analise == 2 else 0
        bateria_kwnominal = 15
        bateria_kwhora = 60
        bateria_modo = "follow"

        # Criação do circuito
        files = create_circuit(num_cargas,num_pvs,pmpp,num_baterias,bateria_kwnominal,bateria_kwhora,bateria_modo)

        # Criando os files do circuito
        for name, parameters in files.items():
            create_file(os.path.join(simulator_path,name), parameters)

        # chamando o opendss
        dss = py_dss_interface.DSSDLL()

        dss_file5 = os.path.join(simulator_path,"simulacao5.dss")
        
        # rodando os arquivos
        dss.text("compile {}".format(dss_file5))

        # arquivos gerados pela compilação do código

        sim5_power_line = "fonte_Mon_monitor_power_line_sim5_1.csv"  # linha 1 terminal 2

        # criando os dataframes

        df_sim5_power_line = pd.read_csv(sim5_power_line,usecols=[2])

        resultados.append(df_sim5_power_line)

    return resultados

resultados = create_simulacoes(11,analise)

# resultados são criados em formado de vetor
resultados_combinados = pd.concat(resultados,axis=1)

# nomeando o número de concatenações
resultados_combinados.columns = [f'P1_{i} kW' for i in range(len(resultados_combinados.columns))]

# coluna de horas a partir do 0
resultados_combinados.insert(0, 'hour', range(1, len(resultados_combinados) + 1))

# Salvar os dados em um arquivo CSV
nome_arquivo_csv = f"Dados_Simulacao_{analise}.csv"
resultados_combinados.to_csv(nome_arquivo_csv, index=False)

# plotando o gráfico
num_cores = len(resultados_combinados.columns[1:])
cores = plt.cm.viridis(np.linspace(0, 1, num_cores))

for i, coluna in enumerate(resultados_combinados.columns[1:], start=0):
    plt.plot(resultados_combinados['hour'], resultados_combinados[coluna], label=coluna, color=cores[i])

plt.xlabel('0.25 Hour')  
plt.ylabel('Value')  
plt.title('Gráfico de Linhas')  
plt.legend()  
plt.ylim(bottom=0)
plt.grid(True)  

# Defina o nome do arquivo para salvar
nome_arquivo = f"Figura_Simulacao_{analise}.png"

# Salve a figura
plt.savefig(nome_arquivo)

# Exibir o gráfico
plt.show()
