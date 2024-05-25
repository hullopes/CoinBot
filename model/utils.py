import os
import time

import ccxt
import pandas as pd
import datetime
import random


class BatchLoader:
    def __init__(self, file_path, batch_size=10, next_records=5, running_time=False):
        self.file_path = file_path
        self.batch_size = batch_size
        self.next_records = next_records
        self.is_running_time = running_time # marca se é para usar o dataset running time
        if file_path is not None:
            if self.is_running_time:
                while True:
                    if os.path.exists(file_path):
                        self.df = pd.read_hdf(file_path, key='btc')
                        self.total_records = len(self.df)
                        ## remover o arquivo
                        os.remove(file_path)
                        break
                    else:
                        print("Arquivo de dataset running time não encontrado! Dormindo.")
                        time.sleep(5)
            else:
                ## não se trata de running time. Vamos abrir o arquivo de dataset tradicional.
                self.df = pd.read_hdf(file_path, key='btc')
                self.total_records = len(self.df)
        else:
            self.df = None
            self.total_records = 0
        self.current_index = 0
        self.count_excepts = 0

    def update_dataset(self):
        while True:
            if os.path.exists(self.file_path):
                while True:
                    print("Arquivo de dataset encontrado. Tentando abrí-lo com segurança!")
                    time.sleep(10)
                    try:
                        self.df = pd.read_hdf(self.file_path, key='btc') ## erro! Erro ao tentar abrir arquivo!
                    except OSError as e:
                        print("Arquivo não pode ser aberto com segurança. Dormindo!")
                        time.sleep(10)

                    self.total_records = len(self.df)
                    ## remover o arquivo
                    os.remove(self.file_path)
                    print("Arquivo lido com sucesso!")
                    break
                break
            else:
                print("Arquivo de dataset running time não encontrado! Dormindo.")
                time.sleep(5)

    def get_random_batch_with_next(self):
        # Escolher aleatoriamente o índice inicial do lote
        start_index = random.randint(0, self.total_records - self.batch_size - self.next_records)

        # Obter o lote atual
        batch = self.df.iloc[start_index:start_index + self.batch_size]

        # Obter os próximos 5 registros após o último registro do lote
        end_index = start_index + self.batch_size
        next_batch = self.df.iloc[end_index:end_index + self.next_records]

        # Agregar os próximos 5 registros em um único candle de 5 minutos
        next_candle = pd.DataFrame({
            'timestamp': [next_batch.iloc[0]['timestamp']],
            'open': [next_batch.iloc[0]['open']],
            'high': [next_batch['high'].max()],
            'low': [next_batch['low'].min()],
            'close': [next_batch.iloc[-1]['close']],
            'volume': next_batch['volume'].sum()
        })

        # Calcular a diferença entre o preço de fechamento do último candle do lote atual
        # e o preço máximo do próximo candle
        diff = batch.iloc[-1]['close'] - next_candle.iloc[0]['high']

        return batch, next_candle, diff

    def get_current_batch_with_next(self):
        start_index = self.current_index
        # Obter o lote atual
        batch = self.df.iloc[start_index:start_index + self.batch_size]

        # Obter os próximos N registros após o último registro do lote
        end_index = start_index + self.batch_size
        next_batch = self.df.iloc[end_index:end_index + self.next_records]

        # Agregar os próximos 5 registros em um único candle de 5 minutos
        next_candle = pd.DataFrame({
            'timestamp': [next_batch.iloc[0]['timestamp']],
            'open': [next_batch.iloc[0]['open']],
            'high': [next_batch['high'].max()],
            'low': [next_batch['low'].min()],
            'close': [next_batch.iloc[-1]['close']],
            'volume': next_batch['volume'].sum()
        })

        # Calcular a diferença entre o preço de fechamento do último candle do lote atual
        # e o preço máximo do próximo candle
        diff = batch.iloc[-1]['close'] - next_candle.iloc[0]['high']

        self.current_index += self.next_records + (self.batch_size - 1)
        #print("Candles {} de {}".format(self.current_index, self.total_records))

        return batch, next_candle, diff

    def get_random_batch_online(self):
        start_date = '2017-01-01'
        end_date = '2022-12-31'
        start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
        end_timestamp = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
        random_timestamp = random.randint(start_timestamp, end_timestamp)
        exchange = ccxt.binance()
        try:
            all_data = exchange.fetch_ohlcv('BTC/USDT', '1s', since=random_timestamp, limit=self.batch_size+self.next_records)
            # Cria um DataFrame pandas com os dados acumulados
            df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            batch = df.iloc[0:0 + self.batch_size]
            # Obter os próximos 5 registros após o último registro do lote
            end_index = 0 + self.batch_size
            next_batch = df.iloc[end_index:end_index + self.next_records]
            # Agregar os próximos 5 registros em um único candle de 5 minutos
            next_candle = pd.DataFrame({
                'timestamp': [next_batch.iloc[0]['timestamp']],
                'open': [next_batch.iloc[0]['open']],
                'high': [next_batch['high'].max()],
                'low': [next_batch['low'].min()],
                'close': [next_batch.iloc[-1]['close']],
                'volume': next_batch['volume'].sum()
            })
            self.count_excepts = 0
        except:
            self.count_excepts += 1
            print("Erro ao obter dados da corretora!\n\nContagem de erros capturados: {}".format(self.count_excepts))
            if self.count_excepts > 10:
                print("Máximo de tentativas alcançado!")
                return None, None
            time.sleep(1)
            batch, next_candle = self.get_random_batch_online()
            return batch, next_candle

        return batch, next_candle

    def get_current_batch_online(self, timestamp, window_size):
        #last_candle_timestamp = last_candle_df['timestamp'].iloc[-1]
        start_timestamp = timestamp + 1000  # Adicionar 1 segundo
        exchange = ccxt.binance()
        # Obtendo os dados
        batch = exchange.fetch_ohlcv('BTC/USDT', '1s', since=start_timestamp, limit=window_size)
        return batch

    def can_get_more_candles(self):
        #self.total_records - self.batch_size - self.next_records
        if (self.current_index + self.batch_size + self.next_records + 1) < self.total_records:
            return True
        else:
            return False



# Exemplo de uso
#loader = BatchLoader('../dataset/running_bts_1s.h5', batch_size=60, next_records=600)
#loader = BatchLoader(None, batch_size=300, next_records=600)
#batch, next_candle, diff = loader.get_random_batch_with_next()
#batch, next_candle = loader.get_random_batch_online()
#print("Batch:")
#print(batch)
#print("\nNext 10-minute candle:")
#print(next_candle)

#diff2 = next_candle.iloc[0]['high'] - batch.iloc[-1]['close']

#print("\nDiferença entre o preço de fechamento do último candle do lote atual e o preço máximo do próximo candle:")
#print(diff2)
#print("\nCompra")
#print(diff2*1)
#print("\nNão compra")
#print(diff2*(-1))

#batch_values = batch[['open', 'high', 'low', 'close', 'volume']].values.flatten().tolist()

#print(batch_values)