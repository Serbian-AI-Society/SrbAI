import classla

classla.download('sr')
nlp = classla.Pipeline('sr')
doc = nlp("France Prešeren je rođen v Vrbi.")
print(doc.to_conll())