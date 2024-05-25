import ccxt
import pandas as pd
import datetime
import time

# Inicialize a exchange (Binance neste exemplo)
exchange = ccxt.binance()

# Parâmetros para obtenção dos dados
symbol = 'BTC/USDT'  # Par de negociação (Bitcoin em relação ao Tether)
timeframe = '1s'  # Intervalo de tempo (1 segundo)
start_date = '2019-05-18'  # Data de início do período desejado
end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Data de término é a data atual
end_date = '2020-12-31'
# Converta as datas para timestamps UNIX0
start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
end_timestamp = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)

# Carregar o último candle do arquivo HDF5
last_candle_df = pd.read_hdf('dataset/btc_data_1s_partial.h5', key='btc')
if not last_candle_df.empty:
    last_candle_timestamp = last_candle_df['timestamp'].iloc[-1]
    start_timestamp = int(last_candle_timestamp.timestamp() * 1000) + 1000  # Adicionar 1 segundo

# Inicialize a lista para armazenar os dados
all_data = []

# Contador para controlar o número de candles acumulados
candles_count = 0

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
    start_timestamp = ohlcv[-1][0] + 1000  # Adiciona 1 segundo ao timestamp do último candle

    # Atualize o contador de candles acumulados
    candles_count += len(ohlcv)

    # Verifique se o número de candles acumulados atingiu 10.000
    if candles_count >= 50000:
        # Cria um DataFrame pandas com os dados acumulados
        df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Converta o timestamp para o formato de data e hora
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Salve os dados acumulados em um arquivo HDF5
        df.to_hdf('dataset/btc_data_1s_partial.h5', key='btc', mode='a')

        # Imprima a data do último candle antes de salvar
        last_candle_timestamp = pd.to_datetime(df['timestamp'].iloc[-1])
        print("Último candle obtido antes de salvar:", last_candle_timestamp)

        # Imprima o total de registros acumulados
        total_registros = df.shape[0]
        print("Total de registros acumulados:", total_registros)

        # Reinicie a lista de dados e o contador de candles
        all_data = []
        candles_count = 0

    print("Etapa concluída. Aguardando para reiniciar!!")
    # Aguarde um curto período de tempo para evitar sobrecarga na API
    time.sleep(1)

print("Feito!!")
