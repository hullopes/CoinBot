import gym
from stable_baselines3 import DQN
import numpy as np

kwargs = {
    'batch_size': 60,
    'next_records': 600
}
env = gym.make('coinbot_env:CoinBot-v2', **kwargs)

modelName = "envB_DQN"
model = DQN("MlpPolicy", env, verbose=1)
training_ts = 20000
model.learn(total_timesteps=training_ts)
model.save("trained_models/{}_{}ts".format(modelName, training_ts))
hist = env.get_history()
#print(hist)
# Salvando a lista em um arquivo de texto
#np.savetxt("training_hist/hist_{}_{}_ts.txt".format(modelName, training_ts), hist)

# Convertendo a lista em uma string formatada
rws_str = str(hist)

# Salvando a string no arquivo de texto
with open("training_hist/hist_{}_{}_ts.txt".format(modelName, training_ts), 'w') as f:
    f.write(rws_str)
