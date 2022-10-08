
import sys,os, subprocess


if os.getuid() != 0:
    print("You must be root.")
    exit(1)
try:
    os.mkdir("/usr/share/plisp")
except FileExistsError:
    pass
print("INFO: Created library dir")
std = ["std/std.plsp","std/test.plsp","std/repl.plsp","std/types","std/types.plsp","std/math"]
t = list(filter(lambda s: s.find('packages') > -1, sys.path))[0]
os.system(f"cp ./src/repltools.py {t}")
print(f"INFO: ./src/repltools.py -> {t}/repltools.py")
os.system(f"cp ./src/plsp.py {t}")
print(f"INFO: ./src/plsp.py -> {t}/plsp.py ")
for x in std:
    os.system(f"cp -r ./src/{x} /usr/share/plisp")
    print(f"INFO: ./src/{x} -> /usr/share/plisp/{x}")
os.system("cp -r ./src/plsp.py /usr/bin/plisp")
os.system("chmod +xrw /usr/bin/plisp")
try:
    x = subprocess.check_output(["plisp","test/testlang.plsp"])
    print("INFO: Running tests")
    if x.decode("utf8").split("\n")[-2].split(":")[1][1:] != "0":
        print("ERR: Tests failed")
        for i in x.decode("utf8").split("\n"):
            if i.count("failed") != 0:
                print("INFO: "+i)
    else:
        print("INFO: All tests passed!")
except:
    print("ERR: Testing program failed.")