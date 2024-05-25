import ccxt
import pandas as pd
import datetime
import time

# Inicialize a exchange (Binance neste exemplo)
exchange = ccxt.binance()

# Parâmetros para obtenção dos dados
symbol = 'BTC/USDT'  # Par de negociação (Bitcoin em relação ao Tether)
timeframe = '1s'  # Intervalo de tempo (5 minutos)
start_date = '2010-01-01'  # Data de início do período desejado
end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Data de término é a data atual

# Converta as datas para timestamps UNIX
start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
end_timestamp = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)

# Inicialize a lista para armazenar os dados
all_data = []

# Obtenha os dados até a data atual, em lotes de 1000 candles
while True:
    # Obtendo os dados
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=start_timestamp, limit=1000)

    # Se não houver mais dados disponíveis, saia do loop
    if len(ohlcv) == 0:
        print("Encerrando!!")
        break

    # Adicione os dados à lista
    all_data.extend(ohlcv)

    # Atualize o timestamp de início para o próximo candle
    start_timestamp = ohlcv[-1][0] + (5 * 60 * 1000)  # Adiciona 5 minutos ao timestamp do último candle

    print("Etapa concluída. Aguardando para reiniciar!!")
    # Aguarde um curto período de tempo para evitar sobrecarga na API
    time.sleep(1)

# Cria um DataFrame pandas com os dados OHLCV
df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Converta o timestamp para o formato de data e hora
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Salve os dados em um arquivo HDF5
df.to_hdf('dataset/btc_data_1s.h5', key='btc', mode='w')

# Total de registros
total_registros = df.shape[0]
print("Total de registros:", total_registros)

print("Feito!!")
