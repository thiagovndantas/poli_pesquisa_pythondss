import py_dss_interface
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from auxiliar import create_file
from auxiliar import create_circuit

# definindo o número de simulações

simulacoes = int(input("qual o número de simulações desejadas?: "))

resultados = []

for i in range(0,simulacoes):
    num_cargas = 100
    num_pvs = int(num_cargas/simulacoes*i)
    pmpp = 40
    num_baterias = int(num_cargas/simulacoes*i)
    bateria_kwnominal = 15
    bateria_kwhora = 60
    bateria_modo = "follow"

    # Criação do circuito
    files = create_circuit(num_cargas,num_pvs,pmpp,num_baterias,bateria_kwnominal,bateria_kwhora,bateria_modo)

    # Criando os files do circuito
    for name, parameters in files.items():
        create_file(name, parameters)

    # chamando o opendss
    dss = py_dss_interface.DSSDLL()

    # criando o loadshape
    loadShape1 = (0.677, 0.6256, 0.6087, 0.5833, 0.58028, 0.6025, 0.657, 0.7477, 0.832, 0.88,
                0.94, 0.989, 0.985, 0.98, 0.9898, 1, 1.05, 1.02, 1, 0.97, 0.9, 0.876, 0.828, 0.756)

    df1 = pd.DataFrame(loadShape1)
    df1.to_csv('loadshape1.csv', index=False, header=False)

    dss_file5 = "simulacao5.dss"
    
    # rodando os arquivos
    dss.text("compile {}".format(dss_file5))

    # arquivos gerados pela compilação do código

    sim5_power_line = "fonte_Mon_monitor_power_line_sim5_1.csv"  # linha 1 terminal 2

    # criando os dataframes

    df_sim5_power_line = pd.read_csv(sim5_power_line,usecols=[2])

    resultados.append(df_sim5_power_line)

resultados_combinados = pd.concat(resultados,axis=1)

resultados_combinados.columns = [f'P1_{i+1} kW' for i in range(len(resultados_combinados.columns))]

# coluna de horas a partir do 0
resultados_combinados.insert(0, 'hour', range(1, len(resultados_combinados) + 1))

# plotando o gráfico

# Definindo as cores para cada linha

num_cores = len(resultados_combinados.columns[1:])
cores = plt.cm.viridis(np.linspace(0, 1, num_cores))

for i, coluna in enumerate(resultados_combinados.columns[1:], start=0):
    plt.plot(resultados_combinados['hour'], resultados_combinados[coluna], label=coluna, color=cores[i])

plt.xlabel('Hour')  
plt.ylabel('Value')  
plt.title('Gráfico de Linhas')  
plt.legend()  
plt.grid(True)  
plt.show()
