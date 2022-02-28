SrbAI - Python biblioteka za procesiranje srpskog jezika
===========================
SrbAI je projekat prikupljanja algoritama i modela za procesiranje srpskog jezika u jedinstvenu Python biblioteku. Biblioteka treba da sadrži kako osnovne metode za procesiranje srpskog, poput stemmera, prepoznavanje vrsta reči (part-of-speech tagging), negacija, do naprednijih funkcionalnosti, poput prepoznavanje imenovanih entiteta (named entity tagging), klasifikacije, itd. Biblioteka jednostavno može da se proširi novim metodima, tako da je ideja da se veći broj studenata, doktoranada i drugih ljudi koji rade i su zainteresovani za razvoj srpskog procesiranja jezika uključe u razvoj projekta. 

Vizija projekta je da postane **jedinstven i sveobuhvatan resurs za obradu srpskog jezika** koji bi se koristio bilo u akademske, bilo u komercijalne svrhe.  

## Instalacija

Kada klonirate paket, možete ga instalirati uz pomoć: 
```bash
python -m pip install --upgrade build .
```
Paket se može kreirati uz pomoć komande: 
```bash
python -m build
```
Nakon čega se može instalirati uz pomoć python pip komande

## Upotreba

Nakon instalacije, paket se može importovati kao

```python

from src import srbai
```

### Transliteracija

Za transliteraciju postoje 2 metode, jedna za transliteraciju sa ćirilice na latinicu, dok druga za transliteraciju sa latinice na ćirilicu

```python
from src.srbai.Alati.Transliterator import transliterate_cir2lat, transliterate_lat2cir

lat = transliterate_cir2lat("Текст на ћирилици. ")
cir = transliterate_lat2cir("Tekst na latinici. ")
```

### Stemmer

Stemer se može koristiti uz pomoć sledeće dve funkcije:

* stem_str - pretvara ulazni tekst u stemmovani izlazni string
* stem_arr - pretvata ulazni tekst u niz string-ova koji su stemmovani

Primer:

```python
from src.srbai.SintaktickiOperatori.stemmer_nm import stem_str, stem_arr

sent = stem_str("Jovica je išao u školu. Marija je dobra devojka.")
```

```python
from src.srbai.SintaktickiOperatori.stemmer_nm import stem_str, stem_arr

sent_arr = stem_arr("Jovica je išao u školu. Marija je dobra devojka.")
```

### Pronalaženje vrsta reči (Part-of-speech tagging)

Za pronalaženje vrsta reči u rečenici i morfološku analizu koristimo HunPos model koji je treniran za srpski i hrvatski jezik.

O karakteristikama modela, oznakama vrsta reči možete više pročitati na http://nlp.ffzg.hr/data/tagging/msd-hr.html

Da bi se model instancirao u memoriju, koristi se klasa, radi brže kasnije obrade i optimizacije resursa.

Primeri korišćenja:

```python
from src.srbai.SintaktickiOperatori.POS_tagger import POS_Tagger

pt = POS_Tagger()
tags = pt.tag('Jovica je išao u školu. Marija je dobra devojka.')
# [('Jovica', b'N-msn'), ('je', b'Vcr3s'), ('išao', b'Vmp-sm'), ('u', b'Sa'), ('školu', b'N-fsa'), ('.', b'Z'), ('Marija', b'N-fsn'), ('je', b'Vcr3s'), ('dobra', b'Agpfsn'), ('devojka', b'N-fsn'), ('.', b'Z')]
```


## Autori i kontributori
