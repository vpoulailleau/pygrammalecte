# pygrammalecte

(english version at the bottom of this document)

Grammalecte, le correcteur grammatical en Python.

Pour être précis, ce projet n’est pas Grammalecte, mais un « wrapper » permettant de l’utiliser facilement en Python.

## Installation

```sh
python -m pip install pygrammalecte
```

## Utilisation

### Vérification d’une chaîne de caractères

```python
from pygrammalecte import grammalecte_text

texte_bidon = """\
Coucou, je veut du fromage.
Je sais coder en VHDL.
Le VHDL est est compliquer.
"""

for message in grammalecte_text(texte_bidon):
    print(message)
```

### Vérification d’un fichier

Vous devez fournir le chemin du fichier en `str` ou en `pathlib.Path`.

```python
from pathlib import Path

from pygrammalecte import grammalecte_file

filepath = Path("toto.txt")

for message in grammalecte_file(filepath):
    print(message)
```

### Messages générés

Les fonctions `grammalecte_file` et `grammalecte_text` sont des générateurs, vous pouvez donc les utiliser dans une boucle `for`.

Deux types de messages existent :

- `GrammalecteSpellingMessage` qui a comme attributs :
  - `line` : numéro de la ligne dans le texte vérifié
  - `start` : numéro du caractère de début de l’erreur dans la ligne
  - `end` : numéro du caractère de fin de l’erreur dans la ligne
  - `word` : le mot non reconnu par `Grammalecte`

- `GrammalecteGrammarMessage` qui a comme attributs :
  - `line` : numéro de la ligne dans le texte vérifié
  - `start` : numéro du caractère de début de l’erreur dans la ligne
  - `end` : numéro du caractère de fin de l’erreur dans la ligne
  - `url` : l’URL fournie par `Grammalecte`
  - `color` : une couleur fournie par `Grammalecte`, c’est une liste de 3 entiers entre 0 et 255.
  - `suggestions` : propositions de correction
  - `message` : message d’erreur
  - `rule` : identifiant de la règle violée
  - `type` : type de la règle (`"conj"`…)

## English version

This is a wrapper for the french grammatical checker called Grammalecte.