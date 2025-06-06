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

    Automat["CurrentPosition"] = 0

    for line in f:
        if inBlock == False: 
            line_number += 1
            if line[0] == '/' or len(line) <= 1:
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
                line = line[start:].strip()

                if line[0] == '(' and line[-1] == ')':
                    Automat[SectionName] = line[1:-1]
                    continue
                
                line = line.split()
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
            if(len(line.split()) == 0):
                continue
            if line.find('}') != -1 and line.find('{') == -1:
                inBlock = False
                continue

            e = line[line.find('{'):]
            e = e[1:-2]
            e = e.split(',')
            if len(e) == 0:
                continue
                

            if len(e) != 5 and len(e) != 3:
                print(f'ERROR: invalid function definition at line {line_number}')
                exit(1)

            if len(e) == 3:
                if (e[0], 'eps') in Automat[SectionName].keys():
                    Automat[SectionName][(e[0], e[1])]["Replace"].append('eps')
                    if e[2] == "R":
                        Automat[SectionName][(e[0], e[1])]["Move"].append(1)
                    else:
                        Automat[SectionName][(e[0], e[1])]["Move"].append(-1)
                    Automat[SectionName][(e[0], e[1])]["Transition"].append(e[1])
                else:
                    Automat[SectionName][(e[0], e[1])] = dict()

                    Automat[SectionName][(e[0], e[1])]["Replace"] = ['eps']
                    if e[2] == "R":
                        Automat[SectionName][(e[0], e[1])]["Move"] = [1]
                    else:
                        Automat[SectionName][(e[0], e[1])]["Move"] = [-1]
                    Automat[SectionName][(e[0], e[1])]["Transition"] = [e[1]]

            if (e[0], e[1]) in Automat[SectionName].keys():
                Automat[SectionName][(e[0], e[1])]["Replace"].append(e[3])
                if e[4] == "R":
                    Automat[SectionName][(e[0], e[1])]["Move"].append(1)
                else:
                    Automat[SectionName][(e[0], e[1])]["Move"].append(-1)
                Automat[SectionName][(e[0], e[1])]["Transition"].append(e[2])
            else:
                Automat[SectionName][(e[0], e[1])] = dict()
               
                Automat[SectionName][(e[0], e[1])]["Replace"] = [e[3]]
                if e[4] == "R":
                    Automat[SectionName][(e[0], e[1])]["Move"] = [1]
                else:
                    Automat[SectionName][(e[0], e[1])]["Move"] = [-1]
                Automat[SectionName][(e[0], e[1])]["Transition"] = [e[2]]
    return Automat

def GetNextState(Automat, current_state):
    i = Automat["CurrentPosition"]
    KeyPair = (current_state, Automat["Memory"][i])
    
    if KeyPair in Automat["Rules"].keys():
        Automat["Memory"] = Automat["Memory"][:i] + Automat["Rules"][KeyPair]["Replace"][0] + Automat["Memory"][i+1:]
        i = i + Automat["Rules"][KeyPair]["Move"][0]
        if i < 0: return False
        if i >= len(Automat["Memory"]): return False
        Automat["CurrentPosition"] = i
        return Automat["Rules"][KeyPair]["Transition"][0]
    
    KeyPair = (current_state, 'eps')
    if KeyPair in Automat["Rules"].keys():
        Automat["Memory"] = Automat["Memory"][:i] + Automat["Rules"][KeyPair]["Replace"][0] + Automat["Memory"][i+1:]
        i = i + Automat["Rules"][KeyPair]["Move"][0]
        if i < 0: return False
        if i >= len(Automat["Memory"]): return False
        Automat["CurrentPosition"] = i
        return Automat["Rules"][KeyPair]["Transition"][0]
    
    return False

def CheckAutomat(Automat):
    init_state = Automat["InitialState"]

    return RecursiveCheck(Automat, init_state)
    
def RecursiveCheck(Automat, current_state):
    next_state = GetNextState(Automat, current_state)
    if next_state == False:
        if current_state in Automat["FinalStates"]:
            return True
        else:
            return False
    return RecursiveCheck(Automat, next_state)

def CheckStringValidity(Automat, String):
    for c in String:
        if c not in Automat["Alphabet"]:
            print(f'ERROR: invalid string submitted, {c} is not in Alphabet')
            exit(1)
    return True


if len(sys.argv) > 1:
    AutomatFile = sys.argv[1]
    Automat = ReadAutoamt(AutomatFile)

    print("Automat file: ", sys.argv[1])
    print(f'Checking memory ({Automat["Memory"]})')
    print(CheckAutomat(Automat))
    print(f'After processing ({Automat["Memory"]})')


else:
    AutomatFile = "testturing.txt"
    Automat = ReadAutoamt(AutomatFile)
    
    print(Automat)  
    print(f'Checking memory ({Automat["Memory"]})')
    print(CheckAutomat(Automat))
    print(f'After processing ({Automat["Memory"]})')
    
