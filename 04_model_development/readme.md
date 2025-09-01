#  Neural Network
### practice of cat vs dog model training
(Google Colab Note Book Link)[https://colab.research.google.com/drive/18wdw2TgaEr7zz7T7H1yqNgOdhFX4d-oh?usp=sharing]

# What is TensorFlow & Keras?
**TensorFlow:** A big framework that handles heavy math (matrix operations, GPU usage).
**Keras:** A friendly interface inside TensorFlow. Instead of writing 100 lines of math code, you write 10 lines in Keras.


# What is Sequential?
In Keras, models can be built in two main ways:
**Sequential Model** → Layers are stacked one after another (like a straight pipeline).
**Functional API** → More flexible (used for advanced models).

# Important Concepts in Neural Networks

**Layer:** Processes input data and passes it forward. Dense layer connects all neurons to the previous layer.

## Activation Function

Activation functions decide whether a neuron should “fire” or stay quiet based on the input.
Without activation functions, a neural network would just do linear calculations, which limits learning complex patterns.

### Common Activation Functions:

**ReLU (Rectified Linear Unit):**

Formula: f(x) = max(0, x)
Used in hidden layers. Turns negative numbers into 0 and keeps positive numbers.
Helps the network learn complex patterns.

**Softmax:**

Used in the output layer for classification problems.
Converts numbers into probabilities that sum to 1.
Example: [0.1, 0.9] → 10% cat, 90% dog.
---

**Loss Function:** Measures how wrong predictions are. Example: categorical_crossentropy for classification.

**Optimizer:** Updates weights to improve learning. Example: Adam.

**Epoch:** One full pass of the dataset through the network.

**Batch Size:** Number of samples processed before updating weights; helps save memory and speed up training.



(Neural Network Documentation)[https://docs.google.com/document/d/1BN4-8vTZ94PAot-5ZSufZ_yXAIe2epuxY_d3iu7lzlE/edit?usp=sharing]