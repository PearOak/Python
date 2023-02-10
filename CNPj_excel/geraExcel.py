import pandas
import json
import re
import datetime as date
import serpro
import genericFunctions
import pytz

def geraPlanilha():
	cnpj_atual = ""
	dict_resposta = {}
	json_final = []
	dadosInput = pandas.read_excel("input_cnpj.xlsx")
	json_input = json.loads(dadosInput.to_json(orient="records"))
	tam = len(json_input)
	amostra = json_input[0]
	atributo = ""
	cnpjsInvalidos = ""

	for chave in amostra:
		chaveTratada = re.sub("[^A-Za-z]", "", chave)
		if chaveTratada.lower() == "cnpj":
			atributo = chave
			break
	try:
		#print(tam)
		for i in range(tam):
			#cnpjsInvalidos = ""
			cnpjAtual = json_input[i][atributo]
			cnpjValido = genericFunctions.validaCnpj(str(cnpjAtual))
			if cnpjValido == False:
				cnpjsInvalidos = f"{cnpjsInvalidos}{i+2}, "

		#cnpjsInvalidos = cnpjsInvalidos[:-2]
		if len(cnpjsInvalidos) > 0:
			cnpjsInvalidos = cnpjsInvalidos[:-2]
			raise Exception(f"Não é possível prosseguir com sua solicitação pois há um ou mais CNPjs inválidos na(s) Linha(s) {cnpjsInvalidos}")
		for i in range(tam):
			dic_atual = {}
			json_input[i]["cnpj"] = str(json_input[i]["cnpj"])
			json_input[i]["cnpj"] = re.sub("[^\d]", "", json_input[i]["cnpj"])
			while len(json_input[i]["cnpj"]) < 14:
				json_input[i]["cnpj"] = f"0{json_input[i]['cnpj']}"
			json_input[i]["cnpj"] = re.sub("(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})", r"\1.\2.\3/\4-\5", json_input[i]["cnpj"])
			print(json_input[i]["cnpj"])
			cnpjTratado = re.sub('[^\d]', '', str(json_input[i]['cnpj']))
			dic_atual["CNPj Pesquisado"] = json_input[i]["cnpj"]

			try:
				response = serpro.consultaCnpj(cnpjTratado)
				#print(response)

				if type(response) == str and re.search("Erro", response) != None:
					#print("Devia ter passado daqui!")
					raise Exception(f"CNPj {cnpjTratado} não foi consultado! ({response})")
				elif "message" in response and len(response) == 1:
					#print("Caiu no lugar certo!")
					cnpj_atual = json_input[i]['cnpj']
					raise Exception(f"CNPj {cnpj_atual} não foi consultado! ({response})")
				else:
					#print("Não devia ter chegado aqui!")
					dataConsulta = date.datetime.now(pytz.timezone('America/Sao_Paulo'))
					capitalOriginal = f"{(response['capitalSocial']/100):.2f}".split(".")
					inteiroCapital = f"{int(capitalOriginal[0]):,}".replace(",", ".")
					decimalCapital = f"{capitalOriginal[1]}"
					capitalSocial = f"R$ {inteiroCapital},{decimalCapital}"
					dic_atual["Data e Hora Consulta"] = dataConsulta.strftime("%d/%m/%Y %H:%M:%S:%f")
					dic_atual["Número de Inscrição"] = genericFunctions.numeroInscricao(f"{response['ni']}")
					dic_atual["Data de Abertura"] = genericFunctions.converteData(f"{response['dataAbertura']}")
					dic_atual["Nome Empresarial"] = response["nomeEmpresarial"]
					dic_atual["Nome Fantasia"] = response["nomeFantasia"]
					dic_atual["Código CNAE Principal"] = f"{response['cnaePrincipal']['codigo']} - {response['cnaePrincipal']['descricao']}"
					try:
						dic_atual["Código CNAE Secundário"] = genericFunctions.cnaesSecundarios(response["cnaeSecundarias"], "|")
					except:
						dic_atual["Código CNAE Secundário"] = "N/A"
					dic_atual["Logradouro"] = f"{response['endereco']['tipoLogradouro']} {response['endereco']['logradouro']}"
					dic_atual["Número"] = f"{response['endereco']['numero']}"
					dic_atual["Complemento"] = f"{response['endereco']['complemento']}"
					dic_atual["Bairro"] = f"{response['endereco']['bairro']}"
					dic_atual["Município"] = f"{response['endereco']['municipio']['descricao']}"
					dic_atual["CEP"] = f"{response['endereco']['cep']}"
					dic_atual["UF"] = f"{response['endereco']['uf']}"
					#Criar condição com as códigos de acordo com o site da Serpro (https://apicenter.estaleiro.serpro.gov.br/documentacao/consulta-cnpj/pt/tipos_situacao_cadastral/)
					try:
						if response['situacaoCadastral']['codigo'] == "1":
							dic_atual["Situação Cadastral"] = "NULA"
						elif response['situacaoCadastral']['codigo'] == "2":
							dic_atual["Situação Cadastral"] = "ATIVA"
						elif response['situacaoCadastral']['codigo'] == "3":
							dic_atual["Situação Cadastral"] = "SUSPENSA"
						elif response['situacaoCadastral']['codigo'] == "4":
							dic_atual["Situação Cadastral"] = "INAPTA"
						elif response['situacaoCadastral']['codigo'] == "5":
							dic_atual["Situação Cadastral"] = "ATIVA NÃO REGULAR"
						elif response['situacaoCadastral']['codigo'] == "8":
							dic_atual["Situação Cadastral"] = "BAIXADA"
						else:
							raise Exception("SITUAÇÃO DESCONHECIDA")
					except:
						dic_atual["Situação Cadastral"] = f"DESCONHECIDA"
					#Fim da condição
					dic_atual["Data da Situação Cadastral"] = f"{genericFunctions.converteData(response['situacaoCadastral']['data'])}"
					dic_atual["Motivo da Situação Cadastral"] = f"{response['situacaoCadastral']['motivo']}"
					dic_atual["Situação Especial"] = f"{response['situacaoEspecial']}"
					dic_atual["Data da Situação Especial"] = f"{response['dataSituacaoEspecial']}"
					dic_atual["Optante pelo Simples Nacional"] = f"{response['informacoesAdicionais']['optanteSimples']}"
					try:
						dic_atual["Data do Simples Nacional"] = f"{genericFunctions.converteData(response['informacoesAdicionais']['listaPeriodosSimples'][len(response['informacoesAdicionais']['listaPeriodosSimples'])-1]['dataInicio'])}"
					except:
						dic_atual["Data do Simples Nacional"] = "N/A"
					dic_atual["Optante pelo MEI"] = f"{response['informacoesAdicionais']['optanteMei']}"
					dic_atual["Natureza Jurídica"] = f"{response['naturezaJuridica']['codigo']} - {response['naturezaJuridica']['descricao']}"
					try:
						dic_atual["Telefone"] = genericFunctions.telefones(response["telefones"], ";")
					except:
						dic_atual["Telefone"] = "TELEFONE NÃO ENCONTRADO"
					dic_atual["E-mail"] = f"{response['correioEletronico']}"
					try:
						dic_atual["Quadro de Sócios"] = genericFunctions.stringMultiplos1(response["socios"],"nome",";")
					except:
						dic_atual["Quadro de Sócios"] = "Socio(s) não encontrado(s)"
					try:
						dic_atual["Capital Social"] = capitalSocial
					except Exception as erro:
						print(f"Erro no CNPj {str(json_input[i]['cnpj'])} ({str(erro)})")
						dic_atual["Capital Social"] = "NÃO ENCONTRADO"
					json_final.append(dic_atual)
			except Exception as erro:
				print(f"Erro: ({str(erro)})")
		print(json_final)
		tabela = pandas.DataFrame(json_final)
		tabela.to_excel("output_cnpj.xlsx", sheet_name='Informações', index=False, na_rep='NaN')

		#Para o trecho abaixo funcionar, é necessário instalar a biblioteca xlsxwriter
		escritor = pandas.ExcelWriter("output_cnpj.xlsx")
		tabela.to_excel(escritor, sheet_name='Informações', index=False, na_rep='NaN')
		for coluna in tabela:
			tam = max(tabela[coluna].astype(str).map(len).max(), len(coluna))
			indice = tabela.columns.get_loc(coluna)
			escritor.sheets['Informações'].set_column(indice, indice, tam)
		escritor.save()
		dict_resposta["sucesso"] = True
		dict_resposta["mensagem"] = "Deu bom! ;)"
	except Exception as erro:
		dict_resposta["sucesso"] = False
		dict_resposta["mensagem"] = f"{str(erro)}"
	return dict_resposta
