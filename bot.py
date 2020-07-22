from dialogs import dialogs
from settings import bot
import api
import json

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, dialogs['welcome'])

@bot.message_handler(regexp='^[0-9]{11}$')
def message_handler(message):
	
	try:
		json_response = api.consultaDivida(message.text)
		if 'error' in json_response.keys():
			bot.reply_to(message, dialogs['sem_dividas'])
	except:
		bot.reply_to(message, dialogs['erro'], parse_mode='markdown')
	else:
		try:	
			resultados = dialogs['resumo'].format(
				json_response['id'], json_response['cpf'], json_response['nomeConsumidor'],
				json_response['codigoCredor'], json_response['nomeCredor'], json_response['valorTotal'],
				json_response['dataCalculo']
			)
			for divida in json_response['carteiras']:
				resultados += dialogs['divida'].format(
					divida['id'], divida['nome'], divida['numero'], divida['valorSaldoDevedor'], divida['valorJuros'],
					divida['valorMulta'], divida['valorDesconto'], divida['valorTotal']
				)
				for fatura in divida['contratos']:
					resultados += dialogs['fatura'].format(
						fatura['numero'], fatura['valorSaldoDevedor'], fatura['valorJuros'], fatura['valorMulta'],
						fatura['valorDesconto'], fatura['valorTotal'], fatura['diasAtraso'],
						fatura['descricaoDetalheContrato'], fatura['cedente'], fatura['cedente']
					)
		except KeyError:
			file = bytes(
				json.dumps(json_response, indent=4), 'utf-8'
			)
			bot.send_document(message.chat.id, file)
		else:
			bot.reply_to(message, resultados, parse_mode='markdown')
			
			file = bytes(
				json.dumps(json_response, indent=4), 'utf-8'
			)
			
			bot.send_document(message.chat.id, file)
		
		
bot.polling(none_stop=True)
