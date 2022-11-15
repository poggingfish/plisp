import time,os
launcher = "python3 ../src/plsp.py"
print("Benchmarking ")
x = time.time()
os.system(f"{launcher} bench1.plsp")
print("Include all in: " + str(time.time()-x) + " seconds.")

x = time.time()
os.system(f"{launcher} bench2.plsp")
print("For loop finished in: " + str(time.time()-x) + " seconds.")

x = time.time()
os.system(f"{launcher} bench3.plsp")
print("Dictionary finished in: " + str(time.time()-x) + " seconds.")

x = time.time()
os.system(f"{launcher} bench4.plsp")
print("50000 loop b=b+1;a=a*b finished in: " + str(time.time()-x) + " seconds.")
x = time.time()
os.system(f"{launcher} ../projecteuler/pe1.plsp")
print("Project Euler 1 finished in: " + str(time.time()-x) + " seconds.")
x = time.time()
os.system(f"{launcher} ../projecteuler/pe2.plsp")
print("Project Euler 2 finished in: " + str(time.time()-x) + " seconds.")