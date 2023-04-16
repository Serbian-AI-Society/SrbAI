SrbAI - Python biblioteka za procesiranje srpskog jezika
========================================================

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

import srbai
```

### Transliteracija

Za transliteraciju postoje 2 metode, jedna za transliteraciju sa ćirilice na latinicu, dok druga za transliteraciju sa latinice na ćirilicu

```python
from srbai.Alati.Transliterator import transliterate_cir2lat, transliterate_lat2cir

lat = transliterate_cir2lat("Текст на ћирилици. ")
cir = transliterate_lat2cir("Tekst na latinici. ")
```

### Stemmer

Stemer se može koristiti uz pomoć sledeće dve funkcije:

* stem_str - pretvara ulazni tekst u stemmovani izlazni string
* stem_arr - pretvata ulazni tekst u niz string-ova koji su stemmovani

Primer:

```python
from srbai.SintaktickiOperatori.stemmer_nm import stem_str, stem_arr

sent = stem_str("Jovica je išao u školu. Marija je dobra devojka.")
```

```python
from srbai.SintaktickiOperatori.stemmer_nm import stem_str, stem_arr

sent_arr = stem_arr("Jovica je išao u školu. Marija je dobra devojka.")
```

### Spell checker za srpski jezik

U okviru SrbAI projekta je implementiran i spell checker zasnovan na rečnicima poteklim iz OpenOffice projekta. 
Implementacija je zasnovana na Trie strukturi podataka i Levensteinovoj distanci. Ovaj rečnik se može koristiti na sledeći način:
```python
from srbai.SintaktickiOperatori.spellcheck import SpellCheck
sc = SpellCheck('sr-latin') #postoji opcija i #sr-cyrilic za ćirilicu
word = "predetori"
correction = sc.spellcheck(word)
if correction:
    print(f"Did you mean '{correction}'?")
else:
    print("No close match found.")
```

Izlaz treba da izgleda na sledeci nacin:
```commandline
Did you mean 'predatori'?
```


### Pronalaženje vrsta reči (Part-of-speech tagging)

Za pronalaženje vrsta reči u rečenici i morfološku analizu koristimo HunPos model koji je treniran za srpski i hrvatski jezik.

O karakteristikama modela, oznakama vrsta reči možete više pročitati na http://nlp.ffzg.hr/data/tagging/msd-hr.html

Da bi se model instancirao u memoriju, koristi se klasa, radi brže kasnije obrade i optimizacije resursa.

Primeri korišćenja:

```python
from srbai.SintaktickiOperatori.POS_tagger import POS_Tagger

pt = POS_Tagger()
tags = pt.tag('Jovica je išao u školu. Marija je dobra devojka.')
# [('Jovica', b'N-msn'), ('je', b'Vcr3s'), ('išao', b'Vmp-sm'), ('u', b'Sa'), ('školu', b'N-fsa'), ('.', b'Z'), ('Marija', b'N-fsn'), ('je', b'Vcr3s'), ('dobra', b'Agpfsn'), ('devojka', b'N-fsn'), ('.', b'Z')]
```

### FastText

FastText je model mašinskog učenja koji enkodira vektorski prostor na osnovu ulaznog korpusa. Vektorski prostor se sastoji iz vektora reči srpskog jezika koje se nalaze unutar ulaznog korpusa. Osnovna ideja jeste da ovaj model ponudi način da se reči srpskog jezika mapiraju na vektorski prostor kako bi se dalje mogle koristiti kao ulazni vektori za neke druge modele. Sam vektorski prostor očuvava semantičku i strukturalnu sličnost reči.

Kako bi se model koristio potrebno je namestiti konfiguraciju za jezik i za model. Konfiguracije se mogu pronaći unutar *configs* direktorijuma *FastText* modula, koji se i sam nalazi unutar direktorijuma *JezickiModeli*. Preporučeno je da se iskoristi već postojeća konfiguracija za model jer se ona pokazala kao najbolja u većini situacija, dok za jezičku konfiguraciju samo treba postaviti putanje ka korpusu na kojem će se model trenirati, putanju do stowords fajla, koji je već prisutan za srpski jezik, kao i putanje željene lokacije čuvanja modela. Samo je važno da se na kraju konfiguracije sačuvaju unutar svojih direktorijuma pod *config.yaml* kako bi modul mogao da ih pronađe na osnovu imena, tako, na primer, ako napravite novu jezičku konfiguraciju za engleski jezik, sačuvali biste je unutar *configs/languages/english* gde bi naziv konfiguracije onda bio *config.yaml*. Isto važi i za konfiguracije modela.

Modul se može koristiti kako bi se natrenirala skroz nova mreža, odnosno embedovao skroz novi vektorski prostor. Takođe ako već postoji natrenirani model onda ga je moguće koristiti kako bi se dobila vektorska reprezentacija neke prosleđene reči, kao i pronalaženje najsličnijih reči nekoj prosleđenoj reči.

Primeri kako se ovo može postići i kako se model koristi nakon postavljanja konfiguracija se nalazi u `__main__.py` fajlu unutar modula. Takođe unutar modula se nalaze primer konfiguracije za srpski jezik, kojem je potrebno promeniti samo `corpus_path` ukoliko želite odmah da ga koristite. Kao i primer jednog kratkog korpusa na srpskom.

## Autori i kontributori
- Nikola Milosevuc ([@nikolamilosevic86](https://github.com/nikolamilosevic86))
- Vladimir Lunic ([@Vlodson](https://github.com/Vlodson))
