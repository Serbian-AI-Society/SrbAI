from typing import Tuple, Dict, Callable, List
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt
import tqdm

from globals import ModelConfig
from text_preprocessing import word_to_vector, make_context_matrix


def relu(tensor: np.ndarray) -> np.ndarray:
    """
    Does the relu function.
    f(x) = max(0, x)
    """
    return tensor * (tensor > 0.0)


def relu_derivative(tensor: np.ndarray) -> np.ndarray:
    """
    Does the derivative of relu
    """
    return 1.0 * (tensor > 0.0)


def tanh(tensor: np.ndarray) -> np.ndarray:
    """
    Does the hyperbolic tan elementwise on tensor
    """
    return np.tanh(tensor)


def tanh_derivative(tensor: np.ndarray) -> np.ndarray:
    """
    Does the derivative of tanh
    """
    return 1 - tanh(tensor) ** 2


def identity(tensor: np.ndarray) -> np.ndarray:
    """
    Does the y = x function on a tensor
    """
    return tensor


def identity_derivative(tensor: np.ndarray) -> np.ndarray:
    """
    Does the derivative of the identity function
    """
    return np.ones_like(tensor)


def softmax(tensor: np.ndarray) -> np.ndarray:
    """
    Does the safe softmax function with numerical stability
    """
    mxs = np.max(tensor, axis=1).reshape(-1, 1)
    exps = np.exp(tensor - mxs)

    sums = np.sum(exps, axis=1).reshape(-1, 1)

    return exps / sums


def make_network_hyperparameters(
    input_size: int, vector_space_size: int, output_size: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Initializes random weights and biases for the network
    Returns a pair of weights, input-hidden and hidden-output
    """
    input_2_hidden = np.random.uniform(-1, 1, size=(input_size, vector_space_size))
    hidden_2_output = np.random.uniform(-1, 1, size=(vector_space_size, output_size))
    return input_2_hidden, hidden_2_output


def forward_one_word(
    word_vector: np.ndarray,
    network_hyperparams: Tuple[np.ndarray, np.ndarray],
    activation: Callable[[np.ndarray], np.ndarray],
) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """
    Does the forward pass for one word of the network.
    Network hyperparameters are in a tuple of input to hidden and hidden to output weights

    Returns a tuple with all the transfer and activation pairs (in order of layers),
    with the last layers' activation being the output
    """
    input_2_hidden_weights, hidden_2_output_weights = network_hyperparams

    input_2_hidden_transfer = word_vector @ input_2_hidden_weights
    input_2_hidden_activation = activation(input_2_hidden_transfer)

    hidden_2_output_transfer = input_2_hidden_activation @ hidden_2_output_weights
    hidden_2_output_activation = softmax(hidden_2_output_transfer)

    return (input_2_hidden_transfer, input_2_hidden_activation), (
        hidden_2_output_transfer,
        hidden_2_output_activation,
    )


def backward_one_word(
    word_vector: np.ndarray,
    context_matrix: np.ndarray,
    forward_results: Tuple[
        Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]
    ],
    network_hyperparams: Tuple[np.ndarray, np.ndarray],
    activation_derivative: Callable[[np.ndarray], np.ndarray],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Takes the word vector it's working on currently, as well as its context.
    Also, the results for all steps in the forward pass and the weights for each layer

    Returns gradients for the network hyperparameters in the order of layers
    """
    _, hidden_2_output_weights = network_hyperparams
    (input_2_hidden_transfer, input_2_hidden_activation), (
        _,
        hidden_2_output_activation,
    ) = forward_results

    grad_hidden_2_output_transfer = (
        np.sum(hidden_2_output_activation - context_matrix, axis=0, keepdims=True)
        / context_matrix.shape[0]
    )
    grad_hidden_2_output_weights = (
        input_2_hidden_activation.T @ grad_hidden_2_output_transfer
    )

    grad_input_2_hidden_activation = (
        grad_hidden_2_output_transfer @ hidden_2_output_weights.T
    )
    grad_input_2_hidden_transfer = (
        grad_input_2_hidden_activation * activation_derivative(input_2_hidden_transfer)
    )
    grad_input_2_hidden_weights = word_vector.T @ grad_input_2_hidden_transfer

    return grad_input_2_hidden_weights, grad_hidden_2_output_weights


def loss_one_word(word_output: np.ndarray, context_matrix: np.ndarray) -> float:
    """
    Calculates log loss for a single word based on its output and context
    """
    loss = np.sum(-1 * (context_matrix * np.log(word_output)))
    return loss / context_matrix.shape[0]


def update_hyperparameter(
    hyperparameter: np.ndarray,
    grad_hyperparameter: np.ndarray,
    m: np.ndarray,
    v: np.ndarray,
    optimizer_params: Dict[str, float],
    learn_rate: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Does ADAM optimization on hyperparameter

    Returns the newly calculated hyperparameter and optimizer parameters
    """
    new_m = (
        optimizer_params["omega1"] * m
        + (1 - optimizer_params["omega1"]) * grad_hyperparameter
    )
    new_v = optimizer_params["omega2"] * v + (1 - optimizer_params["omega2"]) * (
        grad_hyperparameter**2
    )

    m_hat = new_m / (1 - optimizer_params["omega1"])
    v_hat = np.abs(new_v) / (1 - optimizer_params["omega2"])

    new_hyperparameter = (
        hyperparameter
        - (learn_rate / (v_hat + optimizer_params["norm"]) ** 0.5) * m_hat
    )
    return new_hyperparameter, new_m, new_v


def one_word_iteration(
    word_vector: np.ndarray,
    context_matrix: np.ndarray,
    network_hyperparameters: Tuple[np.ndarray, np.ndarray],
    ms: Tuple[np.ndarray, np.ndarray],
    vs: Tuple[np.ndarray, np.ndarray],
    optimizer_params: Dict[str, float],
    learn_rate: float,
) -> Tuple[
    Tuple[np.ndarray, np.ndarray],
    float,
    Tuple[np.ndarray, np.ndarray],
    Tuple[np.ndarray, np.ndarray],
]:
    """
    Does forward pass, loss calculation, backward pass and hyperparameter optimization for one word

    Returns the new hyperparameters and loss for that word, as well as the newly calculated optimizer parameters
    """
    forward_results = forward_one_word(word_vector, network_hyperparameters, tanh)

    _, (_, hidden_2_output_activation) = forward_results
    loss = loss_one_word(hidden_2_output_activation, context_matrix)

    grad_hyperparameters = backward_one_word(
        word_vector,
        context_matrix,
        forward_results,
        network_hyperparameters,
        tanh_derivative,
    )

    input_2_hidden_updated, hidden_2_output_updated = tuple(
        update_hyperparameter(
            hyperparameter, grad_hyperparameter, m, v, optimizer_params, learn_rate
        )
        for hyperparameter, grad_hyperparameter, m, v in zip(
            network_hyperparameters, grad_hyperparameters, ms, vs
        )
    )

    return (
        (input_2_hidden_updated[0], hidden_2_output_updated[0]),
        loss,
        (input_2_hidden_updated[1], hidden_2_output_updated[1]),
        (input_2_hidden_updated[2], hidden_2_output_updated[2]),
    )


def train(
    word_map: Dict[str, Dict[str, List[int]]],
    ngram_vector_map: Dict[str, int],
    word_vector_map: Dict[str, int],
    model_config: ModelConfig,
    plot_graph: bool = False,
) -> np.ndarray:
    """
    Given a word map with input vectors and their context vectors, embeds the vector space.
    plot_graph - whether to plot the loss graph
    """
    words = [*word_map.keys()]
    hyperparameters = make_network_hyperparameters(
        len(ngram_vector_map),
        model_config.vector_space_size,
        len(word_vector_map),
    )

    total_loss = []
    for _ in tqdm.tqdm(range(model_config.epochs)):
        epoch_loss = 0.0
        ms = vs = (0.0, 0.0)

        np.random.shuffle(words)
        for word in words:
            word_dict = itemgetter(word)(word_map)
            word_vector = word_to_vector(word_dict["input"], ngram_vector_map)
            word_context = make_context_matrix(word_dict["context"], word_vector_map)

            hyperparameters, word_loss, ms, vs = one_word_iteration(
                word_vector, word_context, hyperparameters, ms, vs, model_config.optimizer, model_config.learn_rate
            )
            epoch_loss += word_loss

        total_loss.append(epoch_loss)

    if plot_graph:
        plt.plot(total_loss)
        plt.show()

    return hyperparameters[0]
