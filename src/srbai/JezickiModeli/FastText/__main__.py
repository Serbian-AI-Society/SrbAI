from model import train
from text_preprocessing import preprocess_corpus
from globals import GlobalConfig
from io_utils import serialize_object, deserialize_object
from similarity import word_similarity
from embedding import embed_word, embed_word_map


def model_training():
    """
    Example function showing how to train the model for a given language
    """
    # Step 1. Load a configuration with which you would like to train the model
    # To load a config just type the folder name of the model and language
    cfg = GlobalConfig("5gram_5sctx_300vs", "serbian")

    # Step 2. Preprocess the corpus and prepare it for the NN
    _, _, ngram_vectors, word_vectors, word_map = preprocess_corpus(
        cfg.language_config, cfg.model_config
    )

    # Optional Step. Serialize the ngram_vectors and word_map so that they can be used later
    # Keep in mind that the save_dir from the config must exist, the serialization won't check for that itself
    serialize_object(ngram_vectors, cfg.language_config.get_ngram_vectors_file_path())
    serialize_object(word_map, cfg.language_config.get_word_map_file_path())

    # Step 3. Train the NN
    # The result of training will be the weights that lead to the embedding layer
    # If plot graph is true, it will plot the loss graph as well
    vector_space = train(word_map, ngram_vectors, word_vectors, cfg.model_config, plot_graph=False)

    # Optional Step. Save the weights that lead to the embedding layer
    serialize_object(vector_space, cfg.language_config.get_vector_space_file_path())


def similarity_for_word():
    """
    Example function that shows how finding most similar words for a word works
    """
    # Step 1. Load configs for both the model and language
    cfg = GlobalConfig("5gram_5sctx_300vs", "serbian")

    # Step 2. Load the ngram vectors, vector space and word map files
    ngram_vectors = deserialize_object(cfg.language_config.get_ngram_vectors_file_path())
    word_map = deserialize_object(cfg.language_config.get_word_map_file_path())
    vector_space = deserialize_object(cfg.language_config.get_vector_space_file_path())

    # Step 3. Run the word similarity function from the similarity module
    # It will return a tuple of the word itself and
    # a dictionary of words from the word map and their similarities w.r.t the passed word
    word, similarities = word_similarity("ekonom", word_map, ngram_vectors, vector_space, cfg.model_config.ngram_size)

    # Now you can do whatever you like with these similarities
    # Here are the top 5 similarities sorted in descending order
    print(sorted(similarities.items(), key=lambda item: item[1], reverse=True)[:5])


def embedding_things():
    """
    Example function of how to use the embedding module to embed a word or the whole current word map
    """
    # Step 1. Load the configurations for the model and language
    cfg = GlobalConfig("5gram_5sctx_300vs", "serbian")

    # Step 2. Load the ngram vectors, vector space and word map files
    ngram_vectors = deserialize_object(cfg.language_config.get_ngram_vectors_file_path())
    word_map = deserialize_object(cfg.language_config.get_word_map_file_path())
    vector_space = deserialize_object(cfg.language_config.get_vector_space_file_path())

    # Step 3.1 Use the embed word function to embed a single word into the vector space
    # This function will return only the vector
    vector = embed_word("ekonom", ngram_vectors, vector_space, cfg.model_config.ngram_size)
    print(vector)

    # Step 3.2 Use embed_word_map function to embed all the current words in the word map
    # This function will return a dictionary of all the words and their embedded vector representations
    embedded_word_map = embed_word_map(word_map, ngram_vectors, vector_space, cfg.model_config.ngram_size)
    # Print only 5 key-value pairs
    print(list(embedded_word_map.items())[:5])


if __name__ == "__main__":
    embedding_things()
