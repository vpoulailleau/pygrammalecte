from pygrammalecte import grammalecte_text

texte_bidon = """\
Coucou, je veut du fromage.
Je sais coder en VHDL.
Le VHDL est est compliquer.
"""

for message in grammalecte_text(texte_bidon):
    print(message)
