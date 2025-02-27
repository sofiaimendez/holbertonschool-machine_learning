#!/usr/bin/env python3
"""trains a model using mini-batch gradient descent:"""
import tensorflow.keras as K


def train_model(network, data, labels, batch_size, epochs,
                validation_data=None, early_stopping=False,
                patience=0, learning_rate_decay=False,
                alpha=0.1, decay_rate=1, save_best=False,
                filepath=None, verbose=True, shuffle=False):
    """model using mini-batch gradient descent:"""
    stopping = []
    if validation_data is not None:
        if early_stopping is True:
            stopping.append(K.callbacks.EarlyStopping(patience=patience))
        if learning_rate_decay is not None:
            stopping.append(K.callbacks.LearningRateScheduler(
                          schedule=lambda epoch:
                          alpha / (1 + decay_rate * epoch),
                          verbose=1))
        if save_best:
            stopping.append(K.callbacks.ModelCheckpoint(filepath=filepath,
                                                        save_best_only=True))
    iteration = network.fit(data, labels, batch_size=batch_size,
                            epochs=epochs,
                            verbose=verbose, shuffle=shuffle,
                            validation_data=validation_data,
                            callbacks=stopping)
    return iteration
