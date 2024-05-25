import time
import gym
import json
from gym import error, spaces, utils
import numpy as np
import os
from model.utils import BatchLoader


class CoinBotEnv(gym.Env):

    def __init__(self, **kwargs):
        batch_size = 10
        next_records = 5
        if len(kwargs) > 0 and kwargs['batch_size']:
            batch_size = kwargs['batch_size']
        if len(kwargs) > 0 and kwargs['next_records']:
            next_records = kwargs['next_records']
        ## obtendo o loader de amostras
        self.loader = BatchLoader('dataset/btc_data_1m.h5', batch_size=batch_size, next_records=next_records)
        ## obtendo uma amostra
        self.batch, self.next_candle, diff = self.loader.get_random_batch_with_next()
        batch_values = self.batch[['open', 'high', 'low', 'close', 'volume']].values.flatten().tolist()
        self.observation_space = batch_values

        # -1 não compra; +1 compra
        self.actions = [-1, 1]

        self.end_ep = False
        self.debug = 0

        ## inicializando o dataset
        ## vamos olhar para 1m, e medir a qualidade pelo 5m (próximo candle)

        self.action_space = spaces.Discrete(len(self.actions))
        # CRIANDO ESPAÇO DE OBSERVAÇÃO
        self.observation_space = spaces.Box(low=0, high=100000, shape=(len(batch_values),), dtype=float)

        self.rewards = []
        self.rewards_all = []
        self.ep_rewards = []
        self.ep_buy_acts = []

    def reset(self):  # Required by script to initialize the observation space
        self.end_ep = False
        self.observation_space = self.update_obs()
        print("\n Tamanho do episódio: {}".format(len(self.ep_rewards)))
        print(":::Média de rws do episódio: {}, Soma: {} ".format(np.mean(self.ep_rewards), np.sum(self.ep_rewards)))
        self.rewards_all.append(np.sum(self.ep_rewards))
        print(":::Média de rws: {}, Soma: {} ".format(np.mean(self.rewards_all), np.sum(self.rewards_all)))
        self.ep_rewards = []
        print("... total de ações de compra com ganhos no ep: {}".format(len(self.ep_buy_acts)))
        self.ep_buy_acts = []
        return self.observation_space

    def step(self, action_index):

        action = self.actions[action_index]
        diff2 = self.next_candle.iloc[0]['high'] - self.batch.iloc[-1]['close']
        close_last_candle = self.batch.iloc[-1]['close']
        high_next_candle = self.next_candle.iloc[0]['high']
        diff_percent = ((high_next_candle - close_last_candle) / close_last_candle) * 100

        #if diff_percent < 0.5 and action == -1:
        #    diff_percent *= 10

        # if action == 1:  # Se a ação for comprar
        #     if diff_percent > 0.2:  # Se a porcentagem de alta for superior a 0.2%
        #         if diff_percent > 1:
        #             reward = diff_percent * 10
        #         else:
        #             reward = 1  # Recompensa positiva para uma compra bem-sucedida
        #     else:
        #         reward = -1  # Penalização por comprar em um cenário desfavorável
        # else:  # Se a ação for não comprar
        #     if diff_percent > 0.2:  # Se a porcentagem de alta for superior a 0.2%
        #         # Penalização por não comprar em um cenário favorável
        #         if diff_percent > 1:
        #             reward = diff_percent * -10
        #         else:
        #             reward = -1
        #     else:
        #         # Recompensa positiva por não comprar em um cenário desfavorável
        #         if diff_percent < -1:
        #             reward = diff_percent * 10
        #         else:
        #             reward = 1

        if action == 1:
            if diff_percent > 0.1:
                reward = 10 * (1 + diff_percent)
                ## mandou comprar, e era de fato bom momento -> recompensa
            else:
                reward = -1 * (1 + diff_percent)
                ## mandou compar, mas caiu -> penaliza
        else:
            if diff_percent > 0.5:
                reward = -10 * (1 + diff_percent)
                ## mandou não comprar, mas deveria ter comprado -> penaliza
            else:
                reward = 1 * (1 + diff_percent)
                ## mandou não comprar, e caiu -> recompensa
        self.ep_rewards.append(reward)
        #reward = diff2 * action
        #reward = diff_percent * action

        #self.ep_rewards.append(reward)

        info = {}
        ## fechamos um episódio assim que tomar loss
        if reward < 0:
            self.end_ep = True
            info['is_success'] = False
        else:
            if action > 0:
                self.ep_buy_acts.append(1)
            info['is_success'] = True
            self.end_ep = False
            ## forçando uma atualização da observação
            self.observation_space = self.update_obs()

        ##self.rewards.append(reward)
        return self.observation_space, reward, self.end_ep, info

    def render(self):
        pass

    def update_obs(self):
        self.batch, self.next_candle, diff = self.loader.get_random_batch_with_next()
        batch_values = self.batch[['open', 'high', 'low', 'close', 'volume']].values.flatten().tolist()
        return batch_values

    def get_history(self):
        return self.rewards_all