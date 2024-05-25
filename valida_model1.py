import gym
from stable_baselines3 import DQN, A2C
import numpy as np

from model.utils import BatchLoader

kwargs = {
    'batch_size': 60,
    'next_records': 15
}
env = gym.make('coinbot_env:CoinBot-v1', **kwargs)

model_name = "A2C_400000ts"
model = A2C("MlpPolicy", env, verbose=1)
model.load("trained_models/"+model_name)

carteira = 1000
carteira_i = carteira
actions = [-1, 1]
gains_losses = []

loader = BatchLoader('dataset/btc_data_1m_new.h5', batch_size=kwargs['batch_size'], next_records=kwargs['next_records'])
while True:
    if loader.can_get_more_candles():
        batch, next_candle, diff = loader.get_current_batch_with_next()
        obs = batch[['open', 'high', 'low', 'close', 'volume']].values.flatten().tolist()
        ac, _ = model.predict(obs)
        action = actions[ac]
        if action == 1:
            ## avaliando gain/loss
            close_last_candle = batch.iloc[-1]['close']
            high_next_candle = next_candle.iloc[0]['high']
            diff_percent = ((high_next_candle - close_last_candle) / close_last_candle)
            gains_losses.append(diff_percent * 100)
            carteira = carteira * (1 + diff_percent)
    else:
        break

print("Resultado:\n\n")
print("US$ {} investidos - Saldo: US$ {}".format(carteira_i, carteira))
#print(gains_losses)
print("Ganhos:: {}".format(len([gain_loss for gain_loss in gains_losses if gain_loss >= 0])))
print("Perdas:: {}".format(len([gain_loss for gain_loss in gains_losses if gain_loss < 0])))
# Salvando a string no arquivo de texto
with open("validation_hist/gain_{}.txt".format(model_name), 'w') as f:
    f.write(str(gains_losses))