#!/usr/bin/env python3
import sys
import decimal
recurses = 0
tokens = {
    "RBRACKET": 0,
    "LBRACKET": 1,
    "PLUS": 2,
    "MINUS": 3,
    "TIMES": 4,
    "DIVIDE": 5,
    "INT": 6,
    "PRINT": 7,
    "SET": 8,
    "VAR": 9,
    "GET": 10,
    "IF": 11,
    "EQUAL": 12,
    "LESS": 13,
    "MORE": 14,
    "LESSEQUAL": 15,
    "MOREEQUAL": 16,
    "DEF": 17,
    "CALL": 18,
    "LOOP": 19,
    "DROP": 20,
    "EXEC": 21,
    "SWAP": 22,
    "NOTEQUAL": 23, 
    "MOD": 24,
    "POW": 25,
    "INPUT": 26,
    "STRONGSET": 27,
    "RETURN": 28,
    "SETPOP": 29
}
vars = {}
funcs = {}
macros = {}
def load(program):
    global tokens
    try:
        with open(program, "r") as p:
            x = p.read()
    except:
        with open("/usr/share/plisp/"+program, "r") as p:
            x = p.read()
    x = x.replace("\n", " ")
    x = x.replace(" ", "")
    toks = []
    for y in x.split("(")[1:]:
        toks.append(tokens["RBRACKET"])
        z = y.split(")")
        for x in range(z.count("")):
            z.pop()
        for i in z:
            if i == "+":
                toks.append(tokens["PLUS"])
            elif i == "-":
                toks.append(tokens["MINUS"])
            elif i == "*":
                toks.append(tokens["TIMES"])
            elif i == "/":
                toks.append(tokens["DIVIDE"])
            elif i == "print":
                toks.append(tokens["PRINT"])
            elif i == "set":
                toks.append(tokens["SET"])
            elif i == "get":
                toks.append(tokens["GET"])
            elif i == "==":
                toks.append(tokens["EQUAL"])
            elif i == "<":
                toks.append(tokens["LESS"])
            elif i == ">":
                toks.append(tokens["MORE"])
            elif i == "<=":
                toks.append(tokens["LESSEQUAL"])
            elif i == ">=":
                toks.append(tokens["MOREEQUAL"])
            elif i == "!=":
                toks.append(tokens["NOTEQUAL"])
            elif i == "if":
                toks.append(tokens["IF"])
            elif i == "def":
                toks.append(tokens["DEF"])
            elif i == "call":
                toks.append(tokens["CALL"])
            elif i == "loop":
                toks.append(tokens["LOOP"])
            elif i == "drop":
                toks.append(tokens["DROP"])
            elif i == "exec":
                toks.append(tokens["EXEC"])
            elif i == "swap":
                toks.append(tokens["SWAP"])
            elif i == "%":
                toks.append(tokens["MOD"])
            elif i == "^":
                toks.append(tokens["POW"])
            elif i == "in":
                toks.append(tokens["INPUT"])
            elif i == "set!":
                toks.append(tokens["STRONGSET"])
            elif i == "return":
                toks.append(tokens["RETURN"])
            elif i == "setpop":
                toks.append(tokens["SETPOP"])
            else:
                
                try:
                    decimal.Decimal(i)
                    toks.append(tokens["INT"])
                    toks.append("\"i"+i+"\"")
                except:
                    toks.append(tokens["VAR"])
                    toks.append("\"v"+i+"\"")
        for x in range(y.count(")")):
            toks.append(tokens["LBRACKET"])
    return toks
def progtree(program):
    programtree = ""
    for i in program:
        if i == tokens["RBRACKET"]:
            programtree+="["
        elif i == tokens["LBRACKET"]:
            programtree+="],"
        else: programtree += str(i)+","
    programtree = programtree.replace("[,","[")
    programtree = programtree.replace(",]","]")
    programtree = programtree[0:-1]
    i = eval(programtree)
    return i
def recurse(tree, stack=[]):
    global recurses
    global vars
    op = ""
    t = 0
    while t < len(tree):
        i = tree[t]
        if i == tokens["IF"]:
            x = recurse(tree[t+1])
            y = recurse(tree[t+2])
            z = recurse(tree[t+3])
            if x == "==":
                if y == z:
                    recurse(tree[t+4])
                else:
                    recurse(tree[t+5])
            elif x == "<":
                if y < z:
                    recurse(tree[t+4])
                else:
                    recurse(tree[t+5])
            elif x == ">":
                if y > z:
                    recurse(tree[t+4])
                else:
                    recurse(tree[t+5])
            elif x == "<=":
                if y <= z:
                    recurse(tree[t+4])
                else:
                    recurse(tree[t+5])
            elif x == ">=":
                if y >= z:
                    recurse(tree[t+4])
                else:
                    recurse(tree[t+5])
            elif x == "!=":
                if y != z:
                    recurse(tree[t+4])
                else:
                    recurse(tree[t+5])
            t+=5
        elif i == tokens["DEF"]:
            name = recurse(tree[t+1])
            args = recurse(tree[t+2])
            func = tree[t+3]
            funcs.update({name:{
                "args": args,
                "func": func
            }})
            t+=3
        elif i == tokens["LOOP"]:
             count = recurse(tree[t+1])
             for i in range(int(count)):
                 recurse(tree[t+2])
             t+=2
        elif i == tokens["STRONGSET"]:
             name = recurse(tree[t+1])
             macro = tree[t+2]
             macros.update({name:macro})
             t+=2
        elif type(i) == list:
            y = recurse(i)
            if y != None:
                stack.append(y)
        else:
            for y in tokens: 
                if tokens[y] == i:op = y
            if op == "INT":
                return decimal.Decimal(tree[t+1].replace("i",""))
            elif op == "VAR":
                if tree[t+1][1:] in macros:
                    return recurse(macros[tree[t+1][1:]])
                return tree[t+1][1:]
        t+=1 
    if op == "PLUS":
        return (stack.pop()+stack.pop())
    elif op == "MINUS":
        return (stack.pop()-stack.pop())
    elif op == "DIVIDE":
        return (stack.pop()/stack.pop())
    elif op == "TIMES":
        return (stack.pop()*stack.pop())
    elif op == "MOD":
        return (stack.pop()%stack.pop())
    elif op == "POW":
        return (stack.pop()**stack.pop())
    elif op == "PRINT":
        x = stack.pop()
        if type(x) == str:
            x = x.replace("\s"," ").replace("\w","")
        print(x,end="")
        return x
    elif op == "GET":
        return vars[stack.pop()]
    elif op == "EQUAL":
        return "=="
    elif op == "LESS":
        return "<"
    elif op == "MORE":
        return ">"
    elif op == "LESSEQUAL":
        return "<="
    elif op == "MOREEQUAL":
        return ">="
    elif op == "NOTEQUAL":
        return "!="
    elif op == "CALL":
        func = stack.pop()
        if len(stack) < funcs[func]["args"]:
            print("Not enough items on the stack to call: " + func)
            exit()
        return recurse(funcs[func]["func"],stack)
    elif op == "DROP":
        stack.pop()
    elif op == "EXEC":
        x = load(stack.pop())
        i = progtree(x)
        recurse(i)
    elif op == "SWAP":
        x = stack.pop()
        y = stack.pop()
        stack.append(x)
        return y
    elif op == "INPUT":
        return decimal.Decimal(input())
    elif op == "RETURN":
        return stack.pop()
    elif op == "SET":
        x = stack.pop()
        y = stack.pop()
        vars.update({y:x})
    recurses += 1
def full():
    if len(sys.argv) <= 1:
        print("Too few arguments.")
        print("Usage: plisp <file>")
        return
    program = load(sys.argv[1])
    i = progtree(program)
    recurse(i)
full()
try:
    if sys.argv[2] == "--recurses":
        print("\nRecurses: "+ str(recurses))
except:
    pass