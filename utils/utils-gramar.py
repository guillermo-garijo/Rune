terminals={'ᚠ','ᚡ','ᚴ','ᚵ','ᚶ','ᚢ','ᚤ','ᚥ','ᚨ','ᚩ','ᚪ','ᚫ','ᚾ',',ᛅ','ᚬ','ᚭ','ᚮ','ᚯ','ᚿ','ᛆ','ᚦ','ᚧ','ᚺ,','ᚻ','ᛉ','ᛣ','ᛩ','ᚹ','ᚱ','ᛃ','ᛖ','ᛝ','᛫','᛬','ᛰ','ᚁ','ᚂ','ᚃ','ᚄ','ᚅ','ᚆ','ᚇ','ᚈ','ᚉ','ᚊ','#'}

def has_left_recursion(grammar):
    for non_terminal, productions in grammar.items():
        for production in productions:
            first_symbol = production.split()[0]
            if first_symbol == non_terminal:
                print(first_symbol)
                return True
    return False

def has_indirect_left_recursion(grammar):
    non_terminals = list(grammar.keys())
    visited = set()

    def has_indirect_left_recursion_helper(non_terminal, ancestors):
        visited.add(non_terminal)
        for production in grammar[non_terminal]:
            symbols = production.split()
            first_symbol = symbols[0]
            if first_symbol in ancestors:
                print(first_symbol)
                return True
            elif first_symbol in non_terminals and first_symbol not in visited:
                if has_indirect_left_recursion_helper(first_symbol, ancestors + [non_terminal]):
                    print(first_symbol)
                    return True
        return False

    for non_terminal in non_terminals:
        visited.clear()
        print("checking " + non_terminal + "...")
        if has_indirect_left_recursion_helper(non_terminal, []):
            return True

    return False


def compute_first_sets(grammar):
    first_sets = {}
    for non_terminal in grammar:
        first_sets[non_terminal] = set()

    while True:
        updated = False
        for non_terminal, productions in grammar.items():
            print("procesando " + non_terminal)
            for production in productions:
                #print(production)
                tmp = production.split(' ')
                first_symbol=tmp[0]
                #print(first_symbol)
                if first_symbol in grammar:
                    prev_length = len(first_sets[non_terminal])
                    first_sets[non_terminal].update(compute_first_sets_helper(first_symbol, grammar, first_sets))
                    if len(first_sets[non_terminal]) > prev_length:
                        updated = True
                else:
                    if first_symbol != '#':
                        if first_symbol not in first_sets[non_terminal]:
                            first_sets[non_terminal].add(first_symbol)
                            updated = True

        if not updated:
            break

    # Add epsilon symbol to FIRST sets of non-terminals that derive epsilon
    for non_terminal, productions in grammar.items():
        
        for production in productions:
            if production == '#':
                first_sets[non_terminal].add('#')

    return first_sets

def compute_first_sets_helper(symbol, grammar, first_sets):
    first_symbols = set()
    print("procesando " + symbol)
    for production in grammar[symbol]:
        
        #print(production)
        tmp = production.split(' ')
        first_symbol=tmp[0]
        #print(first_symbol)
        if first_symbol in grammar:
            first_symbols.update(compute_first_sets_helper(first_symbol, grammar, first_sets))
        else:
            if first_symbol != '#':
                if first_symbol not in first_symbols:
                    first_symbols.add(first_symbol)

    return first_symbols
"""
def first(production, grammar):
    first_set = set()

    if production[0] in terminals:
        first_set.add(production[0])
    else:
        for rule in grammar:
            if rule[0] == production[0]:
                if production[0] != rule[1]:
                    first_set.update(first(rule[1:], grammar))

    if '#' in first_set and len(production) > 1:
        first_set.remove('#')
        first_set.update(first(production[1:], grammar))

    return first_set
"""
def compute_follows(grammar):
    follows={}
    first=compute_first_sets(grammar)
    for non_terminal in grammar:
        follows[non_terminal]=[]

    follows['E'].append('$')

    for non_terminal in grammar:
        compute_follow(non_terminal, grammar, first, follows[non_terminal])
    return follows
        
def compute_follow(symbol, grammar, first, follow):
    for non_terminal in grammar:
        for production in grammar[non_terminal]:
            tokens=production.split()
            for i in range(len(tokens)):
                if symbol==tokens[i] and i<len(tokens)-1:
                    




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

firsts=compute_first_sets(rules)


f=compute_follows(rules)
print(f)

#print(rules)
#follows=follow(rules)
#print(follows)
#print(has_left_recursion(rules))
#print(has_indirect_left_recursion(rules))
#firsts=compute_first_sets(rules)
#for key,value in firsts.items():
#    print(key, value)
