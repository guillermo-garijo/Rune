


#terminals={'ᚠ','ᚡ','ᚴ','ᚵ','ᚶ','ᚢ','ᚤ','ᚥ','ᚨ','ᚩ','ᚪ','ᚫ','ᚾ',',ᛅ','ᚬ','ᚭ','ᚮ','ᚯ','ᚿ','ᛆ','ᚦ','ᚧ','ᚺ,','ᚻ','ᛉ','ᛣ','ᛩ','ᚹ','ᚱ','ᛃ','ᛖ','ᛝ','᛫','᛬','ᛰ','ᚁ','ᚂ','ᚃ','ᚄ','ᚅ','ᚆ','ᚇ','ᚈ','ᚉ','ᚊ','#'}
terminals={'+','*','#','(',')','id'}

def compute_first(grammar):
    firsts_set = {}
    for rule in grammar:
        firsts_set[rule]=[]
    for rule in grammar:
        #print('making: ' + rule)
        first_helper(grammar, firsts_set, rule, rule)

    return firsts_set


def first_helper(grammar, firsts_set, production, origin):
    for p in grammar[production]:
        symbols=p.split(' ')
        #print(symbols[0])
        if symbols[0] in terminals:
            firsts_set[origin].append(symbols[0])
            #print(firsts_set)
        elif symbols[0] in firsts_set:
            if '#' in symbols:
                firsts_set[origin].append(firsts_set[symbols[0]])
                #print(firsts_set)
                if len(symbols)>1:
                    first_helper(grammar, firsts_set, symbols[1], origin)
            else:
                first_helper(grammar, firsts_set, symbols[0], origin)


def compute_follow(grammar, firsts_set):
    follows_set = {}
    for rule in grammar:
        follows_set[rule]=[]

    for rule in grammar:
        print('making: ' + rule)
        follow_helper(grammar, follows_set, rule, firsts_set)
    return follows_set

def follow_helper(grammar, follows_set, current, firsts_set):
    for production in grammar:
        for derivation in production:
            tokens=derivation.split(' ')
            for i in range(len(tokens)):
                if tokens[i]==current:
                    if i==len(tokens)-1:
                        follows_set[current].extend(follows_set[production])
                        break
                    else:
                        if tokens[i+1] in terminals:
                            follows_set[current].append(tokens[i+1])
                            break
                        else:
                            if '#' not in firsts_set[tokens[i+1]]:
                                follows_set[current].extend(firsts_set[tokens[i+1]])
                                break
                            else:
                                follows_set[current].extend(firsts_set[tokens[i+1]])
                                for j in range(i+1,len(tokens)):
                                    if '#' in firsts_set[tokens[j]]:
                                        follows_set[current].extend(firsts_set[tokens[j]])
                                    else:
                                        follows_set[current].extend(firsts_set[tokens[j]])
                                        break
                                    follows_set[current].extend(follows_set[production])
                                break
                                




    pass


rules={}
file = open("tests.txt")
for line in file.readlines():
    if(line[0]!='-'):
        split1=line.strip().split(':')
        tmp=split1[1].replace('[','')
        productions=tmp.replace(']','')
        split2=productions.split(',')
        rules[split1[0]]=split2
file.close()

firsts=compute_first(rules)
#print(firsts)

follows=compute_follow(rules, firsts)
print(follows)