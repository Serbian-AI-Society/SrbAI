import os
import unittest
from srbai.SintaktickiOperatori.stemmer_nm import stem_str, stem_arr
from srbai.SintaktickiOperatori.POS_tagger import POS_Tagger


class SintaktickiOperatoriTestovi(unittest.TestCase):
    def test_stemmer_nm(self):
        sent = stem_str("Jovica je išao u školu. Marija je dobra devojka.")
        self.assertEqual(sent, " jovi jesam isx u sxkol . marij jesam dobr devoj .")  # add assertion here
        sent2 = stem_arr("Jovica je išao u školu. Marija je dobra devojka.")
        expect = ['jovi', 'jesam', 'isx', 'u', 'sxkol', '.', 'marij', 'jesam', 'dobr', 'devoj', '.']
        self.assertEqual(sent2, expect)

    def test_tagger(self):
        pt = POS_Tagger()
        tags = pt.tag('Jovica je išao u školu. Marija je dobra devojka.')
        self.assertEqual(tags,[('Jovica', b'N-msn'), ('je', b'Vcr3s'), ('išao', b'Vmp-sm'), ('u', b'Sa'), ('školu', b'N-fsa'), ('.', b'Z'), ('Marija', b'N-fsn'), ('je', b'Vcr3s'), ('dobra', b'Agpfsn'), ('devojka', b'N-fsn'), ('.', b'Z')])
        tags = pt.tag('Predlozi su nepromenljive vrste reči koje izražavaju odnos između bića, stvari i pojava i utiču na padež reči uz koju stoje.  Stoje uz imenice i zamenice.')
        print(tags)
        tags = pt.tag(
            'Radn površina')
        print(tags)
if __name__ == '__main__':
    unittest.main()
