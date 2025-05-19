import sys

VERIFY = False

def Top(L):
    return L[len(L) - 1]

def ReadAutoamt(AutomatFile):
    f = open(AutomatFile, "r").readlines()

    Automat = dict()
    inBlock = False
    CurrentSection = ""
    line_number = 0

    Automat["Stiva"]= []

    for line in f:
        if inBlock == False: 
            line_number += 1
            if line[0] == '/' or len(line) == 0:
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

            e = line.split()
            if len(e) == 0:
                continue
                

            if len(e) != 5 and len(e) != 3:
                print(f'ERROR: invalid function definition at line {line_number}')
                exit(1)


            if (e[0], e[1]) in Automat[SectionName].keys():
                if len(e) == 5:
                    Automat[SectionName][(e[0], e[1])]["Pop"].append(e[2])
                    Automat[SectionName][(e[0], e[1])]["Push"].append(e[3])
                    Automat[SectionName][(e[0], e[1])]["Transition"].append(e[4])
                else:
                    Automat[SectionName][(e[0], e[1])]["Pop"].append('eps')
                    Automat[SectionName][(e[0], e[1])]["Push"].append('eps')
                    Automat[SectionName][(e[0], e[1])]["Transition"].append(e[2])
            else:
                Automat[SectionName][(e[0], e[1])] = dict()
                if len(e) == 5:
                    Automat[SectionName][(e[0], e[1])]["Pop"] = [e[2]]
                    Automat[SectionName][(e[0], e[1])]["Push"] = [e[3]]
                    Automat[SectionName][(e[0], e[1])]["Transition"] = [e[4]]
                else:
                    Automat[SectionName][(e[0], e[1])]["Pop"] = ['eps']
                    Automat[SectionName][(e[0], e[1])]["Push"] = ['eps']
                    Automat[SectionName][(e[0], e[1])]["Transition"] = [e[2]]
    return Automat

def GetNextState(Automat, current_state, letter):

    if (current_state, letter) not in Automat["Rules"].keys():
        return False
        
    for i in range(len(Automat['Rules'][(current_state, letter)]['Push'])):
        toPop = Automat["Rules"][(current_state, letter)]["Pop"][i]
        toPush = Automat["Rules"][(current_state, letter)]["Push"][i]
        toTransition = Automat["Rules"][(current_state, letter)]["Transition"][i]
            
        if toPop != 'eps' and (len(Automat['Stiva']) == 0 or Top(Automat['Stiva'])) != toPop:
            continue
            
        if toPop != 'eps':
            Automat['Stiva'].pop()
        if toPush != 'eps':
            Automat["Stiva"].append(toPush)
        return toTransition
    return False

def CheckString(Automat, string):
    global VERIFY
    VERIFY = False
    init_state = Automat["InitialState"]

    return RecursiveCheck(Automat, init_state, string)
    
def RecursiveCheck(Automat, current_state, string):

    if len(string) == 0:
        
        if current_state in Automat['FinalStates']:
            return True
        
        if (current_state, 'eps') in Automat["Rules"].keys():
            for i in range(len(Automat['Rules'][(current_state, 'eps')]['Push'])):
                toPop = Automat["Rules"][(current_state, 'eps')]["Pop"][i]
                toPush = Automat["Rules"][(current_state, 'eps')]["Push"][i]
                toTransition = Automat["Rules"][(current_state, 'eps')]["Transition"][i]

                if toPop != 'eps' and (len(Automat['Stiva']) == 0 or Top(Automat['Stiva']) != toPop):
                    continue

                if toPop != 'eps':
                    Automat['Stiva'].pop()
                if toPush != 'eps':
                    Automat['Stiva'].append(toPush)
                return RecursiveCheck(Automat, toTransition, string)
        return False
    else:
        if (current_state, 'eps') in Automat["Rules"].keys():
            for i in range(len(Automat['Rules'][(current_state, 'eps')]['Push'])):
                toPop = Automat["Rules"][(current_state, 'eps')]["Pop"][i]
                toPush = Automat["Rules"][(current_state, 'eps')]["Push"][i]
                toTransition = Automat["Rules"][(current_state, 'eps')]["Transition"][i]

                if toPop != 'eps' and (len(Automat['Stiva']) == 0 or Top(Automat['Stiva']) != toPop):
                    continue

                if toPop != 'eps':
                    Automat['Stiva'].pop()
                if toPush != 'eps':
                    Automat['Stiva'].append(toPush)
                return RecursiveCheck(Automat, toTransition, string)
        
        letter = string[0]
        if (current_state, letter) not in Automat["Rules"].keys():
            return False
        
        for i in range(len(Automat['Rules'][(current_state, letter)]['Push'])):
            toPop = Automat["Rules"][(current_state, letter)]["Pop"][i]
            toPush = Automat["Rules"][(current_state, letter)]["Push"][i]
            toTransition = Automat["Rules"][(current_state, letter)]["Transition"][i]
            
            if toPop != 'eps' and (len(Automat['Stiva']) == 0 or Top(Automat['Stiva'])) != toPop:
                continue
            
            if toPop != 'eps':
                Automat['Stiva'].pop()
            if toPush != 'eps':
                Automat["Stiva"].append(toPush)
            return RecursiveCheck(Automat, toTransition, string[1:])
        return False

def CheckStringValidity(Automat, String):
    for c in String:
        if c not in Automat["Alphabet"]:
            print(f'ERROR: invalid string submitted, {c} is not in Alphabet')
            exit(1)
    return True


if len(sys.argv) > 1:
    AutomatFile = sys.argv[1]
    Automat = ReadAutoamt(AutomatFile)
        
    if len(sys.argv) == 3:
        String = ''
        if len(sys.argv) > 2:
            String = sys.argv[2]

        print("Automat file: ", sys.argv[1])

        print("string to check: ", String)
        CheckStringValidity(Automat, String)

        print(CheckString(Automat, String))
    else:
        if sys.argv[3] != '--inline':
            print(f'Unknown flag {sys.argv[4]}')
            exit(1)
        
        current_state = Automat['InitialState']
        print("Enter exit to finish string")
        
        
        while True:
            print(f'{current_state}  {Automat["Stiva"]}')
            symbol = input("Input: ")   
            if symbol not in Automat["Alphabet"] and symbol != "exit":
                print(f'Invalid, {symbol} not in alphabet. Try Again!')
                continue
            if symbol == "exit":
                break

            current_state = GetNextState(Automat, current_state, symbol)
            if current_state == False:
                print(f'False no rule for case')
                exit(1)
                        
        if current_state in Automat["FinalStates"]:
            print(True)
        else:
            print(f'False not in final states')
else:
    AutomatFile = "testpda.txt"
    Automat = ReadAutoamt(AutomatFile)
    
    print(Automat)
