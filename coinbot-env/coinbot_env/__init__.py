from gym.envs.registration import register

register(
    id='CoinBot-v1',
    entry_point='coinbot_env.envs:CoinBotEnv',
)

register(
    id='CoinBot-v2',
    entry_point='coinbot_env.envs:CoinBotEnvB',
)