## New environment

* This is a Gym environment for RAN problem.

* This environment was built according to https://github.com/openai/gym/blob/master/docs/creating-environments.md

``
env = gym.make('mpp_ran_env:mpp-ran-v0') # for 1 env
env = make_vec_env("sra_env:mpp-ran-v0", n_envs=4) # for 4 envs - multiprocessing
``

#### Installing

```sh
pip install -e ran-env
```