import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from constants import DEALER_UP_CARD_FEATURE, PLAYER_HAND_FEATURE, PLAYER_RESULT_FEATURE, \
    PLAYER_CURRENT_TOTAL, PLAYER_CURRENT_ACTION
from constants import NUM_SIMULATIONS


def generate_stats(strategy_name):
    model_df = generate_model()
    if not os.path.exists(os.path.join("stats", strategy_name)):
        os.makedirs(os.path.join("stats", strategy_name))
    stats_folder = os.path.join("stats", strategy_name)
    plot_win_vs_dealer_up_card(model_df, stats_folder)
    plot_win_vs_player_hand(model_df, stats_folder)
    plot_player_hand_vs_dealer_up_card(model_df, stats_folder)


def plot_win_vs_dealer_up_card(model_df, stats_folder):
    data = 1 - (model_df.groupby(by='dealer_card').sum()['loss'] /
                model_df.groupby(by='dealer_card').count()['loss'])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.barplot(x=data.index,
                     y=data.values)
    ax.set_xlabel("Dealer's Card", fontsize=16)
    ax.set_ylabel("Probability of Tie or Win", fontsize=16)

    plt.tight_layout()
    plt.savefig(fname=os.path.join(stats_folder, 'dealer_card_probs'), dpi=100)


def plot_win_vs_player_hand(model_df, stats_folder):
    data = 1 - (model_df.groupby(by='player_total_initial').sum()['loss'] /
                model_df.groupby(by='player_total_initial').count()['loss'])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.barplot(x=data[:-1].index,
                     y=data[:-1].values)
    ax.set_xlabel("Player's Hand Value", fontsize=16)
    ax.set_ylabel("Probability of Tie or Win", fontsize=16)

    plt.tight_layout()
    plt.savefig(fname=os.path.join(stats_folder, 'player_hand_probs'), dpi=100)


def plot_player_hand_vs_dealer_up_card(model_df, stats_folder):
    pivot_data = model_df[model_df['player_total_initial'] != 21]

    losses_pivot = pd.pivot_table(pivot_data, values='loss',
                                  index=['dealer_card_num'],
                                  columns=['player_total_initial'],
                                  aggfunc=np.sum)

    games_pivot = pd.pivot_table(pivot_data, values='loss',
                                 index=['dealer_card_num'],
                                 columns=['player_total_initial'],
                                 aggfunc='count')

    heat_data = 1 - losses_pivot.sort_index(ascending=False) / games_pivot.sort_index(ascending=False)

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.heatmap(heat_data, square=False, cmap="PiYG")

    ax.set_xlabel("Player's Hand Value", fontsize=16)
    ax.set_ylabel("Dealer's Card", fontsize=16)

    plt.savefig(fname=os.path.join(stats_folder, 'heat_map_random'), dpi=100)


def plot_chart(win_rates, stats_folder):
    plt.style.use('ggplot')
    plt.figure(figsize=(12, 6))

    plt.plot(range(NUM_SIMULATIONS), win_rates)
    plt.title("Blackjack Probability")
    plt.ylabel("Win rate")
    plt.xlabel("Games Played")
    plt.ylim([0, 100])
    plt.xlim([0, NUM_SIMULATIONS])
    plt.savefig(fname=os.path.join(stats_folder, 'player_win_rate'), dpi=100)


def generate_model():
    model_df = pd.DataFrame()
    model_df['dealer_card'] = DEALER_UP_CARD_FEATURE
    model_df['player_total_initial'] = [hand.get_initial_hand_total() for hand in PLAYER_HAND_FEATURE]
    model_df['Y'] = [res[0] for res in PLAYER_RESULT_FEATURE]
    model_df['hit?'] = PLAYER_CURRENT_ACTION

    loss = []
    for res in model_df['Y']:
        if res == -1:
            loss.append(1)
        else:
            loss.append(0)
    model_df['loss'] = loss

    has_ace = []
    for hand in PLAYER_HAND_FEATURE:
        if 'A' in [card.get_face() for card in hand.hand_cards]:
            has_ace.append(1)
        else:
            has_ace.append(0)
    model_df['has_ace'] = has_ace

    dealer_card_num = []
    for d_card in model_df['dealer_card']:
        if d_card == 'A':
            dealer_card_num.append(11)
        else:
            dealer_card_num.append(d_card)
    model_df['dealer_card_num'] = dealer_card_num

    correct = []
    for i, val in enumerate(model_df['loss']):
        if val == 1:
            if PLAYER_CURRENT_ACTION[i] == 1:
                correct.append(0)
            else:
                correct.append(1)
        else:
            if PLAYER_CURRENT_ACTION[i] == 1:
                correct.append(1)
            else:
                correct.append(0)
    model_df['correct_action'] = correct

    return model_df
