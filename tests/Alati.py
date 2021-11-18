import unittest
from srbai.Alati.Transliterator import transliterate_cir2lat,transliterate_lat2cir


class AlatiTestovi(unittest.TestCase):
    def test_transliterate_cir2lat(self):
        lat = transliterate_cir2lat("Он је ишао на преглед код доктора. Заљубио се у докторку. ")
        self.assertEqual(lat, "On je išao na pregled kod doktora. Zaljubio se u doktorku. ")  # add assertion here

    def test_transliterate_lat2cir(self):
        cir = transliterate_lat2cir("On je išao na pregled kod doktora. Zaljubio se u doktorku. ")
        self.assertEqual(cir,"Он је ишао на преглед код доктора. Заљубио се у докторку. ")


if __name__ == '__main__':
    unittest.main()
