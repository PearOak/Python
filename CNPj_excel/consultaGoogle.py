import requests
import pandas

def CriaPlanilhaInput():
	dict_resposta = {}
	try:
		url = "https://script.google.com/macros/s/AKfycbzqnKarXatTLgL4Jrn9L3KuvryDhuoIeutpyNtsZzlrS5Dfnut_D1-gjlMA_LkycQA/exec"
		resposta = requests.request("GET", url).json()[0]["data"]
		tabela = pandas.DataFrame(resposta)
		tabela.to_excel("input_cnpj.xlsx", sheet_name='Dados', index=False, na_rep='NaN')

		#Para o trecho abaixo funcionar, é necessário instalar a biblioteca xlsxwriter
		escritor = pandas.ExcelWriter("input_cnpj.xlsx")
		tabela.to_excel(escritor, sheet_name='Dados', index=False, na_rep='NaN')
		for coluna in tabela:
			tam = max(tabela[coluna].astype(str).map(len).max(), len(coluna))
			indice = tabela.columns.get_loc(coluna)
			escritor.sheets['Dados'].set_column(indice, indice, tam)
		escritor.save()
		dict_resposta["sucesso"] = True
		dict_resposta["mensagem"] = "Deu bom!"
	except Exception as erro:
		dict_resposta["sucesso"] = False
		dict_resposta["mensagem"] = f"Sua solicitação não será processada (erro: {str(erro)}).<br>Favor Contactar o administrador!"
	return dict_resposta

