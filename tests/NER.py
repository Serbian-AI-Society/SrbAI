import unittest
from src.srbai import NER_classla


class NER_Testovi(unittest.TestCase):
    def test_classla_NER(self):
        ner = NER_classla()
        res = ner.perform_NER("Nikola je bio u Parizu.")
        true_res = [{'text': 'Nikola', 'NER': 'B-PER', 'dep_rel': 'nsubj'}, {'text': 'je', 'NER': 'O', 'dep_rel': 'aux'}, {'text': 'bio', 'NER': 'O', 'dep_rel': 'root'}, {'text': 'u', 'NER': 'O', 'dep_rel': 'case'}, {'text': 'Parizu', 'NER': 'B-LOC', 'dep_rel': 'obl'}, {'text': '.', 'NER': 'O', 'dep_rel': 'punct'}]
        self.assertEqual(res,true_res)  # add assertion here


if __name__ == '__main__':
    unittest.main()
