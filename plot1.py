import pandas as pd
import matplotlib.pyplot as plt

# Carregue os dados do arquivo h5
df = pd.read_hdf('dataset/btc_data_1m.h5', key='btc')

# Plot do valor de 'close'
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['close'], color='blue', linewidth=1)
plt.title('Valor de Fechamento do Bitcoin ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Valor de Fechamento (USD)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
