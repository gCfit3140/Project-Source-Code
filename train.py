import numpy as np
import pickle

# The Artificial Neural Network code is based of https://beckernick.github.io/neural-network-scratch/

# get the training input & output data
with open('trainInput', 'rb') as f1:
    trainInput = pickle.load(f1)
    trainInput = np.array(trainInput)
    print(trainInput[17:20])
with open('trainOutput', 'rb') as f2:
    trainOutput = pickle.load(f2)
    trainOutput = np.array(trainOutput)
    print(trainOutput[17:20])
# get the testing input & output data
with open('testInput', 'rb') as f3:
    testInput = pickle.load(f3)
    testInput = np.array(testInput)
    print(testInput[:3])
with open('testOutput', 'rb') as f4:
    testOutput = pickle.load(f4)
    testOutput = np.array(testOutput)
    print(testOutput[:3])


# activate function, make output=0 if input<0 and output=input if input>0
def relu_activation(inputArray):
    return np.maximum(inputArray, 0)


# average loss over the loss for every input
def cross_entropy_softmax_loss_array(probabilityArray, label):
    indices = np.argmax(label, axis=1).astype(int)
    predicted_probability = probabilityArray[np.arange(len(probabilityArray)), indices]
    log_preds = np.log(predicted_probability)
    loss = -1.0 * np.sum(log_preds) / len(log_preds)
    return loss


# calculate regularization loss (and avoid over fitting)
def regularization_L2_softmax_loss(reg_lambda, weight1, weight2):
    weight1_loss = 0.5 * reg_lambda * np.sum(weight1 * weight1)
    weight2_loss = 0.5 * reg_lambda * np.sum(weight2 * weight2)
    return weight1_loss + weight2_loss


# get the probability distribution over possible choices
def softmax(output_array):
    logits_exp = np.exp(output_array)
    return logits_exp / np.sum(logits_exp, axis=1, keepdims=True)


# use the neural network to train using the training
def train(weight1=None, weight2=None, bias1=None, bias2=None):

    # assign input and output training data
    training_data = trainInput
    training_labels = trainOutput
    # assign input and output testing data
    testing_data = testInput
    testing_labels = testOutput

    # define number of hidden nodes
    hidden_nodes = 3
    num_labels = training_labels.shape[1]
    num_features = training_data.shape[1]
    learning_rate = .01
    reg_lambda = .01

    # check if there has been trained weights and bias
    if bias1 is not None and bias2 is not None:
        layer1_weights_array = weight1
        layer2_weights_array = weight2
        layer1_biases_array = bias1
        layer2_biases_array = bias2
    else:
        # generate random weights and bias if no stored ones
        layer1_weights_array = np.random.normal(0, 1, [num_features, hidden_nodes])
        layer2_weights_array = np.random.normal(0, 1, [hidden_nodes, num_labels])
        layer1_biases_array = np.zeros((1, hidden_nodes))
        layer2_biases_array = np.zeros((1, num_labels))

    # use a loop to train the model
    for step in range(5001):
        # feed forward the input data
        inputLayer = np.dot(training_data, layer1_weights_array)
        hiddenLayer = relu_activation(inputLayer + layer1_biases_array)
        outputLayer = np.dot(hiddenLayer, layer2_weights_array) + layer2_biases_array
        output = softmax(outputLayer)

        # calculate the loss during this iteration
        loss = cross_entropy_softmax_loss_array(output, training_labels)
        loss += regularization_L2_softmax_loss(reg_lambda, layer1_weights_array, layer2_weights_array)
        output_error_signal = (output - training_labels) / output.shape[0]
        error_signal_hidden = np.dot(output_error_signal, layer2_weights_array.T)
        error_signal_hidden[hiddenLayer <= 0] = 0

        # adjust the weights and bias using the error/loss
        gradient_layer2_weights = np.dot(hiddenLayer.T, output_error_signal)
        gradient_layer2_bias = np.sum(output_error_signal, axis=0, keepdims=True)
        gradient_layer1_weights = np.dot(training_data.T, error_signal_hidden)
        gradient_layer1_bias = np.sum(error_signal_hidden, axis=0, keepdims=True)
        gradient_layer2_weights += reg_lambda * layer2_weights_array
        gradient_layer1_weights += reg_lambda * layer1_weights_array
        layer1_weights_array -= learning_rate * gradient_layer1_weights
        layer1_biases_array -= learning_rate * gradient_layer1_bias
        layer2_weights_array -= learning_rate * gradient_layer2_weights
        layer2_biases_array -= learning_rate * gradient_layer2_bias

        # print error/loss every 1000 iterations
        if step % 1000 == 0:
                print('Loss at step {0}: {1}'.format(step, loss))

    # use the trained model to predict the training dataset for accuracy checking
    inputLayer = np.dot(training_data, layer1_weights_array)
    hiddenLayer = relu_activation(inputLayer + layer1_biases_array)
    scores = np.dot(hiddenLayer, layer2_weights_array) + layer2_biases_array
    probs = softmax(scores)
    print(np.round(probs[17:20], 3))
    print('Train accuracy: {0}%'.format(accuracy(probs, training_labels)))

    # use the trained model to predict the testing dataset for accuracy checking
    inputLayer = np.dot(testing_data, layer1_weights_array)
    hiddenLayer = relu_activation(inputLayer + layer1_biases_array)
    scores = np.dot(hiddenLayer, layer2_weights_array) + layer2_biases_array
    probs = softmax(scores)
    print(np.round(probs[:3], 3))
    print('Test accuracy: {0}%'.format(accuracy(probs, testing_labels)))

    # returning model attributes which needed to be stored
    return layer1_weights_array, layer2_weights_array, layer1_biases_array, layer2_biases_array


# checking accuracy
def accuracy(predictions, labels):
    # as long as the highest probability in prediction and label have the same indices
    # it will be counted as one correct prediction
    corrects = np.argmax(predictions, 1) == np.argmax(labels, 1)
    totalCorrect = np.sum(corrects)
    # convert to %
    accuracy = 100.0 * totalCorrect / predictions.shape[0]
    return accuracy


# save the trained weight of the NN
def save(weight1, weight2, bias1, bias2):
    with open('weight1', 'wb') as w1:
        pickle.dump(weight1, w1)
    with open('weight2', 'wb') as w2:
        pickle.dump(weight2, w2)
    with open('bias1', 'wb') as b1:
        pickle.dump(bias1, b1)
    with open('bias2', 'wb') as b2:
        pickle.dump(bias2, b2)
    '''
    print("-----------------------------------------------------------------------------------------------------------")
    print("Saved successfully! The weights and bias are shown below:")
    print(weight1)
    print(weight2)
    print(bias1)
    print(bias2)'''


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
    '''
    print("-----------------------------------------------------------------------------------------------------------")
    print("Loaded all required model attributes successfully!")
    print(weight1)
    print(weight2)
    print(bias1)
    print(bias2)'''
    return weight1, weight2, bias1, bias2


# menu to use the training model
def start():
    stored = load()
    results = train(stored[0], stored[1], stored[2],stored[3])
    save(results[0], results[1], results[2], results[3])

start()
