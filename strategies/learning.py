"""
NN functionality
"""
import os

import numpy as np
import sklearn.metrics as metrics
from keras.layers import Dense
from keras.models import Sequential
from matplotlib import pyplot as plt


# Creating the neural network and generating it's ROC curve
def neural_net(model_df):
    feature_list = [i for i in model_df.columns if i not in ['dealer_card',
                                                             'Y', 'loss',
                                                             'correct_action']]
    train_X = np.array(model_df[feature_list])
    train_Y = np.array(model_df['correct_action']).reshape(-1, 1)

    # Setting up a neural net with 5 layers
    model = Sequential()
    model.add(Dense(16))
    model.add(Dense(128))
    model.add(Dense(32))
    model.add(Dense(8))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='sgd')
    model.fit(train_X, train_Y, epochs=20, batch_size=256, verbose=1)

    Y_train_prediction = model.predict(train_X)
    pred = train_Y[:, -1]

    # Plotting the ROC curve metric
    fpr, tpr, threshold = metrics.roc_curve(pred, Y_train_prediction)
    roc_auc = metrics.auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(10, 8))
    plt.plot(fpr, tpr, label=('ROC AUC = %0.3f' % roc_auc))

    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    ax.set_xlabel("False Positive Rate", fontsize=16)
    ax.set_ylabel("True Positive Rate", fontsize=16)
    plt.setp(ax.get_legend().get_texts(), fontsize=16)

    if not os.path.exists(os.path.join("stats", "ml")):
        os.makedirs(os.path.join("stats", "ml"))
    plt.savefig(fname="stats\\ml\\roc_curve_blackjack", dpi=50)

    return model


# Decides action - hit or stand
def take_action(model, player_total, dealer_card_val, has_ace):
    input = np.array([player_total, 0, has_ace, dealer_card_val]).reshape(1, -1)
    predict = model.predict(input)
    if predict > 0.5:
        return "hit"
    return "stand"
