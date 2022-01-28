import classla


class NER_classla():
    def __init__(self):
        classla.download('sr')
        self.nlp = classla.Pipeline('sr')

    def perform_NER(self, text):
        doc = self.nlp(text)
        result = []
        for ent in doc.to_dict()[0][0]:
            result.append({'text': ent["text"], "NER": ent["ner"], "dep_rel": ent["deprel"]})
        return result
