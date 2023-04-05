import re
import string
from typing import List, Dict, Tuple
from operator import itemgetter

import numpy as np

from globals import ModelConfig, LanguageConfig
from io_utils import open_corpus


def remove_white_space(text: str) -> str:
    """
    Removes multiple occurrences of space, newlines, return lines with a single space
    """
    cleaned_text = re.sub(r"(\s+|\n+|\r+)", " ", text)
    return cleaned_text


def remove_numbers(text: str) -> str:
    """
    Removes all numbers in text
    """
    cleaned_text = re.sub(r"[0-9]+", " ", text)
    return cleaned_text


def remove_punctuation(text: str) -> str:
    """
    Removes all occurrences of punctuation
    """
    cleaned_text = text.translate(str.maketrans("", "", string.punctuation))
    return cleaned_text


def to_lowercase(text: str) -> str:
    """
    Turns all words into lowercase
    """
    return text.lower()


def clean_text(text: str) -> str:
    """
    Cleans text using above functions
    """
    no_whitespace = remove_white_space(text)
    no_numbers = remove_numbers(no_whitespace)
    no_punctuation = remove_punctuation(no_numbers)
    lowercase = to_lowercase(no_punctuation)
    return lowercase


def make_word_list(text: str) -> List[str]:
    """
    Makes a list from single whitespace separated text
    """
    split_text = text.split(" ")
    return [word for word in split_text if word != ""]


def remove_stopwords(word_list: List[str], stopwords_path: str) -> List[str]:
    """
    Removes all stopwords from text.
    Stopwords path is the path to the comma separated stopwords.
    """
    # preprocess stopwords
    with open(stopwords_path, "r", encoding="utf-8") as f:
        stopwords = f.read()
    stopwords = stopwords.split(",")

    word_list = [word for word in word_list if word not in stopwords]
    return word_list


def make_ngram_map(word_list: List[str], ngram_size: int) -> Dict[str, List[str]]:
    """
    Makes a map of all the words and their ngrams given a list of words.
    Inside the list of ngrams is also the word itself as a ngram (as per facebook docs)
    """
    ngram_map = {}
    for word in word_list:
        ngram_map[word] = [
            word[i : i + ngram_size] for i in range(0, len(word) - (ngram_size - 1))
        ]
        ngram_map[word].append(word)
        word_list = [other_word for other_word in word_list if other_word != word]

    return ngram_map


def make_context_map(
    word_list: List[str],
    left_context_window: int,
    right_context_window: int,
    self_context: bool,
) -> Dict[str, List[str]]:
    """
    Makes a map of the context of a single word given how far left and right the context stretches.
    The word itself is inside its own context.
    """
    context_map = {}

    for i, word in enumerate(word_list):
        temp_left_context_window = left_context_window if i > left_context_window else i

        if word not in context_map:
            context_map[word] = word_list[
                i - temp_left_context_window : i + right_context_window + 1
            ]
        else:
            context_map[word].extend(
                word_list[i - temp_left_context_window : i + right_context_window + 1]
            )

        if not self_context:
            context_map[word].remove(word)

        # removes duplicates, but could be slow
        context_map[word] = list(set(context_map[word]))

    return context_map


def make_ngram_vector_map(ngram_map: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Makes a vector for each ngram and maps the ngram to that vector.
    """
    # python magic. list of lists -> list of all elements using iterators
    all_ngrams = [ngram for ngram_list in [*ngram_map.values()] for ngram in ngram_list]
    unique_ngrams = np.unique(all_ngrams)

    ngram_vector_map = {}
    for i, ngram in enumerate(unique_ngrams):
        ngram_vector_map[ngram] = i

    return ngram_vector_map


def make_word_vector_map(word_list: List[str]) -> Dict[str, int]:
    """
    Given the list of words, one hot encodes them all
    """
    unique_words = np.unique(word_list)

    word_vector_map = {}
    for i, word in enumerate(unique_words):
        word_vector_map[word] = i

    return word_vector_map


def _spawn_one_hot_encoded_vector(vector_size: int, one_index: int) -> np.ndarray:
    """
    Given the size of the vector and the index of the 1 returns a one hot encoded vector
    """
    ohe_vec = np.zeros(shape=(1, vector_size))
    ohe_vec[0, one_index] = 1.0
    return ohe_vec


def word_to_vector(
    ngram_list: List[int], ngram_vector_map: Dict[str, int]
) -> np.ndarray:
    """
    Given a list of ngrams of a word, returns the vector representing that word based on ngrams
    """
    vector_size = len(ngram_vector_map)
    # more python magic. itemgetter gets a collection of items from an iterable/collection all using iterables
    return np.sum(
        [_spawn_one_hot_encoded_vector(vector_size, ngram) for ngram in ngram_list],
        axis=0,
    ).reshape(1, -1)


def make_context_matrix(
    context_list: List[int], word_vector_map: Dict[str, int]
) -> np.ndarray:
    """
    Creates context matrix for given a list of the words context words
    """
    vector_size = len(word_vector_map)
    return np.vstack(
        [_spawn_one_hot_encoded_vector(vector_size, word) for word in context_list]
    )


def make_word_map(
    word_list: List[str],
    ngram_map: Dict[str, List[str]],
    context_map: Dict[str, List[str]],
    ngram_vectors: Dict[str, int],
    word_vector_map: Dict[str, int],
) -> Dict[str, Dict[str, List[int]]]:
    """
    Maps the input vector as well as the target matrix to their respective words

    Return dict in the shape of: {word: {input: vector, context: matrix}}
    """
    word_map = {}
    for word in np.unique(word_list):
        single_entry = {}
        ngrams = ngram_map[word]
        context = context_map[word]

        input_vector = (
            list(itemgetter(*ngrams)(ngram_vectors))
            if len(ngrams) > 1
            else [ngram_vectors[ngrams[0]]]
        )
        target_matrix = (
            list(itemgetter(*context)(word_vector_map))
            if len(context) > 1
            else [word_vector_map[context[0]]]
        )

        single_entry["input"] = input_vector
        single_entry["context"] = target_matrix

        word_map[word] = single_entry

    return word_map


def make_maps(
    word_list: List[str], model_config: ModelConfig
) -> Tuple[
    Dict[str, List[str]],
    Dict[str, List[str]],
    Dict[str, int],
    Dict[str, int],
    Dict[str, Dict[str, List[int]]],
]:
    """
    Makes all the needed maps for later use in the network.

    Returns ngram, context, ngram_vector, word_vector and word maps
    """
    ngram_map = make_ngram_map(word_list, model_config.ngram_size)
    context_map = make_context_map(
        word_list,
        left_context_window=model_config.context_window["left"],
        right_context_window=model_config.context_window["right"],
        self_context=model_config.self_context,
    )
    ngram_vectors = make_ngram_vector_map(ngram_map)
    word_vectors = make_word_vector_map(word_list)
    word_map = make_word_map(
        word_list, ngram_map, context_map, ngram_vectors, word_vectors
    )

    return ngram_map, context_map, ngram_vectors, word_vectors, word_map


def preprocess_corpus(
    language_config: LanguageConfig, model_config: ModelConfig
) -> Tuple[
    Dict[str, List[str]],
    Dict[str, List[str]],
    Dict[str, int],
    Dict[str, int],
    Dict[str, Dict[str, List[int]]],
]:
    """
    Given the path to the corpus, create dataset that will later be used in the NN
    """
    text = open_corpus(language_config.corpus_path)
    cleaned = clean_text(text)
    word_list = make_word_list(cleaned)
    word_list = remove_stopwords(word_list, language_config.stopwords_path)
    maps = make_maps(word_list, model_config)

    return maps
