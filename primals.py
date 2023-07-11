import argparse
import os
import time
import math
from tqdm import tqdm
from multiprocessing import Process, Pipe, Queue
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
def progress(low, high, que:Queue, que2:Queue, debug):
    progressing = tqdm(total=high-low, disable=debug, smoothing=0.5, leave=True, unit="Nums", desc="Generating primes", unit_scale=True)
    value = 0
    while(True):
        progressing.n = 2*value + que.qsize()
        progressing.update()
        if (not que2.empty()):
            progressing.total = que2.get()
            break
def Job(low, high, format, conn, process_num, total_processes, que:Queue, que3:Queue):
    time.sleep(process_num)
    num_range = high - low
    sets = set()
    i = 3
    low1 = low + math.ceil((num_range/total_processes)*process_num)
    high1 = high - math.floor((num_range/total_processes)*(total_processes-(process_num+1)))
    if (low1 % 2 == 0):
        low1 = low1 + 1
    if (high1 % 2 == 0):
        high1 = high1 + 1
    while(low1 <= high1):
        if(len(sets) >= 500):
            conn.send(sets)
            sets = set()
        if (low1 % i != 0):
            i = i + 2
            if (i >= low1):
                if (format == 1):
                    sets.add(hex(low1))
                    que.put(True, block=False)
                else:
                    sets.add(low1)
                    que.put(True, block=False)
                i = 3
                low1 = low1 + 2
        else:
            low1 = low1 + 2
            i = 3
            que.put(True, block=False)
    conn.send(sets)
    que3.put(1)
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
    que = Queue()
    que2 = Queue()
    que3 = Queue()

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
        progress_update = Process(target=progress, args=(low, high, que, que2, debug))
        progress_update.start()

        for x in range(process_num):
            globals() ["process" + str(x)] = Process(target=Job, args=(low, high, format, conn2, x, process_num, que, que3))
            globals() ["process" + str(x)].start()

        
        while (que3.qsize() != process_num):
            for x in range(process_num):
                prime_set = prime_set.union(conn1.recv())
                tqdm.write(str(que3.qsize()))
        for x in range(process_num):
            globals() ["process" + str(x)].terminate()

        
        prime_set = sorted(prime_set)
        que2.put(len(prime_set))
        progress_update.join()
    
    for val in prime_set:
        output.write(str(val) + ";")
    end = time.perf_counter()
    print(bcolors.OKBLUE + " Successfuly finished in " + str(math.floor((end-start)*100)/100) + " seconds!" + bcolors.ENDC)