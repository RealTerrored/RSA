import argparse
import os
import time
import math
import threading
from multiprocessing import Process, Pipe, Queue
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
start = time.perf_counter()
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
def test():
    time.sleep(1)
def Job(low, high, format, conn, process_num, total_processes):
    time.sleep(process_num)
    num_range = high - low
    sets = set()
    i = 3
    low1 = low + math.ceil((num_range/total_processes)*process_num)
    high1 = high - math.floor((num_range/total_processes)*(total_processes-(process_num+1)))
    globals()["progress" + str(process_num)] = tqdm(total=math.ceil(high1-low1), desc="Finding values in process " + str(process_num), unit="nums", leave= False)
    if (low1 % 2 == 0):
        low1 = low1 + 1
    if (high1 % 2 == 0):
        high1 = high1 + 1
    while(low1 <= high1):
        if (low1 % i != 0):
            i = i + 2
            if (i >= low1):
                if (format == 1):
                    sets.add(hex(low1))
                    globals()["progress" + str(process_num)]:tqdm.update(1)
                else:
                    sets.add(low1)
                    #finding1.update(1)
                i = 3
                low1 = low1 + 2
        else:
            #finding1.update(1)
            low1 = low1 + 2
            i = 3
    conn.send(sets)
if __name__ == '__main__':
    os.system("cls")
    parser = argparse.ArgumentParser(description='Primal number locator')
    parser.add_argument("--mode", default=2, type=int,choices=[1, 2], help="Mode of operation: 1=Primal detector, 2=Primal Generator")
    parser.add_argument("--number", type=int, help="Number to check, required with mode 1")
    parser.add_argument("--low", type=int, default= 0, help="Starting point for calculations, required with mode 2")
    parser.add_argument("--high", type=int, default= 100, help="Ending point for calculations, required with mode 2")
    parser.add_argument("--name", type=str, default="test", help="Name for the output file, required with mode 2")
    parser.add_argument("--hex", type=int, choices=[1, 2], default=2, help="Defines the format of output, 1=Hexadecimal, 2= Decadecimal, required with mode 2")
    parser.add_argument("--process", type=int,default=1, help="Defines the format of output, 1=Hexadecimal, 2= Decadecimal, required with mode 2")
    args = parser.parse_args()

    mode = args.mode
    num = args.number
    low = args.low
    high = args.high
    file = args.name
    format = args.hex
    process_num = args.process
    prime_set = set()
    conn1, conn2 = Pipe()
    temp = 0

    debug = False

    if(mode == 2):
        if (file == None):
            print(bcolors.FAIL + "ERROR: --file value is needed" + bcolors.ENDC)
            exit()
        path = os.path.dirname(os.path.realpath(__file__))
        path = path + "\output\\" + file + ".txt"

        while(True):
            if (os.path.isfile(path)):
                print(bcolors.WARNING + "Destination file exists, do you want to overwrite it? Choosing no will add new numbers to the end of the file" + bcolors.ENDC)
                print(bcolors.WARNING + "y = yes" + bcolors.ENDC)
                print(bcolors.WARNING + "n = no" + bcolors.ENDC)
                choice = input()
                if (choice == "y"):
                    choice = "w"
                    break
                elif (choice == "n"):
                    choice = "a"
                    break
                else:
                    print(bcolors.FAIL + "ERROR: Please choose either y or n" + bcolors.ENDC)
            else:
                choice = "w"
                break
    os.system("cls")
    i = 3
    if (mode == 1):
        if (num == None):
            print(bcolors.FAIL + "ERROR: --number value is needed" + bcolors.ENDC)
            exit()
        while (True):
            if ((num % i) != 0):
                i = i + 2
                if (i >= num):
                    print(bcolors.OKGREEN + "The number is primal" + bcolors.ENDC)
                    break
            else:
                print(bcolors.OKCYAN + "The number is NOT primal" + bcolors.ENDC)
                break
    elif (mode == 2):
        output = open(path, choice)
        
        #total = tqdm(total=math.floor((high-low)*1.33), desc="Main progress", unit="nums", leave= False, disable=debug)
        total = process_map()
        writing = tqdm(desc="Writing values", unit="nums", leave= False, disable=debug)

        for x in range(process_num):
            globals() ["process" + str(x)] = Process(target=Job, args=(low, high, format, conn2, x, process_num))
            globals() ["process" + str(x)].start()

        

        for x in range(process_num):
            prime_set = prime_set.union(conn1.recv())
        prime_set = sorted(prime_set)
    
    writing.total = (len(prime_set))
    total.total = ((high-low)+len(prime_set))
    for val in prime_set:
        output.write(str(val) + ";")
        writing.update(1)
        total.update(1)
    writing.close()
    total.close()
    end = time.perf_counter()
    print(bcolors.OKBLUE + " Successfuly finished in " + str(math.floor((end-start)*100)/100) + " seconds!" + bcolors.ENDC)