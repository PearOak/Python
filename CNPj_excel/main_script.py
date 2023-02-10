import consultaGoogle, envia_email, geraExcel

def main_function():
	resposta = ""
	conteudo_email = ""
	try:
		resposta = consultaGoogle.CriaPlanilhaInput()
		if resposta["sucesso"] == False:
			raise Exception(f"Planilha de Entrada não foi extraida!\nErro: {str(resposta['mensagem'])}")
		resposta = geraExcel.geraPlanilha()
		if resposta["sucesso"] == False:
			raise Exception(f"Planilha de Saída não foi gerada!\n ({str(resposta['mensagem'])})")
		else:
			conteudo_email = "Sua solicitação foi processada com sucesso! Segue anexo!"
	except Exception as erro:
		conteudo_email = f"Sua solicitação não foi processada!<br><br>Motivo: <b>{erro}</b><br>Favor contatar administrador!"
	envia_email.enviaEmail(conteudo_email)

main_function()
