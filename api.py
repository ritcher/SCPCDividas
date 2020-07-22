import requests
import random
from settings import user_agents

def consultaDivida(cpf):
	
	headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'pt',
		'Connection': 'keep-alive',
		'Authorization': 'Basic VVNFUl9DTElFTlRfQVBQOnBhc3N3b3Jk',
		'User-Agent': random.choice(user_agents)
	}
	
	payload = {
		'grant_type': 'password',
		'username': 'credor-19',
		'password': cpf,
		'type': ''
	}
	
	with requests.post('https://negocie.scpc.com.br/oauth/token', data=payload, headers=headers) as r:
		json_response = r.json()
	
	headers.update(
		{
			'Authorization': 'Bearer {}'.format(json_response['access_token'])
		}
	)
	
	with requests.get('https://negocie.scpc.com.br/consultardividas/19', headers=headers) as r:
		json_response = r.json()
	
	return json_response
	
