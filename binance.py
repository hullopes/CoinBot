import ccxt
import pandas as pd
import datetime


# Inicialize a exchange (Binance neste exemplo)
exchange = ccxt.binance()

# Obtenha dados históricos de OHLCV (Open, High, Low, Close, Volume)
symbol = 'BTC/USDT'  # Par de negociação (Bitcoin em relação ao Tether)
timeframe = '1m'     # Intervalo de tempo 1d: 1 dia; 1w: 1 semana;
limit = 10          # Número de barras de histórico a serem recuperadas

# Obtendo os dados
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

# Cria um DataFrame pandas com os dados OHLCV
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
total_registros = df.shape[0]
print("Total de registros:", total_registros)
# salvando em HDF5
#df.to_hdf('dataset/btc_data_1h.h5', key='btc', mode='w')


# Exemplo de saída dos dados
for candle in ohlcv:
    print(candle)
print("Feito!!")