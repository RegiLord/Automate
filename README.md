# Automata

## DFA/NFA:
  I have implemented a DFA and NFA in python, that used a standardized automata file to define the machine and receives an input in command line as the string to check.

  The DFA code is pretty straightforward, it simply takes the current state and input and moves in the next state. However the NFA was more complicated because of it's nondeterministic nature. The code I wrote has worked for my tests, unfortunately I can't gurantee it's efficiency. It's based upon a memory block that remembers whenever you enter a state what string you've entered the state with.
  For example:
```
   MemoryLog = dict()
   MemoryLog[state] = ["aaa", "bbb", "bccc", "baaa"]
```
  This is done so you keep continuing with the input in a recursive method.

  PS: The DFA and NFA are implemented in the same python file, the file that differenciates is the automata file.

### Using the DFA/NFA
   
```bash
python3 <file.py> <automata_file_name> <string_to_check>
```
### Editing the automata file
  The file looks like the following example:
```
[States] : q1 q2 q3 q4
[Alphabet] : 0 1
[InitialState] = q1
[Rules] {
    q1 0 q1
    q1 1 q1
    q1 1 q2 
    q2 0 q3
    q2 1 q3
    q3 0 q4
    q3 1 q4 
}
[FinalStates] : q4
```

Pentru rulare PDA
```bash
python3 <fisier.py> <nume_fisier_automat> <string_to_check>
python3 <fisier.py> <nume_fisier_automat> --inline
```
Cu inline pentru scrie in real time
Pentru game.txt comenzile sunt (w - in sus, a - la stanga, s - in jos, d -> la dreapta si p -> pentru a lua cheia)
Iar scriere exit va iesi din program

Pentru rulare Turing
```bash 
python3 <fisier.py> <nume_fisier_automat>
```



2. PDA:
  PDA-ul e implementat pastrand un vector pentru stack, nu functioneaza nondeterministic din cauza ca ar trebui sa pastram o copie de stack
pentru fieacre ruta, daca am implementa ar trebui sa pastram o memorie ca la NFA, dar sa pastram si stack-ul nu doar input-ul

3. Masina Turing:
  Din cauza conceptului de spatii goale fisierul de configurare este un pic sensibil deoarece caracterul spatiu reprezinta un spatiu gol
