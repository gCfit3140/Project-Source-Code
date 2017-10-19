import numpy as np
import pickle
import dataAnalysis as dA

# The Artificial Neural Network code is based of https://beckernick.github.io/neural-network-scratch/

def relu_activation(data_array):
    return np.maximum(data_array, 0)


def softmax(output_array):
    logits_exp = np.exp(output_array)
    return logits_exp / np.sum(logits_exp, axis=1, keepdims=True)


def predict(data, weight1, weight2, bias1, bias2):
    input_layer = np.dot(data, weight1)
    hidden_layer = relu_activation(input_layer + bias1)
    scores = np.dot(hidden_layer, weight2) + bias2
    scores = np.round(softmax(scores), 3)
    return scores


# load the trained weight of the NN
def load():
    with open('weight1', 'rb') as w1:
        weight1 = pickle.load(w1)
    with open('weight2', 'rb') as w2:
        weight2 = pickle.load(w2)
    with open('bias1', 'rb') as b1:
        bias1 = pickle.load(b1)
    with open('bias2', 'rb') as b2:
        bias2 = pickle.load(b2)
    print("Loaded all required model attributes successfully!")
    return weight1, weight2, bias1, bias2


# run the NN model
def menu(region=None, year=None):
    inputData = dA.start(region, year)
    required = [inputData[0][1], inputData[1][1], inputData[2][1], inputData[3]]
    stored = load()
    result = predict(required, stored[0], stored[1], stored[2],stored[3])
    print(result)
    return result.tolist(), inputData
