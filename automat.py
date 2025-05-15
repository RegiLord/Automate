import sys

VERIFY = False

def ReadAutoamt(AutomatFile):
    f = open(AutomatFile, "r").readlines()

    Automat = dict()
    inBlock = False
    CurrentSection = ""
    line_number = 0

    for line in f:
        if inBlock == False: 
            line_number += 1
            if line[0] == '/':
                continue

            SectionName = line[:line.find(']') + 1]
            SectionName = SectionName[1:-1]
            CurrentSection = SectionName

            if SectionName in Automat.keys():
                print(f"ERROR: double declaration at line {line_number}")
                exit(1)
            # 0->undefined 1->set 2->single variabel 3-> function
            SectionType = 0

            start = line.find(']') + 1
            i = start 
            while i < len(line) - 1:
                if line[i] == " ":
                    i+= 1
                    continue
                start = i + 1
                SectionType = (line[i])
                break
                
            if SectionType == ':':
                SectionType = 1
            elif SectionType == '=':
                SectionType = 2
            elif SectionType == '{':
                SectionType = 3
                inBlock = True
            else: 
                SectionType = 0

            if SectionType == 0:
                print(f'ERROR: invalid section at line {line_number}')
                exit(1)
            
            if SectionType == 1:
                line = line[start:]
                Automat[SectionName] = line.split()
            elif SectionType == 2:
                line = line[start:].split()
                if len(line) > 1:
                    print(f"ERROR: invalid = definition, not a single variable at line {line_number}")
                    exit(1)
                Automat[SectionName] = line[0]
            elif SectionType == 3:
                Automat[SectionName] = dict()
                inBlock = True
            else: 
                pass
        else:
            if line.find('}') != -1:
                inBlock = False
                continue

            entry_function = line.split()
            if len(entry_function) == 0: 
                continue
            if  0 < len(entry_function) < 3 or len(entry_function) > 3:
                print(f'ERROR: invalid function definition at line {line_number}')
                exit(1)

            if (entry_function[0], entry_function[1]) in Automat[SectionName].keys():
                #e deja in dictionar
                Automat[SectionName][(entry_function[0], entry_function[1])].append(entry_function[2])
            else:
                #nu e
                Automat[SectionName][(entry_function[0], entry_function[1])] = []
                Automat[SectionName][(entry_function[0], entry_function[1])].append(entry_function[2])
    return Automat
                
def CheckString(Automat, string):
    global VERIFY
    VERIFY = False
    init_state = Automat["InitialState"]

    MemoryLog = dict()
    for state in Automat["States"]:
        MemoryLog[state] = []

    MemoryLog[Automat["InitialState"]].append(string)
    return RecursiveCheck(Automat, init_state, string, MemoryLog)
    
def RecursiveCheck(Automat, currentstate, string, MemoryLog):
    global VERIFY
    if len(string) == 0:
        return currentstate in Automat["FinalStates"]
    else:

        if (currentstate, 'eps') in Automat["Rules"] and len(Automat["Rules"][(currentstate, 'eps')]) != 0:
            for next_state in Automat["Rules"][(currentstate, 'eps')]:
                
                if string in MemoryLog[next_state]:
                    continue
                MemoryLog[next_state].append(string)
                VERIFY = VERIFY or RecursiveCheck(Automat, next_state, string, MemoryLog)

        if VERIFY == True: return VERIFY
        
        if (currentstate, string[0]) in Automat["Rules"] and len(Automat["Rules"][(currentstate, string[0])]) != 0:
            for next_state in Automat["Rules"][(currentstate, string[0])]:

                if string[1:] in MemoryLog[next_state]:
                    continue
                MemoryLog[next_state].append(string[1:])
                VERIFY = VERIFY or RecursiveCheck(Automat, next_state, string[1:], MemoryLog)

    return VERIFY

def CheckStringValidity(Automat, String):
    for c in String:
        if c not in Automat["Alphabet"]:
            print(f'ERROR: invalid string submitted, {c} is not in Alphabet')
            exit(1)
    return True

if len(sys.argv) > 1:

    AutomatFile = sys.argv[1] or "automayFinit.txt"
    String = sys.argv[2]
    Automat = ReadAutoamt(AutomatFile)

    print("Automat file: ", sys.argv[1])

    if String == "-inline":
        print("Make sure your Automat is deterministic")
        current_state = Automat["InitialState"]
        print(f'Current State: {current_state}')
        letter = input()
        
        while (letter != "exit"):
            if letter not in Automat["Alphabet"]:
                print("Invalid Entry: retry")
                letter = input()
                continue

            if (current_state, letter) in Automat["Rules"]:
                current_state = Automat["Rules"][(current_state, letter)][0]
            print(f'Current State: {current_state}')
            letter = input()

        if current_state in Automat["FinalStates"]:
            print(True)
        else:
            print(False)        
        
    else:
        print("string to check: ", sys.argv[2])
        CheckStringValidity(Automat, String)

        print(CheckString(Automat, String))
else:
    AutomatFile = "automatFinit.txt"
    Automat = ReadAutoamt(AutomatFile)
    
    print(Automat)
