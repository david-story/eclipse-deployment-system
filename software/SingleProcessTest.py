import time
import os
import math

def f(x):
    if x > 0:
        value = 0
        for i in range(x):
            value = value + math.cos(math.sqrt(x))
        return value
    return

if __name__ == '__main__':

    start = time.time()
    value = []
    for i in range(25000):
        thing = f(i)
        value.append(thing)

    end = time.time()
    total = end-start

    file = open("new_output.txt", 'w')
    for thing in value:
        file.write(str(thing) + "\n")

    file.write("Total processing time:" +str(total)+"\nEnd of test")
    print(total)