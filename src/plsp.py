#!/usr/bin/env python3
import sys
import decimal
import os
import time
import re as regex
recurses = 0
imports = []
histfile = os.path.join(os.path.expanduser("~"), ".plisp-history")
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
    "SETPOP": 29,
    "ARGS": 30,
    "SYS": 31,
    "EXIT": 32,
    
    "NEWARRAY": 33,
    "APPEND": 34,
    "POP": 35,
    "INDEX": 36,
    "SETINDEX": 37,
    
    "ESTR": 38,
    "REPLACE": 39,
    "EXPR": 40,
    "STR": 41,
    
    "FOR": 42,
    
    "FLOAT": 43,
    "SPLIT": 44,
    "REGEX": 45,
    
    "TYPE": 46,
    "FREE": 47
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
            elif i == "args":
                toks.append(tokens["ARGS"])
            elif i == "sys":
                toks.append(tokens["SYS"])
            elif i == "exit":
                toks.append(tokens["EXIT"])
            elif i == "newarr":
                toks.append(tokens["NEWARRAY"])
            elif i == "append":
                toks.append(tokens["APPEND"])
            elif i == "pop":
                toks.append(tokens["POP"])
            elif i == "index":
                toks.append(tokens["INDEX"])
            elif i == "setindex":
                toks.append(tokens["SETINDEX"])
            elif i == "e":
                toks.append(tokens["ESTR"])
            elif i == "expr":
                toks.append(tokens["EXPR"])
            elif i == "replace":
                toks.append(tokens["REPLACE"])
            elif i == "str":
                toks.append(tokens["STR"])
            elif i == "for":
                toks.append(tokens["FOR"])
            elif i == "float":
                toks.append(tokens["FLOAT"])
            elif i == "split":
                toks.append(tokens["SPLIT"])
            elif i == "regex":
                toks.append(tokens["REGEX"])
            elif i == "type":
                toks.append(tokens["TYPE"])
            elif i == "free":
                toks.append(tokens["FREE"])
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
    try:
        i = eval(programtree)
    except:
        print("Unclosed/Unopened parenthesis")
        return None
    return i
previous_args = []
retval = 0
mfloat = False
def getret():
    global retval
    return retval
def setret(val):
    global retval
    retval=val
def recurse(tree, args=[]):
    global retval
    global mfloat
    global imports
    global previous_args
    global recurses
    recurses+=1
    global vars
    stack = []
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
                    t+=4
                    return recurse(tree[t])
                else:
                    t+=5
                    return recurse(tree[t])
            elif x == "<":
                if y < z:
                    t+=4
                    return recurse(tree[t])
                else:
                    t+=5
                    return recurse(tree[t])
            elif x == ">":
                if y > z:
                    t+=4
                    return recurse(tree[t])
                else:
                    t+=5
                    return recurse(tree[t])
            elif x == "<=":
                if y <= z:
                    t+=4
                    return recurse(tree[t])
                else:
                    t+=5
                    return recurse(tree[t])
            elif x == ">=":
                if y >= z:
                    t+=4
                    return recurse(tree[t])
                else:
                    t+=5
                    return recurse(tree[t])
            elif x == "!=":
                if y != z:
                    t+=4
                    return recurse(tree[t])
                else:
                    t+=5
                    return recurse(tree[t])
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
        elif i == tokens["ESTR"]:
            t+=1
            return str(tree[t])
        elif i == tokens["EXPR"]:
            t+=1
            i = recurse(tree[t])
            i = eval(i)
            return recurse(i)
        elif i == tokens["FOR"]:
            var = recurse(tree[t+1])
            outvar = recurse(tree[t+2])
            function = tree[t+3]
            for i in vars[var]:
                vars.update({outvar:i})
                recurse(function)
            return
        elif type(i) == list:
            y = recurse(i)
            if y != None:
                stack.append(y)
        else:
            for y in tokens: 
                if tokens[y] == i:op = y
            if op == "INT":
                if mfloat == False:
                    return decimal.Decimal(tree[t+1].replace("i",""))
                else:
                    return float(tree[t+1].replace("i",""))
            elif op == "VAR":
                if tree[t+1][1:] in funcs:
                    func = tree[t+1][1:]
                    argc = int(funcs[func]["args"])
                    args = []
                    t+=1
                    for i in range(argc):
                        args.append(recurse(tree[t+1]))
                        t+=1
                    previous_args = args
                    recurse(funcs[func]["func"])
                    return getret()
                else:
                    return tree[t+1][1:].replace("\s"," ").replace("\w","").replace("\_rb","(").replace("\_lb",")").replace(
                        "\_w","\w"
                    ).replace("\_s","\s")
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
    elif op == "DROP":
        stack.pop()
        return
    elif op == "EXEC":
        y = stack.pop()
        if y not in imports:
            x = load(y)
            i = progtree(x)
            recurse(i)
            imports.append(y)
        return
    elif op == "SWAP":
        print("SWAP has been deprecated")
        raise DeprecationWarning
    elif op == "INPUT":
        return input()
    elif op == "SET":
        x = stack.pop()
        y = stack.pop()
        vars.update({y:x})
        return
    elif op == "ARGS":
        x = stack.pop()
        args = previous_args
        return args[int(x)]
    elif op == "SYS":
        os.system(stack.pop())
        return
    elif op == "RETURN":
        setret(stack.pop())
        return getret()
    elif op == "EXIT":
        exit(stack.pop())
    elif op == "NEWARRAY":
        x = stack.pop()
        vars.update({x:[]})
        return
    elif op == "APPEND":
        x = stack.pop()
        y = stack.pop()
        vars[y].append(x)
        return
    elif op == "INDEX":
        x = stack.pop()
        y = stack.pop()
        return vars[y][int(x)]
    elif op == "SETINDEX":
        z = stack.pop()
        x = stack.pop()
        y = stack.pop()
        vars[y][int(x)] = z
        return
    elif op == "POP":
        x = stack.pop()
        return vars[x].pop()
    elif op == "REPLACE":
        x = stack.pop()
        z = stack.pop()
        y = stack.pop()
        return y.replace(x,z)
    elif op == "STR":
        x = stack.pop()
        return str(x)
    elif op == "FLOAT":
        mfloat = True
    elif op == "SPLIT":
        x = stack.pop()
        y = stack.pop()
        return y.split(x)
    elif op == "REGEX":
        x = stack.pop()
        y = stack.pop()
        return regex.findall(regex.compile(x),y)
    elif op == "TYPE":
        return str(type(stack.pop())).split(" ")[1].split("'")[1]
    elif op == "FREE":
        vars.pop(stack.pop())
def full():
    if len(sys.argv) < 2:
        import repltools as repltools
        repltools.repl()
    program = load(sys.argv[1])
    i = progtree(program)
    recurse(i)
if __name__ == "__main__":
    decimal.getcontext().prec = 100
    full()
    try:
        if sys.argv[2] == "--recurses":
            print("\nRecurses: "+ str(recurses))
    except:
        pass