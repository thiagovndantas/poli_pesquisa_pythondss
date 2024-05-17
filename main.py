import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import py_dss_interface

from Parameters.parametersgen import create_circuit
from Parameters.parametersgen import create_file

analise = int(input("Defina a análise conforme README.\nSua análise: "))

# puxando o resultado, usando como input o número de simulações

resultados = []

simulator_path = os.path.join(os.path.dirname(__file__),"simulator")

# máscara de simulação que vai obedecer a análise escolhida no par [FV,BESS]
simulator_mask = [[[0,0],[0.25,0],[0.5,0],[0.75,0],[1.0,0]],\
                [[0,0],[0.75,0],[0.75,0.25],[0.75,0.5],[0.75,0.75]],\
                [[0,0],[0.5,0],[0.5,0.25],[0.5,0.5],[0.5,0.75]],\
                [[0,0],[0.25,0],[0.25,0.25],[0.25,0.5],[0.25,0.75]]]

def create_simulacoes():
    for i in simulator_mask[analise]:
        num_cargas = 100
        num_pvs = int(num_cargas*i[0])
        pmpp = 40
        num_baterias = int(num_cargas*i[1])
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

resultados = create_simulacoes()

# resultados são criados em formado de vetor
resultados_combinados = pd.concat(resultados,axis=1)

# nomeando o número de concatenações
resultados_combinados.columns = [f'Simulação {i}' for i in range(len(resultados_combinados.columns))]

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

plt.xlabel('0.25 de hora')  
plt.ylabel('Potência [kW]')  
plt.title('Potência na linha')  
plt.legend()  
plt.ylim(bottom=0)
plt.grid(True)  

texto = ["Cenários de 0, 25, 50 e 75% 100 de penetração de FV","cenários de 0, 25, 50 e 75% de penetração de BESS sob 75% de FV (grande penetração","cenários de 0, 25, 50 e 75% de penetração de BESS sob 50% de FV (média penetração)","cenários de 0, 25, 50 e 75% de penetração de BESS sob 25% de FV (pequena penetração)"]

plt.text(96, 80, texto[analise], fontsize=8, ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))


# Defina o nome do arquivo para salvar
nome_arquivo = f"Figura_Simulacao_{analise}.png"

# Salve a figura
plt.savefig(nome_arquivo)

# Exibir o gráfico
plt.show()
