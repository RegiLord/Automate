Automate:

1. Def/Nfa:
   Fisierul python poate rula si NFA-uri si DFA-uri in functie de daca este introdus simbolul epsilon in reguli sau daca sunt omise niste
reguli.
  NFA-ul pentru a evita ciclarea pastreaza o memorie atunci cand intra intr-o stare cu un input anumit si daca ajunge din nou in aceea
stare cu acelasi input atunci nu mai continue.

2. PDA:
  PDA-ul e implementat pastrand un vector pentru stack, nu functioneaza nondeterministic din cauza ca ar trebui sa pastram o copie de stack
pentru fieacre ruta, daca am implementa ar trebui sa pastram o memorie ca la NFA, dar sa pastram si stack-ul nu doar input-ul

3. Masina Turing:
  Din cauza conceptului de spatii goale fisierul de configurare este un pic sensibil deoarece caracterul spatiu reprezinta un spatiu gol
