import random
from Parameters.input_real_data.database import calcular_media_diaria_por_hora
from Parameters.input_real_data.database import calcular_irradiancia_diaria_por_hora
from Parameters.input_real_data.database import calcular_potencia_diaria_por_hora
import pandas as pd

def create_file(name, parameters):
    arquivo = open(name, "w")
    arquivo.write(parameters)

def create_circuit(num_cargas,num_pvs,pmpp,num_baterias,bateria_kwnominal,bateria_kwhora,bateria_modo):

    # Cria um array vazio para concatenar as linhas
    linhas = ""

    # Estrutura de repetição para criação das linhas que conectam as cargas à linha principal
    for i in range(2, num_cargas + 1):
        linha_value = f"new line.linha{i} bus1=b bus2=c{i-1} phases=3 length=0.01 units=km linecode=arranjo\n"
        linhas += linha_value

    # Cria um array vazio para concatenar as cargas
    cargas = ""

    # Estrutura de repetição para a criação das cargas
    for i in range(1, num_cargas + 1):
        carga_name = f"carga{i}"
        kw = random.uniform(150, 200)
        pf = random.uniform(0.8, 1)
        carga_value = f"new load.{carga_name} phases=3 conn=wye bus1=c{i} kw={kw:.2f} pf={pf:.2f} kv=0.38 daily=semana\n"
        cargas += carga_value

    # Cria um array vazio para concatenar os pvsysts
    pvsyst = ""

    # Estrutura de repetição para a criação dos pvsysts
    for i in range(1, num_pvs + 1):
        pvsyst_value = f"new pvsystem.pv{i} phases=3 bus1=c{i} kv=0.38 irrad= 1 pmpp={pmpp} temperature=26 pf=1 \n\
        %cutin=0.1 %cutout=0.1 effcurve=myeff p-tcurve=mypvst daily=myirrad tdaily=mytemp\n"
        pvsyst += pvsyst_value

    # Transforma o dicionário de entrada e saída da bateria para a curva que é lida pelo opendss
    curva_bateria = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:-0.15, 9:-0.25, 10:-0.5, 11:-0.25, 12:0, 13:0, 14:0, 15:0, 16:0.25, 17:0.5, 18:0.75, 19:1, 20:0.75, 21:0.5, 22:0.25, 23:0, 24:0}
    curva_bateria_dss = tuple(valor for valor in curva_bateria.values() for _ in range(4))
    
    # Cria um array vazio para concatenar as baterias
    baterias = ""

    # Estrutura de repetição para a criação das baterias
    for i in range(1, num_baterias + 1):
        baterias_value = f"new storage.batery{i} phases=3 bus1=c{i} kv=0.38 kwrated={bateria_kwnominal} kwhrated={bateria_kwhora} dispmode={bateria_modo} %reserve = 20 %stored = 50 daily=storagecurve\n"
        baterias += baterias_value
        
    # Cálculo das médias de temperatura, potência e irradiação com base no arquivos do sam results.csv
    pvsyst_temp = calcular_media_diaria_por_hora('results.csv')
    pvsyst_pot = calcular_potencia_diaria_por_hora('results.csv',num_pvs)
    pvsyst_irrad = calcular_irradiancia_diaria_por_hora('results.csv')
    
    # Cria a função para a criação do circuito geral
    files = {
    "arranjo.txt": "new linecode.arranjo \n\
        rmatrix=(0.02 | 0.02 0.04 | 0.02 0.04 0.06)\n\
        xmatrix=(0.48 | 0.48 0.6 | 0.48 0.6 0.69) \n\
        cmatrix=(-2.51 | 0.69 4.1 | -0.51 0.69 4.1)\n",

    "fonte.txt": "new circuit.fonte bus1=a basekv=0.380 phases=3\n",
    
    "linhas.txt": "new line.linha1 bus1=a bus2=b phases=3 length=0.5 units=km linecode=arranjo\n",

    "linhas_cargas.txt": linhas,

    "carga.txt": cargas,

    "pvsyst_temp.txt": pvsyst_temp,

    "pvsyst_irrad.txt": pvsyst_irrad,

    "pvsyst_pot.txt": pvsyst_pot,

    "mypvsyst.txt": f"new xycurve.mypvsist npts=4 xarray=(0 25 75 100) yarray=(1.2 1 .8 .6) \n\
        new xycurve.myeff npts=4 xarray=(.1 .2 .4 1) yarray=(.86 .9 .93 .97) \n\
        new loadshape.myirrad npts=96 interval=0.25 \n\
        redirect pvsyst_irrad.txt \n\
        new tshape.mytemp npts=96 interval=0.25 \n\
        redirect pvsyst_temp.txt\n",

    "mypvsyst_cargas.txt": pvsyst,

    "baterias.txt": f"new loadshape.storagecurve npts=96 interval=0.25 \n\
        mult={curva_bateria_dss}\n",
    "baterias_cargas.txt": baterias
    }

    return files