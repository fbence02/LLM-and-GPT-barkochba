#  Szemantikus Barkochba

A projekt célja egy olyan innovatív barkochba játék kifejlesztése volt, amely a hagyományos, betűalapú egyezések helyett a szavak **valódi, kontextusbeli jelentését** veszi alapul a tippek kiértékelésénél.

---

##  Hogyan működik?

A játék motorját a modern természetes nyelvfeldolgozás (NLP) és a mesterséges intelligencia alapelvei hajtják, az alábbi folyamat szerint:

### 1. Szóbeágyazás (Word Embedding)
A rendszer a szavakat nem egyszerű szövegként kezeli, hanem **többdimenziós matematikai vektorokká** (hosszú számsorozatokká) alakítja. A szótár összes szava egy közös geometriai vektortérben helyezkedik el, ahol az irányok és a távolságok szigorú logikai és jelentésbeli összefüggéseket tükröznek.

### 2. Koszinusz-hasonlóság (Cosine Similarity)
Amikor a játékos beküldi a tippjét, a backend lekéri a célszó és a tippelt szó vektorát, majd kiszámítja a kettő közötti koszinusz-hasonlóságot (a vektorok által bezárt szöget):
**Nagy érték (közel 1.0-hez):** A vektorok iránya hasonló, vagyis a szavak jelentése nagyon közel áll egymáshoz (pl. *kutya* és *farkas*).
**Kis érték (közel 0.0-hoz):** A vektorok távoliak, a szavak jelentése között nincs érdemi összefüggés (pl. *kutya* és *csavarhúzó*).

### 3. AI Asszisztens (Okos Segítség)
Ha a játékos elakadna, segítséget kérhet a beépített **mesterséges intelligenciától**. Az AI asszisztens olyan kontextuális utalásokat és nyomokat generál, amelyek komoly lökést adhatnak a megoldás felé, de nem teszik túl egyszerűvé a játékot, így megmarad a felfedezés öröme és a kihívás.