import py_dss_interface
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from auxiliar import create_file
from auxiliar import create_circuit

# Criação do circuito
files = create_circuit()

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


# simulação 1 - carga sem nada
dss_file1 = "simulacao1.dss"

# simulação 2 - carga somente com storage em mode = default
dss_file2 = "simulacao2.dss"

# simulação 3 - carga somente com storage em mode = follow
dss_file3 = "simulacao3.dss"

# simulação 4 - carga somente com storage em mode = peakshave
dss_file4 = "simulacao4.dss"

# simulação 5 - carga somente com pvsystem
dss_file5 = "simulacao5.dss"

# simulação 6 - carga somente com storage em modo = follow e pvsystem
dss_file6 = "simulacao6.dss"


# rodando os arquivos
dss.text("compile {}".format(dss_file1))
#dss.text("compile {}".format(dss_file2))
#dss.text("compile {}".format(dss_file3))
#dss.text("compile {}".format(dss_file4))
dss.text("compile {}".format(dss_file5))
#dss.text("compile {}".format(dss_file6))


# arquivos gerados pela compilação do código

sim1_power_line = "fonte_Mon_monitor_power_line_sim1_1.csv"  # linha 1 terminal 2
#sim2_power_line = "fonte_Mon_monitor_power_line_sim2_1.csv"  # linha 1 terminal 2
#sim2_power_batery = "fonte_Mon_monitor_power_batery_sim2_1.csv"
#sim3_power_line = "fonte_Mon_monitor_power_line_sim3_1.csv"  # linha 1 terminal 2
#sim3_power_batery = "fonte_Mon_monitor_power_batery_sim3_1.csv"
#sim4_power_line = "fonte_Mon_monitor_power_line_sim4_1.csv"  # linha 1 terminal 2
#sim4_power_batery = "fonte_Mon_monitor_power_batery_sim4_1.csv"
sim5_power_line = "fonte_Mon_monitor_power_line_sim5_1.csv"  # linha 1 terminal 2
sim5_power_line2_1 = "fonte_Mon_monitor_power_line2_1_sim5_1.csv"  # linha 2 terminal 1
sim5_power_line2_2 = "fonte_Mon_monitor_power_line2_2_sim5_1.csv"  # linha 2 terminal 2
#sim6_power_line = "fonte_Mon_monitor_power_line_sim6_1.csv"  # linha 1 terminal 2
#sim6_power_line2 = "fonte_Mon_monitor_power_line2_sim6_1.csv"  # linha 2 terminal 1
#sim6_power_batery = "fonte_Mon_monitor_power_batery_sim6_1.csv"
# sim6_power_pv = "fonte_Mon_monitor_power_pv_sim6_1.csv"
# sim6_power_load = "fonte_Mon_monitor_power_load_sim6_1.csv"

# criando os dataframes


df_sim1_power_line = pd.read_csv(sim1_power_line)
#df_sim2_power_line = pd.read_csv(sim2_power_line)
#df_sim2_power_batery = pd.read_csv(sim2_power_batery)
#df_sim3_power_line = pd.read_csv(sim3_power_line)
#df_sim3_power_batery = pd.read_csv(sim3_power_batery)
#df_sim4_power_line = pd.read_csv(sim4_power_line)
#df_sim4_power_batery = pd.read_csv(sim4_power_batery)
df_sim5_power_line = pd.read_csv(sim5_power_line)
df_sim5_power_line2_1 = pd.read_csv(sim5_power_line2_1)
df_sim5_power_line2_2 = pd.read_csv(sim5_power_line2_2)
#df_sim6_power_line = pd.read_csv(sim6_power_line)
#df_sim6_power_line2 = pd.read_csv(sim6_power_line2)
#df_sim6_power_batery = pd.read_csv(sim6_power_batery)
# df_sim6_power_pv = pd.read_csv(sim6_power_pv)
# df_sim6_power_load = pd.read_csv(sim6_power_load)


# plotando o gráfico

plt.plot(df_sim1_power_line['hour'],
         df_sim1_power_line[' P1 (kW)'], label='Simulacao 1: Carga sem nada - Linha 1')
plt.plot(df_sim5_power_line['hour'],
         df_sim5_power_line[' P1 (kW)'], label='Simulacao 5: Carga com pvsystem e bateria - Linha 1')
# plt.plot(df_sim5_power_line2_1['hour'],
#         df_sim5_power_line2_1[' P1 (kW)'], label='Simulacao 5: Carga com pvsystem - Linha 2 t1')
# plt.plot(df_sim5_power_line2_2['hour'],
#         df_sim5_power_line2_2[' P1 (kW)'], label='Simulacao 5: Carga com pvsystem - Linha 2 t2')
#plt.plot(df_sim6_power_line2['hour'],
#         df_sim6_power_line2[' P1 (kW)'], label='Simulacao 6: Carga com storage em modo follow e pvsystem - Linha 2')
# plt.plot(df_sim6_power_batery['hour'],
#         df_sim6_power_batery[' P1 (kW)'], label='Simulacao 6: Carga com storage em modo follow e pvsystem - Bateria')
# plt.plot(df_sim6_power_pv['hour'],
#          df_sim6_power_pv[' P1 (kW)'], label='Simulacao 6: Carga com storage em modo follow e pvsystem - # PV')
# plt.plot(df_sim6_power_load['hour']
#          df_sim6_power_load[' P1 (kW)'], label='Simulacao 6 - Load')


plt.xlabel('hour')
plt.ylabel(' P1 (kW)')
plt.title('Potência na linha')
plt.legend()
plt.show()
