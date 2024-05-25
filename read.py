import pandas as pd

# Caminho para o arquivo h5
file_path = 'dataset/btc_data_3m.h5'

# Carregue os dados do arquivo h5
df = pd.read_hdf(file_path, key='btc')

# Tamanho do lote
batch_size = 10
# Número de registros a serem lidos após cada lote
next_records = 5

# Índice inicial para iterar sobre o DataFrame
start_index = 0

# Iteração através dos dados em lotes de 10 registros
while start_index < len(df):
    # Obter o lote atual
    batch = df.iloc[start_index:start_index + batch_size]

    # Processamento ou manipulação dos dados do lote
    print("Batch:")
    print(batch)

    # Obter os próximos 5 registros após o último registro do lote
    end_index = start_index + batch_size
    next_batch = df.iloc[end_index:end_index + next_records]

    # Processamento ou manipulação dos próximos 5 registros
    print("Next 5 records:")
    print(next_batch)

    # Atualizar o índice inicial para o próximo lote
    start_index += batch_size

    break

