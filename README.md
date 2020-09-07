# pygrammalecte

[![PyPI](https://img.shields.io/pypi/v/pygrammalecte.svg)](https://pypi.python.org/pypi/pygrammalecte)
[![PyPI](https://img.shields.io/pypi/l/pygrammalecte.svg)](https://github.com/vpoulailleau/pygrammalecte/blob/master/LICENSE)
[![Travis](https://api.travis-ci.com/vpoulailleau/pygrammalecte.svg?branch=master)](https://travis-ci.com/vpoulailleau/pygrammalecte)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Downloads](https://pepy.tech/badge/pygrammalecte)](https://pepy.tech/project/pygrammalecte)
[![Test Coverage](https://api.codeclimate.com/v1/badges/44347ade656fa1e652ae/test_coverage)](https://codeclimate.com/github/vpoulailleau/pygrammalecte/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/44347ade656fa1e652ae/maintainability)](https://codeclimate.com/github/vpoulailleau/pygrammalecte/maintainability)

(english version at the bottom of this document)

Grammalecte, le correcteur grammatical en Python.

Pour être précis, ce projet n’est pas Grammalecte, mais un « wrapper » permettant de l’utiliser facilement en Python.

## Installation

Vous devez utiliser un Python en version supérieure ou égale à 3.7.

L’utilisation d’un environnement virtuel est fortement recommandé.

```sh
python3 -m pip install pygrammalecte
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

Vous devez fournir le chemin du fichier en `str` ou en `pathlib.Path`. Le fichier doit être un fichier texte brut (pas un fichier Word ou OpenDocument par exemple).

```python
from pathlib import Path

from pygrammalecte import grammalecte_file

filepath = Path("toto.txt")

for message in grammalecte_file(filepath):
    print(message)
```

### Messages générés

Les fonctions `grammalecte_file` et `grammalecte_text` sont des générateurs, vous pouvez donc les utiliser dans une boucle `for`. Elles génèrent des `GrammalecteMessage`.

Deux types de `GrammalecteMessage` existent :

- `GrammalecteSpellingMessage` qui a comme attributs :

  - `line` : numéro de la ligne dans le texte vérifié
  - `start` : numéro du caractère de début de l’erreur dans la ligne
  - `end` : numéro du caractère de fin de l’erreur dans la ligne
  - `word` : le mot non reconnu par `Grammalecte`
  - `message` : message d’erreur

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

## Changelog

### Version v1.1.0

- Ajout de l'attribut `message` pour `GrammalecteSpellingMessage`

### Version v1.0.0

- Refactoring
- Ajout de l'intégration continue

### Version v0.1.0

- Première version !
- Utilisation de Grammalecte v1.11.0

## English version

This is a wrapper for the french grammatical checker called Grammalecte.
