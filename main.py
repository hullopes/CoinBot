from coinmarketcap import Client

key = 'c8e2a324-bdbb-48cd-89aa-93098916a8f6'
# Configurar a API CoinMarketCap (substitua 'API_KEY' pelo seu token de API)
#cmc = coinmarketcap.CoinMarketCapAPI('c8e2a324-bdbb-48cd-89aa-93098916a8f6')

# By default throttling of requests are off.
# Ignore the Client's keyword arguments "throttle", "plan", and "block" if
# you don't want the client to throttle requests.

# client_1 will not exceed the number of request each minute with the basic plan.
#client_1 = Client(throttle="minute", plan="basic")
client = Client(apikey=key)

# Obter dados históricos do Bitcoin
#bitcoin_historical_data = cmc.cryptocurrency_historical('BTC', 'USD', start='2020-01-01T00:00:00Z', end='2024-01-01T00:00:00Z')

# Exemplo de saída dos dados
#for data_point in bitcoin_historical_data['data']['quotes']:
#    print(data_point)
