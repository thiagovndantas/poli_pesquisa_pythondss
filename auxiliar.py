def create_file(name, parameters):
    arquivo = open(name, "w")
    arquivo.write(parameters)
