#!/usr/bin/env python3
"""creates a sparse autoencoder:"""
import tensorflow.keras as keras


def autoencoder(input_dims, hidden_layers, latent_dims, lambtha):
    """creates a sparse autoencoder:"""
    L1 = keras.regularizers.l1(lambtha)
    X_inputs = keras.Input(shape=(input_dims,))
    hidden_ly = keras.layers.Dense(units=hidden_layers[0], activation='relu')
    Y_prev = hidden_ly(X_inputs)
    for i in range(1, len(hidden_layers)):
        hidden_ly = keras.layers.Dense(units=hidden_layers[i],
                                       activation='relu')
        Y_prev = hidden_ly(Y_prev)
    latent_ly = keras.layers.Dense(units=latent_dims, activation='relu',
                                   activity_regularizer=L1)
    bottleneck = latent_ly(Y_prev)
    encoder = keras.Model(X_inputs, bottleneck)
    X_decode = keras.Input(shape=(latent_dims,))
    hidden_ly = keras.layers.Dense(units=hidden_layers[-1], activation='relu')
    Y_prev = hidden_ly(X_decode)
    for j in range(len(hidden_layers) - 2, -1, -1):
        hidden_d = keras.layers.Dense(units=hidden_layers[j],
                                      activation='relu')
        Y_prev = hidden_d(Y_prev)
    last_layer = keras.layers.Dense(units=input_dims, activation='sigmoid')
    output = last_layer(Y_prev)
    decoder = keras.Model(X_decode, output)
    X_input = keras.Input(shape=(input_dims,))
    e_output = encoder(X_input)
    d_output = decoder(e_output)
    autoencoder = keras.Model(X_input, d_output)
    autoencoder.compile(loss='binary_crossentropy', optimizer='adam')
    return encoder, decoder, autoencoder
