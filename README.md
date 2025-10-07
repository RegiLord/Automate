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
  In the States segment you list out the state names with a space between them, same for the Alphabet (the letters of course) and Final States.\
  Initial State is only one so just a single state name.\
  In the Rules category the format is: **[state I'm in] [input i need] [state I want to go]**\
  For the epsilon variable write *eps*

## PDA

  The PDA is implemented using a vector as the memory stack, unfortunately it doesn't work nondeterministically as we would need to keep a copy of the stack for each different possibility and that might lead to too much memory usage.\
  The format is similar to the DFA/NFA with additional information to the automata file.
  
### Using the PDA
  These are the options to run the file in  command line, the *--inline* option was added as a way to visualize the changes. This was because the first PDA I built and the one on which I tested the python file is a minigame in which you can move up down left and right and need to go to the kitchen get the key and unlock the exit.
  However I don't advise using the *--inline* option except in specific cases.
  
```bash
python3 <fisier.py> <nume_fisier_automat> <string_to_check>
python3 <fisier.py> <nume_fisier_automat> --inline
```
For game.txt the commands are:
  - w upwards
  - a left
  - d right
  - s down
  - p get key
For the *--inline* option writing exit will finish the sequence

### Editing the automata file
```
[States] : q0 q1 q2 q3
[Alphabet] : 0 1 eps
[InitialState] = q0 
[FinalStates] : q3
[Rules] {
    q0 eps eps $ q1
    q1 0 eps 0 q1
    q1 1 0 eps q2 
    q2 1 0 eps q2
    q2 eps $ eps q3
}
```
  It is similar to the DFA/NFA automata however the Rules section has changed.\
  The Rules Format is now: **[state we're in][input to check][stack to pop][stack to push][state to go]**

Pentru rulare Turing
```bash 
python3 <fisier.py> <nume_fisier_automat>
```


3. Masina Turing:
  Din cauza conceptului de spatii goale fisierul de configurare este un pic sensibil deoarece caracterul spatiu reprezinta un spatiu gol
