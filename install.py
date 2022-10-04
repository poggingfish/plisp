
import sys,os, subprocess


if os.getuid() != 0:
    print("You must be root.")
    exit(1)
try:
    os.mkdir("/usr/share/plisp")
except FileExistsError:
    pass
print("INFO: Created library dir")
std = ["std/std.plsp","std/test.plsp"]
for x in std:
    os.system(f"cp ./{x} /usr/share/plisp")
    print(f"INFO: ./{x} -> /usr/share/plisp/{x}")
os.system("cp ./plsp.py /usr/bin/plisp")
os.system("chmod +xrw /usr/bin/plisp")
x = subprocess.check_output(["plisp","testlang.plsp"])
print("INFO: Running tests")
if x.decode("utf8").split("\n")[-2].split(":")[1][1:] != "0":
    print("INFO: Tests failed")
    for i in x.decode("utf8").split("\n"):
        if i.count("failed") != 0:
            print("INFO: "+i)
else:
    print("INFO: All tests passed!")