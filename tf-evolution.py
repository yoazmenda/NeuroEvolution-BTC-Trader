import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler

from population.population import Population
from population.network import Network
from data.data_util import BinanceAPI
from ta.ta import TA

# suppress tf GPU logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# for evaluating model fitness
def calculate_profit(trades, trade_prices):
    btc_wallet = 0.
    starting_cash = 100.
    usd_wallet = starting_cash
    fee = 0.001

    holding = False
    for idx, trade in enumerate(trades):
        if holding and not np.argmax(trade):
            holding = False
            usd_wallet = btc_wallet * trade_prices[idx] * (1 - fee)
        if not holding and np.argmax(trade):
            holding = True
            btc_wallet = usd_wallet / trade_prices[idx] * (1 - fee)

    return (usd_wallet / starting_cash - 1) * 100


if __name__ == '__main__':
    # inputs
    client = BinanceAPI(trading_pair='BTCUSDT')
    price_data = client.fetch_data(15, start='yesterday', save='data/historical_data.npy')
    ta = TA(price_data)
    inputs = np.transpose(np.array([ta.EMA(5).values, ta.DEMA(5).values]))
    valid_idx = ta.remove_NaN(inputs, price_data)
    inputs = StandardScaler().fit_transform(inputs[valid_idx:])
    price_data = price_data['close'][valid_idx:]

    # genetic parameters
    pop_size = 100
    w_mutation_rate = 0.05
    b_mutation_rate = 0.0
    mutation_scale = 0.3
    generations = 20

    # network parameters
    network_params = {
        'network': 'feedforward',
        'input': 2,
        'hidden': [16, 16],
        'output': 2
    }

    # build initial population
    pop = Population(network_params,
                     pop_size,
                     mutation_scale,
                     w_mutation_rate,
                     b_mutation_rate)

    # run for set number of generations
    for g in range(generations):
        pop.evolve(g)
        pop.run(inputs, price_data, fitness_callback=calculate_profit)
