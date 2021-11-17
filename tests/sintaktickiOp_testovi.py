import unittest
from src.SintaktickiOperatori.stemmer_nm import stem_str, stem_arr


class SintaktickiOperatoriTestovi(unittest.TestCase):
    def test_stemmer_nm(self):
        sent = stem_str("Jovica je išao u školu. Marija je dobra devojka.")
        self.assertEqual(sent, " jovi jesam isx u sxkol . marij jesam dobr devoj .")  # add assertion here
        sent2 = stem_arr("Jovica je išao u školu. Marija je dobra devojka.")
        expect = ['jovi', 'jesam', 'isx', 'u', 'sxkol', '.', 'marij', 'jesam', 'dobr', 'devoj', '.']
        self.assertEqual(sent2, expect)


if __name__ == '__main__':
    unittest.main()
