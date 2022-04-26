"""
Machine learning strategy logic goes here
Create a separate function for this strategy if you feel the need
"""
import numpy as np
import sklearn.metrics as metrics
from keras.layers import Dense
from keras.models import Sequential
from matplotlib import pyplot as plt


def neural_net(model_df):
    feature_list = [i for i in model_df.columns if i not in ['dealer_card',
                                                             'Y', 'loss',
                                                             'correct_action']]
    print(feature_list)
    train_X = np.array(model_df[feature_list])
    train_Y = np.array(model_df['correct_action']).reshape(-1, 1)

    # Set up a neural net with 5 layers
    model = Sequential()
    model.add(Dense(16))
    model.add(Dense(128))
    model.add(Dense(32))
    model.add(Dense(8))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='sgd')
    model.fit(train_X, train_Y, epochs=20, batch_size=256, verbose=1)

    pred_Y_train = model.predict(train_X)
    actuals = train_Y[:, -1]

    fpr, tpr, threshold = metrics.roc_curve(actuals, pred_Y_train)
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

    plt.savefig(fname="stats\\ml\\roc_curve_blackjack", dpi=100)

    return model


def take_action(model, player_total, dealer_card_val, has_ace):
    input = np.array([player_total, 0, has_ace, dealer_card_val]).reshape(1, -1)
    predict = model.predict(input)
    if predict > 0.5:
        return "hit"
    return "stand"
