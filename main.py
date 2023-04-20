import py_dss_interface
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# chamando o opendss
dss = py_dss_interface.DSSDLL()

# criando o loadshape
loadShape1 = (0.677, 0.6256, 0.6087, 0.5833, 0.58028, 0.6025, 0.657, 0.7477, 0.832, 0.88,
              0.94, 0.989, 0.985, 0.98, 0.9898, 0.999, 1, 0.958, 0.936, 0.913, 0.876, 0.876, 0.828, 0.756)
df1 = pd.DataFrame(loadShape1)
df1.to_csv('loadshape1.csv', index=False, header=False)

# simulação 1 - carga sem nada
dss_file1 = "D:/OpenDSS/POLI_storage_pvsyst_simulation/simulacao1.dss"

# simulação 2 - carga somente com storage em mode = default
dss_file2 = "D:/OpenDSS/POLI_storage_pvsyst_simulation/simulacao2.dss"

# simulação 3 - carga somente com storage em mode = follow
dss_file3 = "D:/OpenDSS/POLI_storage_pvsyst_simulation/simulacao3.dss"

# simulação 4 - carga somente com storage em mode = peakshave
dss_file4 = "D:/OpenDSS/POLI_storage_pvsyst_simulation/simulacao4.dss"

# simulação 5 - carga somente com pvsystem
dss_file5 = "D:/OpenDSS/POLI_storage_pvsyst_simulation/simulacao5.dss"

# simulação 4 - carga somente com storage em modo = follow e pvsystem
dss_file6 = "D:/OpenDSS/POLI_storage_pvsyst_simulation/simulacao6.dss"

# rodando os arquivos
dss.text("compile {}".format(dss_file1))
dss.text("compile {}".format(dss_file2))
dss.text("compile {}".format(dss_file3))
dss.text("compile {}".format(dss_file4))
dss.text("compile {}".format(dss_file5))
dss.text("compile {}".format(dss_file6))

# arquivos gerados pela compilação do código

sim1_power_line = "D://OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_line_sim1_1.csv"
sim2_power_line = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_line_sim2_1.csv"
sim2_power_batery = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_batery_sim2_1.csv"
sim3_power_line = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_line_sim3_1.csv"
sim3_power_batery = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_batery_sim3_1.csv"
sim4_power_line = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_line_sim4_1.csv"
sim4_power_batery = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_batery_sim4_1.csv"
sim5_power_line = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_line_sim5_1.csv"
sim6_power_line = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_line_sim6_1.csv"
sim6_power_line2 = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_line2_sim6_1.csv"
sim6_power_batery = "D:/OpenDSS/POLI_storage_pvsyst_simulation/fonte_Mon_monitor_power_batery_sim6_1.csv"

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


# plotando o gráfico

plt.plot(df_sim1_power_line['hour'],
         df_sim1_power_line[' P1 (kW)'], label='Simulacao 1')
plt.plot(df_sim3_power_line['hour'],
         df_sim3_power_line[' P1 (kW)'], label='Simulacao 2')

plt.xlabel('hour')
plt.ylabel(' P1 (kW)')
plt.title('Potência na linha')
plt.legend()
plt.show()
