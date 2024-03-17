import random
from database import calcular_media_diaria_por_hora
from database import calcular_irradiancia_diaria_por_hora
from database import calcular_potencia_diaria_por_hora
import py_dss_interface
import pandas as pd

def create_file(name, parameters):
    arquivo = open(name, "w")
    arquivo.write(parameters)

def create_circuit(num_cargas,num_pvs,pmpp,num_baterias,bateria_kwnominal,bateria_kwhora,bateria_modo):
    # Solicita as informações para a criação do circuito
    #num_cargas = c
    #num_pvs = pv
    #pmpp = pm
    #num_baterias = b
    #bateria_kwnominal = int(input("defina a potência nominal das baterias: "))
    #bateria_kwhora = int(input("defina o armazenamento em kwh das baterias: "))
    #bateria_modo = input("defina o modo da bateria:\n\
    #                         - follow\n\
    #                         - peakshave\n")


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
        kw = random.uniform(50, 60)
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

    # Cria um array vazio para concatenar as baterias
    
    baterias = ""

    # Estrutura de repetição para a criação das baterias
    for i in range(1, num_baterias + 1):
        baterias_value = f"new storage.batery{i} phases=3 bus1=c{i} kv=0.38 kwrated={bateria_kwnominal} kwhrated={bateria_kwhora} dispmode={bateria_modo} daily=storagecurve\n"
        baterias += baterias_value
        

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

    "loadshapes": "new loadshape.storagecurve npts=96 interval=0.25 \n\
    mult=(0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0)",
    #     1 2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17  18  19  20  21 22 23
    "storage.batery.txt": "new storage.batery phases=3 bus1=c kv=0.380 \n\
        kwrated=15 kwhrated=60 dispmode=follow daily=storagecurve",

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

    "baterias.txt": f"new loadshape.storagecurve npts=96 interval=1 \n\
        mult=(0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0)\n",
        #     1 2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17  18  19  20  21 22 23
    "baterias_cargas.txt": baterias
    }

    return files

resultados = []
def create_simulacoes(simulacoes,analise):
    for i in range(0,simulacoes):
        num_cargas = 100
        num_pvs = int(num_cargas/simulacoes*i)
        pmpp = 40
        num_baterias = int(num_cargas/simulacoes*i) if analise == 1 else 0
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
        loadShape1 = (0.677, 0.66920548, 0.66165494, 0.65436487, 0.64735173, 0.64063299, 0.63422512, 0.62814558, 0.2241185, 0.61704139, 0.61205166, 0.6074601, 0.60328416, 0.5995413, 0.59624897, 0.59342463, 0.59108574, 0.58924975, 0.58793412, 0.58715629, 0.58693372, 0.58728387, 0.58822419, 0.58977214, 0.59194516, 0.59476069, 0.59823618, 0.60238908, 0.60723683, 0.61279688, 0.61908667, 0.62612363, 0.63392521, 0.64250886, 0.65189203, 0.66209217, 0.67312674, 0.68401318, 0.69476896, 0.70541154, 0.71595837, 0.72642691, 0.73683462, 0.74719897, 0.7575374, 0.76786738, 0.77820636, 0.78857178, 0.79898109, 0.80945173, 0.82000115, 0.8306468, 0.84140613, 0.8522966, 0.86333565, 0.87454072, 0.88592926, 0.89751871, 0.90932652, 0.92137014, 0.93366701, 0.94623458, 0.9590903, 0.97225161, 0.98573597, 0.99956084, 1.01374367, 1.02830191, 1.04325302, 1.05861446, 1.07440369, 1.09063817, 1.10733535, 1.12451269, 1.14218764, 1.16037765, 1.17910019, 1.1983727, 1.21821265, 1.23863751, 1.25966475, 1.28131185, 1.30359628, 1.32653552, 1.35014705, 1.37444834, 1.39945687, 1.42519011, 1.45166555, 1.47890066, 1.50691293, 1.53571983, 1.56533886, 1.59578748)

        
        #df1 = pd.DataFrame(loadShape1)
        #df1.to_csv('loadshape1.csv', index=False, header=False)

        dss_file5 = "simulacao5.dss"
        
        # rodando os arquivos
        dss.text("compile {}".format(dss_file5))

        # arquivos gerados pela compilação do código

        sim5_power_line = "fonte_Mon_monitor_power_line_sim5_1.csv"  # linha 1 terminal 2

        # criando os dataframes

        df_sim5_power_line = pd.read_csv(sim5_power_line,usecols=[2])

        resultados.append(df_sim5_power_line)

    return resultados