import classla

classla.download('sr')
nlp = classla.Pipeline('sr', processors='tokenize,pos,lemma')

def get_lemmas(text: str):
    doc = nlp(text)
    dc = doc.to_dict()
    lemmas = []
    for da in dc:
        arr = da[0]
        print(arr)
        for token in arr:
            lemmas.append(token['lemma'])
    return lemmas

lemme = get_lemmas("Milica voli da ide u školu koja se nalazi u Novom Sadu. Nije ništa rekla. ")
print(lemme)
