from multiprocessing.sharedctypes import Value
import os


completer = [
    "()",
    "print",
    "set",
    "get",
    "if",
    "def",
    "loop",
    "drop",
    "exec",
    "==",
    "!=",
    ">=",
    "<=",
    "sys",
    "return",
    "args",
    "in",
    "newarr",
    "str",
    "pop",
    "index",
    "setindex",
    "append"
]
def repl():
    from plsp import progtree,recurse,load,funcs
    import sys
    from os.path import expanduser
    if len(sys.argv) <= 1:
        from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory       
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.styles.pygments import style_from_pygments_cls
    from pygments.styles import get_style_by_name    
    from prompt_toolkit.shortcuts import ProgressBar
    from prompt_toolkit.shortcuts import clear
    from prompt_toolkit.output.color_depth import ColorDepth

    libs = ["std.plsp","repl.plsp","types.plsp","math/proof.plsp"]
    clear()
    print("Loading librarys")
    with ProgressBar() as pb:
        for i in pb(libs):
            with open("repl.tmp","w") as t:
                t.write(f"(exec({i}))")
            prg = load("repl.tmp")
            os.remove("repl.tmp")
            i = progtree(prg)
            recurse(i)
    for i in funcs:
        if i not in completer:
            completer.append(i)
    style = style_from_pygments_cls(get_style_by_name('monokai'))
    
    def bottom_toolbar():
        return
    session = PromptSession(history = FileHistory(expanduser('~/.plisphistory')),)
    print("""
 _ __ | (_)___ _ __  
| '_ \| | / __| '_ \ 
| |_) | | \__ \ |_) |
| .__/|_|_|___/ .__/ 
|_|           |_|
Commit: 54""")
    while True:
        try:
            x = session.prompt('plisp → ',completer=WordCompleter(completer,ignore_case=True),
                            complete_while_typing=True, style=style, auto_suggest=AutoSuggestFromHistory(), color_depth=ColorDepth.TRUE_COLOR)
        except ValueError:
            exit(1)
        if x == "exit":
            exit(0)
        with open("repl.tmp","w") as t:
            t.write("("+x+")")
        prg = load("repl.tmp")
        os.remove("repl.tmp")
        i = progtree(prg)
        try:
            print("\n"+str(recurse(i)))
        except Exception as _:
            print("error.")
        for i in funcs:
            if i not in completer:
                completer.append(i)
