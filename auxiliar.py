import random

def create_file(name, parameters):
    arquivo = open(name, "w")
    arquivo.write(parameters)

def create_circuit():
    # Chama uma quantidade de cargas
    num_cargas = int(input("defina a quantidade de cargas: "))

    # Cria um array vazio para concatenar as cargas
    cargas = ""

    # Estrutura de repetição para a criação das cargas
    for i in range(1, num_cargas + 1):
        carga_name = f"carga{i}.txt"
        kw = random.uniform(5, 50)
        pf = random.uniform(0.8, 1)
        carga_value = f"new load.{carga_name} phases=3 conn=wye bus1=b kw={kw:.2f} pf={pf:.2f} kv=0.22 daily=default\n"
        cargas += carga_value

    # Cria a função para a criação do circuito geral
    files = {
    "arranjo.txt": "new linecode.arranjo rmatrix=(0.02 | 0.02 0.04 | 0.02 0.04 0.06) xmatrix=(0.48 | 0.48 0.6 | 0.48 0.6 0.69) cmatrix=(-2.51 | 0.69 4.1 | -0.51 0.69 4.1)\n",
    "fonte.txt": "new circuit.fonte bus1=a basekv=0.22 phases=3\n",
    "linha1.txt": "new line.linha1 bus1=a bus2=b phases=3 length=0.5 units=km linecode=arranjo\n",
    "linha2.txt": "new line.linha2 bus1=b bus2=c phases=3 length=0.15 units=km linecode=arranjo\n",
    "loadshape.txt": "new loadshape.semana",
    "carga.txt": cargas
    }

    return files
