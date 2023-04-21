import py_dss_interface
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# criação do arranjo
arranjo_file = "arranjo.txt"
arranjo = open(arranjo_file, "w")
arranjo.write("new linecode.arranjo rmatrix=(0.02 | 0.02 0.04 | 0.02 0.04 0.06) xmatrix=(0.48 | 0.48 0.6 | 0.48 0.6 0.69) cmatrix=(-2.51 | 0.69 4.1 | -0.51 0.69 4.1)")

# chamando o opendss
dss = py_dss_interface.DSSDLL()

# criando o loadshape
loadShape1 = (0.677, 0.6256, 0.6087, 0.5833, 0.58028, 0.6025, 0.657, 0.7477, 0.832, 0.88,
              0.94, 0.989, 0.985, 0.98, 0.9898, 0.999, 1, 0.958, 0.936, 0.913, 0.876, 0.876, 0.828, 0.756)
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
dss.text("compile {}".format(dss_file2))
dss.text("compile {}".format(dss_file3))
dss.text("compile {}".format(dss_file4))
dss.text("compile {}".format(dss_file5))
dss.text("compile {}".format(dss_file6))
#dss.text("complie {}".format(dss_file7))


# arquivos gerados pela compilação do código

sim1_power_line = "fonte_Mon_monitor_power_line_sim1_1.csv"
sim2_power_line = "fonte_Mon_monitor_power_line_sim2_1.csv"
sim2_power_batery = "fonte_Mon_monitor_power_batery_sim2_1.csv"
sim3_power_line = "fonte_Mon_monitor_power_line_sim3_1.csv"
sim3_power_batery = "fonte_Mon_monitor_power_batery_sim3_1.csv"
sim4_power_line = "fonte_Mon_monitor_power_line_sim4_1.csv"
sim4_power_batery = "fonte_Mon_monitor_power_batery_sim4_1.csv"
sim5_power_line = "fonte_Mon_monitor_power_line_sim5_1.csv"
sim6_power_line = "fonte_Mon_monitor_power_line_sim6_1.csv"
sim6_power_line2 = "fonte_Mon_monitor_power_line2_sim6_1.csv"
sim6_power_batery = "fonte_Mon_monitor_power_batery_sim6_1.csv"
sim6_power_pv = "fonte_Mon_monitor_power_pv_sim6_1.csv"

# criando os dataframes


df_sim1_power_line = pd.read_csv(sim1_power_line)
df_sim2_power_line = pd.read_csv(sim2_power_line)
df_sim2_power_batery = pd.read_csv(sim2_power_batery)
df_sim3_power_line = pd.read_csv(sim3_power_line)
df_sim3_power_batery = pd.read_csv(sim3_power_batery)
df_sim4_power_line = pd.read_csv(sim4_power_line)
df_sim4_power_batery = pd.read_csv(sim4_power_batery)
df_sim5_power_line = pd.read_csv(sim5_power_line)
df_sim6_power_line = pd.read_csv(sim6_power_line)
df_sim6_power_line2 = pd.read_csv(sim6_power_line2)
df_sim6_power_batery = pd.read_csv(sim6_power_batery)
df_sim6_power_pv = pd.read_csv(sim6_power_pv)


# plotando o gráfico

plt.plot(df_sim1_power_line['hour'],
         df_sim1_power_line[' P1 (kW)'], label='Simulacao 1')
plt.plot(df_sim3_power_line['hour'],
         df_sim3_power_line[' P1 (kW)'], label='Simulacao 6 - Linha 1')
plt.plot(df_sim6_power_line2['hour'],
         df_sim6_power_line2[' P1 (kW)'], label='Simulacao 6 - Linha 2')
plt.plot(df_sim6_power_batery['hour'],
         df_sim6_power_batery[' P1 (kW)'], label='Simulacao 6 - Bateria')
plt.plot(df_sim6_power_pv['hour'],
         df_sim6_power_pv[' P1 (kW)'], label='Simulacao 6 - PV')


plt.xlabel('hour')
plt.ylabel(' P1 (kW)')
plt.title('Potência na linha')
plt.legend()
plt.show()
