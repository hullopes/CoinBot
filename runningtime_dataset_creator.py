import time
import ccxt
import pandas as pd
import datetime
import random
import os
import matplotlib.pyplot as plt

batch_size = 60
next_records = 600

start_date = '2017-01-01'
end_date = '2022-12-31'
start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
end_timestamp = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
exchange = ccxt.binance()
hdf5_filename = 'dataset/running_bts_1s.h5'
sync_file = 'flags/dataset_pronto.txt'
stop_file = 'flags/stop.txt'

## roda enquanto não encontra o arquivo do dataset, ou quando encontra o arquivo flag de parada
while True:
    while True:
        print("Checando se o dataset existe")
        if os.path.exists(hdf5_filename):
            ## se o arquivo do dataset existe, é pq ainda não foi lido pela outra aplicação
            ## assim que ele é lido lá, ele é removido
            print("Arquivo de dataset foi encontrado! Dormindo.")
            time.sleep(5)
        else:
            print("Arquivo de dataset não encontrado! Iniciando o fetch de candles.")
            break


    # Inicialize a lista para armazenar os dados
    all_data = []
    candles_count = 0
    random_timestamp = random.randint(start_timestamp, end_timestamp)
    while True:
        print("Buscando candles")

        ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1s', since=random_timestamp, limit=1000)
        # Se não houver mais dados disponíveis, saia do loop
        if len(ohlcv) == 0:
            print("Encerrando!!")
            break

        # Adicione os dados à lista
        all_data.extend(ohlcv)
        # Atualize o contador de candles acumulados
        candles_count += len(ohlcv)

        # Atualize o timestamp de início para o próximo candle
        sss = ohlcv[-1][0]
        random_timestamp = ohlcv[-1][0] + 1000  # Adiciona 1 segundo ao timestamp do último candle
        print("Atualizando o índice de início. De {} para {}".format(pd.to_datetime(sss, unit='ms'),
                                                                     pd.to_datetime(random_timestamp, unit='ms')))
        #start_timestamp = df['timestamp'].iloc[-1] + 1000
        print(":::{}/{} novos Candles obtidos".format(len(ohlcv), candles_count))
        # Imprima a data do último candle antes de salvar
        last_candle_timestamp = pd.to_datetime(ohlcv[-1][0], unit='ms')
        print("Último candle obtido antes de buscar novamente:", last_candle_timestamp)

        # Verifique se o número de candles acumulados atingiu o limite
        if candles_count >= (1000) * 35:

            # Cria um DataFrame pandas com os dados acumulados
            df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            # Salve os dados acumulados em um arquivo HDF5
            df.to_hdf(hdf5_filename, key='btc', mode='w')
            print("Dataset criado com sucesso!")
            break

    ## checando se a flag de parada existe
    # Excluir o arquivo
    if os.path.exists(stop_file):
        print("Arquivo de stop encontrado! Parando fetch de dados!")
        os.remove(stop_file)
        print('O arquivo de stop foi excluído.')
        break


