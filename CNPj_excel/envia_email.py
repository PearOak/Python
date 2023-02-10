import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from creds_email import gera_creds as creds
import datetime as date
import re as regex
import pytz

def enviaEmail(texto_parcial):
	agora = date.datetime.now(pytz.timezone('America/Sao_Paulo'))
	hora_atual = int(agora.strftime("%H"))
	if hora_atual >= 6 and hora_atual < 12:
		texto = "Bom dia!<br><br>"
	elif hora_atual >= 12 and hora_atual < 19:
		texto = "Boa tarde!<br><br>"
	else:
		texto = "Boa noite!<br><br>"
	texto = f"{texto}{texto_parcial}"
	credenciais = creds()
	arquivo = "output_cnpj.xlsx"
	#arquivo = "/home/ubuntu/Recruta/09-12-2022/retorno_09122022_162240.txt"
	msg = MIMEMultipart()
	#print(credenciais)
	msg["From"] = credenciais["email"]
	msg["To"] = 'fiscal@bild.com.br, danilo.silva@enkelbpo.com.br, barbara.silva@enkelbpo.com.br'
	#msg["To"] = 'wellpcarv@hotmail.com'
	msg["CC"] = 'wellington.carvalho@enkelbpo.com.br, rafael.toniello@enkelbpo.com.br'
	msg["Subject"] = "[Planilha CNPjs] - Resposta da Solicitação"
	#texto = "Isso aqui é um exemplo de email em <b>Python</b> com a planilha atualizada do fiscal"
	msg.attach(MIMEText(texto, 'html'))

	if regex.search("Sua solicitação foi processada com sucesso! Segue anexo!",texto) != None:
		anexo = open(arquivo, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((anexo).read())
		encoders.encode_base64(part)
		part.add_header("Content-Disposition", f"attachment; filename={arquivo}")
		msg.attach(part)
	#try:
	servidor = smtplib.SMTP('smtp.office365.com', 587)
	print(servidor)
	#except:
	#servidor = smtplib.SMTP_SSL('smtp.office365.com', 465)
	servidor.ehlo()
	servidor.starttls()
	servidor.ehlo()
	servidor.login(credenciais["email"], credenciais["senha"])
	servidor.send_message(msg)
	servidor.quit()
