import py_dss_interface
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from auxiliar import create_file
from auxiliar import create_circuit
from auxiliar import create_simulacoes

# definindo o número de simulações

resultados = create_simulacoes(10)

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
