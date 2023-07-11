import os.path
import argparse
import random
import math
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
os.system("cls")
start = time.perf_counter()
"""
def Euclidean(x, y):
    x_set = set()
    x_devisor = 1
    y_set = set()
    y_devisor = 1
    xy_devisor = None
    while (x >= x_devisor):
        if(x % x_devisor == 0):
            x_set.add(x_devisor)
        x_devisor = x_devisor + 1
    while (y >= y_devisor):
        if(y % y_devisor == 0):
            y_set.add(y_devisor)
        y_devisor = y_devisor + 1
    x_set = sorted(x_set, reverse=True)
    y_set = sorted(y_set, reverse=True)
    for a in x_set:
        if (a in y_set):
            xy_devisor = a
            break
    return xy_devisor
def phi(n:int)->int:
    y = 0
    for k in range(1, n + 1):
        if Euclidean(n, k) == 1:
            y += 1
    return y
def carmichael(x:int, y:int)->int:
    if (x == y):
        return phi(x*y)
    else:
        return int((abs((phi(x))*(phi(y)))/Euclidean((phi(x)), (phi(y)))))"""
def Totient(x:int,y:int)->int:
    return((x-1)*(y-1))
def eFunc(tot:int)->int:
    e = random.randint(10,tot)
    i=3
    while(True):
        prime = False
        if(e % 2 != 0):
            while (True):
                if ((e % i) != 0 or i >= e):
                    if (i >= e):
                        i = 3
                        prime = True
                        break
                else:
                    i = 3
                    break
                i = i + 2
        if(prime == True and tot%e != 0):
            return e
        else:
            e = e - 1
def dFunc(e, tot):
    d = random.randint(e,tot)
    while(True):
        if((d*e)%tot == 1):
            return d
        else:
            d = d + 1
            

def encrypt(text:str):
    return bytearray(text.encode("utf-8"))







parser = argparse.ArgumentParser(description='RSA cypher')
parser.add_argument("--path", type=str, help="Path to file with primal numbers, if not specified, program will open a GUI interface to pick")
args = parser.parse_args()

path = args.path

if (path == None):
    Tk().withdraw()
    path = askopenfilename()
    start = time.perf_counter()
try:
    file = open(path, "r")
except:
    print(bcolors.FAIL + "ERROR: File or path does not exist, please specify a valid path" + bcolors.ENDC)
    exit()
primals_list = file.read().split(';')
p = int(primals_list[random.randint(0, len(primals_list))])
q = int(primals_list[random.randint(0, len(primals_list))])
text = "Hello"
n = p*q
Tot = Totient(p,q)
e = eFunc(Tot)
d = dFunc(e, Tot)
e = hex(e)
d = hex(d)
encrypted = encrypt(text)

print(Tot)
print(e)
print(d)
end = time.perf_counter()
print("Finished in " + str(math.floor((end-start)*100)/100) + " seconds")
#for i in encrypted:
#    print(i)