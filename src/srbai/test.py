import classla
classla.download('sr')
nlp =classla.Pipeline('sr')
doc = nlp("Milica voli da ide u školu koja se nalazi u Novom Sadu.")
print(doc.to_dict()[0][0])

