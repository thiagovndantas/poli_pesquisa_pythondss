import random
from database import calcular_media_diaria_por_hora
from database import calcular_irradiancia_diaria_por_hora
from database import calcular_potencia_diaria_por_hora

def create_file(name, parameters):
    arquivo = open(name, "w")
    arquivo.write(parameters)

def create_circuit():
    # Solicita as informações para a criação do circuito
    num_cargas = int(input("defina a quantidade de cargas: "))
    num_pvs = int(input("defina a quantidade de cargas com sistemas solares instalados: "))
    pmpp = int(input("defina a potência máxima por inversor: "))
    num_baterias = int(input("defina a quantidade de cargas com baterias instaladas: "))
    bateria_kwnominal = int(input("defina a potência nominal das baterias: "))
    bateria_kwhora = int(input("defina o armazenamento em kwh das baterias: "))
    bateria_modo = input("defina o modo da bateria:\n\
                             - follow\n\
                             - peakshave\n")


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
        carga_value = f"new load.{carga_name} phases=3 conn=wye bus1=c{i} kw={kw:.2f} pf={pf:.2f} kv=0.38 daily=default\n"
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

    "loadshapes": "new loadshape.semana\n\
    new loadshape.storagecurve npts=24 interval=1 \n\
    mult=(0 0 0 0 0 0 0 0  0 -1 -1 -1 -1  -1 -1 0  0  1   1   1    1  1 0  0 0)",
    #     1 2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17  18  19  20  21 22 23
    "storage.batery.txt": "new storage.batery phases=3 bus1=c kv=0.380 \n\
        kwrated=15 kwhrated=60 dispmode=follow daily=storagecurve",

    "carga.txt": cargas,

    "pvsyst_temp.txt": pvsyst_temp,

    "pvsyst_irrad.txt": pvsyst_irrad,

    "pvsyst_pot.txt": pvsyst_pot,

    "mypvsyst.txt": f"new xycurve.mypvsist npts=4 xarray=(0 25 75 100) yarray=(1.2 1 .8 .6) \n\
        new xycurve.myeff npts=4 xarray=(.1 .2 .4 1) yarray=(.86 .9 .93 .97) \n\
        new loadshape.myirrad npts=24 interval=1 \n\
        redirect pvsyst_irrad.txt \n\
        new tshape.mytemp npts=24 interval=1 \n\
        redirect pvsyst_temp.txt\n",

    "mypvsyst_cargas.txt": pvsyst,

    "baterias.txt": f"new loadshape.storagecurve npts=24 interval=1 \n\
        mult=(0 0 0 0 0 0 0 0  0 -1 -1 -1 -1  -1 -1 0  0  1   1   1    1  1 0  0 0)\n",
        #     1 2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17  18  19  20  21 22 23
    "baterias_cargas.txt": baterias
    }

    return files
