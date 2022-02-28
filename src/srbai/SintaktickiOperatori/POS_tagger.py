import os

from nltk import word_tokenize
from nltk.tag.hunpos import HunposTagger

from src import srbai


class POS_Tagger():
    def __init__(self):
        path = os.path.abspath(srbai.__file__).replace(os.path.sep + "__init__.py", "")
        os.environ["HUNPOS_TAGGER"] = os.environ["HUNPOS"] = path + os.path.sep+"Resursi"+os.path.sep+"PomocneDatoteke"+os.path.sep+"hunpos-tag.exe"
        print(os.environ["HUNPOS_TAGGER"])
        self.ht = HunposTagger(path + os.path.sep+'Resursi'+os.path.sep+'Modeli'+os.path.sep+'model.hunpos.mte5.defnpout',encoding='UTF-8')


    def tag(self, text):
        """
        Oznacava vrste reci u tekstu. Prvo slovo oznacava generalno vrstu reci:
        http://nlp.ffzg.hr/data/tagging/msd-hr.html
        - N - Imenica
        - V - Glagol
        - A - Pridev
        - P - Zamenice
        - S - Predlozi
        - Z - Znak interpunkcije
        - C - Veznik
        - M - Broj
        - R - Prilozi,
        - I - Uzvici
        - Q - Rečice
        - Y - Skraćenice
        - X - Ostalo
        :param text:
        :return:
        """
        tagged = self.ht.tag(word_tokenize(text))
        return tagged
