import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Parameters.parametersgen import create_simulacoes

analise = int(input("Qual será a análise?\n0 - Sem nada ou\n1 - Com pvsystem ou\n2 - Com pvsystem e baterias\nSua resposta: "))

# puxando o resultado, usando como input o número de simulações
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
