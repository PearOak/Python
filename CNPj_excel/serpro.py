import requests
import re

def geraToken():
	url = "https://gateway.apiserpro.serpro.gov.br/token"
	payload = "grant_type=client_credentials"
	headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Authorization": "Basic Qjd5THNHcXhoYVRaSjZ6Q0ZEcHRvU0lvMWw0YTpmblFaOTljNHkzb1BFeWhpOENualNHU0ZtMEVh"
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	return response.json()

def consultaCnpj(cnpj):
	try:
		cnpjTratado = re.sub("[^\d]", "", str(cnpj))
		url = f"https://gateway.apiserpro.serpro.gov.br/consulta-cnpj-df/v2/qsa/{cnpjTratado}"
		creds = geraToken()
		headerReq = {
			"Authorization": f"{creds['token_type']} {creds['access_token']}"
		}
		response = requests.request("GET", url, headers=headerReq)
		return response.json()
	except Exception as erro:
		print(f"Erro: {str(erro)}")
