import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados dos arquivos HDF5
df1 = pd.read_hdf('dataset/btc_data_1s_partial.h5', key='btc')
df2 = pd.read_hdf('dataset/btc_data_1s_partial_2023_B.h5', key='btc')
df3 = pd.read_hdf('dataset/btc_data_1s_partial_2024.h5', key='btc')

# Função para exibir informações do DataFrame
def display_info(df, label):
    start_time = pd.to_datetime(df['timestamp'].iloc[0])
    end_time = pd.to_datetime(df['timestamp'].iloc[-1])
    print(f"{label}:")
    print(f"  - Total de registros: {df.shape[0]}")
    print(f"  - Timestamp inicial: {start_time}")
    print(f"  - Timestamp final: {end_time}")

# Exibir informações dos DataFrames individuais
display_info(df1, 'Arquivo 1 (btc_data_1s_partial.h5)')
display_info(df2, 'Arquivo 2 (btc_data_1s_partial_2023.h5)')
display_info(df3, 'Arquivo 3 (btc_data_1s_partial_2024.h5)')

# Concatenar os DataFrames
combined_df = pd.concat([df1, df2, df3])

# Remover duplicatas baseadas na coluna 'timestamp'
combined_df = combined_df.drop_duplicates(subset='timestamp')

# Classificar os dados pelo 'timestamp'
combined_df = combined_df.sort_values(by='timestamp')

# Exibir informações do DataFrame combinado
display_info(combined_df, 'Arquivo Combinado')

# Salvar o DataFrame combinado em um novo arquivo HDF5
combined_df.to_hdf('dataset/btc_data_1s_combined.h5', key='btc', mode='w')

print("Dados combinados salvos com sucesso!")

# Plotar os valores de 'close'
plt.figure(figsize=(15, 7))
plt.plot(combined_df['timestamp'], combined_df['close'], label='Close Price')
plt.xlabel('Timestamp')
plt.ylabel('Close Price')
plt.title('BTC/USDT Close Prices Over Time')
plt.legend()
plt.grid(True)
plt.show()
