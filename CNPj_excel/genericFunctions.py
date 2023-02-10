import re
import datetime as date

def telefones(lista, delimitador):
	tam = len(lista)
	stringFinal = ""

	for i in range(tam):
		telefoneTratado = ""
		telefoneAtual = str(lista[i]['numero'])
		for j in range(len(telefoneAtual)):
			if j == 4:
				telefoneTratado = f"{telefoneTratado}-{telefoneAtual[j]}"
			else:
				telefoneTratado = f"{telefoneTratado}{telefoneAtual[j]}"
		stringFinal = f"{stringFinal}({lista[i]['ddd']}) {telefoneTratado}{delimitador}"
	return stringFinal

def cnaesSecundarios(lista, delimitador):
	tam = len(lista)
	stringFinal = ""

	for i in range(tam):
		stringFinal = f"{stringFinal}{lista[i]['codigo']} - {lista[i]['descricao']} {delimitador} "
	return stringFinal

def converteData(str_data):
	data_separada = str_data.split("-")
	obj_data = date.datetime(int(data_separada[0]), int(data_separada[1]), int(data_separada[2]))
	return obj_data.strftime("%d/%m/%Y")

def numeroInscricao(cnpj):
	numCnpj = re.sub("[^\d]", "", f"{cnpj}")
	tam = len(numCnpj)
	stringCnpj = ""
	matriz = True if cnpj[11] == "1" else False

	for i in range(tam):
		if i == 2 or i == 5:
			stringCnpj = f"{stringCnpj}.{cnpj[i]}"
		elif i == 8:
			stringCnpj = f"{stringCnpj}/{cnpj[i]}"
		elif i == 12:
			stringCnpj = f"{stringCnpj}-{cnpj[i]}"
		else:
			stringCnpj = f"{stringCnpj}{cnpj[i]}"
	retorno = f"{stringCnpj}|{'MATRIZ' if matriz == True else 'FILIAL'}"
	return retorno

def stringMultiplos1(lista, formato, delimitador):
	tam = len(lista)
	stringFinal = ""

	for i in range(tam):
		stringFinal = f"{stringFinal}{lista[i][formato]}{delimitador} "
	return stringFinal

def calculaModulo11(amostra):
	stringFinal = f"{amostra}"
	i = len(amostra)-1
	soma = 0
	multiplicador = 2

	while i >= 0:
		soma = soma + int(amostra[i])*multiplicador
		if multiplicador == 9:
			multiplicador = 2
		else:
			multiplicador = multiplicador + 1
		i = i - 1
	modulo11 = soma % 11

	if (modulo11 < 2):
		stringFinal = f"{stringFinal}{0}"
	else:
		stringFinal = f"{stringFinal}{str(11-modulo11)}"
	return stringFinal

def validaCnpj(cnpj):
	cnpjTratado = re.sub("[^\d]", "", cnpj)
	while len(cnpjTratado) < 14:
		cnpjTratado = f"0{cnpjTratado}"
	primeiroDigito = cnpjTratado[0]
	umDigito = re.search(primeiroDigito+"{14}", cnpjTratado)
	tam = len(cnpjTratado)

	if umDigito != None or tam != 14:
		return False
	else:
		amostra = cnpjTratado[0:12]
		tam = len(amostra)

		while tam != 14:
			amostra = calculaModulo11(amostra)
			tam = len(amostra)
		if cnpjTratado == amostra:
			return True
		else:
			return False
