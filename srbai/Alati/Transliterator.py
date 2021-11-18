def transliterate_cir2lat(text: str) -> str:
    """
    Pretvara tekst napisan ćirilicom u latinicu
    :param text: Tekst na ćirilici
    :return: Tekst na latinici
    """
    mappings = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ђ": "đ", "е": "e", "ж": "ž", "з": "z", "и": "i",
                "ј": "j", "к": "k", "л": "l", "љ": "lj", "м": "m", "н": "n", "њ": "nj", "о": "o", "п": "p", "р": "r",
                "с": "s", "т": "t", "ћ": "ć", "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "č", "џ": "dž", "ш": "š",
                "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Ђ": "Đ", "Е": "E", "Ж": "Ž", "З": "Z", "И": "I",
                "Ј": "J", "К": "K", "Л": "L", "Љ": "Lj", "М": "M", "Н": "N", "Њ": "Nj", "О": "O", "П": "P", "Р": "R",
                "С": "S", "Т": "T", "Ћ": "Ć", "У": "U", "Ф": "F", "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š"}
    translit = ""
    for char in text:
        if char in mappings.keys():
            translit = translit + mappings[char]
        else:
            translit = translit + char
    return translit


def transliterate_lat2cir(text: str) -> str:
    """
    Pretvara tekst napisan na laticini u ćirilicu
    :param text: Tekst na latinici
    :return: Tekst na ćirilici
    """
    mappings = {"a": "а", "b": "б", "v": "в", "g": "г", "d": "д", "đ": "ђ", "e": "е", "ž": "ж", "z": "з", "i": "и",
                "j": "ј", "k": "к", "l": "л", "lj": "љ", "m": "м", "n": "н", "nj": "њ", "o": "о", "p": "п", "r": "р",
                "s": "с", "t": "т", "ć": "ћ", "u": "у", "f": "ф", "h": "х", "c": "ц", "č": "ч", "dž": "џ", "š": "ш",
                "A": "А", "B": "Б", "V": "В", "G": "Г", "D": "Д", "Đ": "Ђ", "E": "Е", "Ž": "Ж", "Z": "З", "I": "И",
                "J": "Ј", "K": "К", "L": "Л", "Lj": "Љ", "LJ": "Љ", "M": "М", "N": "Н", "Nj": "Њ", "NJ": "Њ", "O": "О",
                "P": "П", "R": "Р",
                "S": "С", "T": "Т", "Ć": "Ћ", "U": "У", "F": "Ф", "H": "Х", "C": "Ц", "Č": "Ч", "Dž": "Џ", "DŽ": "Џ",
                "Š": "Ш"}
    translit = ""
    i = 0
    while i < len(text):
        if text[i] in mappings.keys():
            if text[i] in ["l", "n", "L", "N"] and i + 1 < len(text) and (text[i + 1] == "j" or text[i + 1] == "J"):
                translit = translit + mappings[text[i] + text[i + 1]]
                i = i + 1
            elif text[i] in ["d", "D"] and i + 1 < len(text) and (text[i + 1] == "ž" or text[i + 1] == "Ž"):
                translit = translit + mappings[text[i] + text[i + 1]]
                i = i + 1
            else:
                translit = translit + mappings[text[i]]
        else:
            translit = translit + text[i]
        i = i + 1
    return translit
