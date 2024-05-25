import gym
from stable_baselines3 import A2C
kwargs={}
env = gym.make('coinbot_env:CoinBot-v1', **kwargs)

model = A2C("MlpPolicy", env, verbose=1)
training_ts = 1000000
model.learn(total_timesteps=training_ts)
model.save("trained_models/A2C_{}ts".format(training_ts))