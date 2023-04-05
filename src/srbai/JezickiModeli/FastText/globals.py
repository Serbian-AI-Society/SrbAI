import os
from typing import Dict, Any

import yaml


class Config:
    def __init__(self) -> None:
        self.config_dir: str = os.path.join(".", "configs")

    def load_yaml(self, yaml_path: str) -> Dict[str, Any]:
        with open(yaml_path, "rb") as f:
            yaml_data = yaml.safe_load(f)

        return yaml_data


class ModelConfig(Config):
    def __init__(self, model_name: str) -> None:
        super().__init__()

        _yaml_data = self.load_yaml(
            os.path.join(self.config_dir, "models", model_name, "config.yaml")
        )

        _text_preproc = _yaml_data["text_preprocessing"]
        self.ngram_size: int = _text_preproc["ngram_size"]
        self.context_window: Dict[str, int] = _text_preproc["context_window"]
        self.self_context: bool = _text_preproc["self_context"]

        _neural_network = _yaml_data["neural_network"]
        self.vector_space_size: int = _neural_network["vector_space_size"]
        self.optimizer: Dict[str, float] = _neural_network["optimizer"]
        self.learn_rate: float = _neural_network["learn_rate"]
        self.epochs: int = _neural_network["epochs"]


class LanguageConfig(Config):
    def __init__(self, language: str) -> None:
        super().__init__()

        _yaml_data = self.load_yaml(
            os.path.join(self.config_dir, "languages", language, "config.yaml")
        )

        self.corpus_path: str = _yaml_data["corpus_path"]
        self.stopwords_path: str = _yaml_data["stopwords_path"]

        _io = _yaml_data["io"]
        self.root = _io["root"]
        self.save_dir = _io["save_dir"]
        self.vector_space_file = _io["vector_space_file"]
        self.ngram_vectors_file = _io["ngram_vectors_file"]
        self.word_map_file = _io["word_map_file"]

    def _get_save_dir_path(self) -> str:
        return os.path.join(self.root, self.save_dir)

    def get_vector_space_file_path(self) -> str:
        return os.path.join(self._get_save_dir_path(), self.vector_space_file)

    def get_ngram_vectors_file_path(self) -> str:
        return os.path.join(self._get_save_dir_path(), self.ngram_vectors_file)

    def get_word_map_file_path(self) -> str:
        return os.path.join(self._get_save_dir_path(), self.word_map_file)


class ClusteringConfig(Config):
    def __init__(self, clustering_model_name: str):
        super.__init__()
        self.data = self.load_yaml(
            os.path.join(self.config_dir, "clustering", clustering_model_name, "config.yaml")
        )


class GlobalConfig:
    def __init__(self, model_name: str, language: str) -> None:
        self.model_config: ModelConfig = ModelConfig(model_name)
        self.language_config: LanguageConfig = LanguageConfig(language)
