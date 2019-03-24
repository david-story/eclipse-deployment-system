from multiprocessing import Pool
import time
import math
import os

def f(x):
    if x > 0:
        value = 0
        for i in range(x):
            value = value + math.cos(math.sqrt(x))
        return value
    return

if __name__ == '__main__':
	
	go = False
	try:
		cpu = os.cpu_count()
		go = True
	except:
		pass
		
	try:
		if go == False:
			cpu = multiprocessing.cpu_count()
			go = True
	except:
		cpu = 1
		pass
	start = time.time()
	p = Pool(os.cpu_count())
	value = p.map(f, range(25000))
	end = time.time()
	total = end - start
	file = open("output.txt", "w")
	file.write("\n-------- Start of Test --------")
	iterator = 0
	writestart = time.time()
	for item in value:
		file.write(str(item)+" ")
		iterator += 1
		if (iterator % 50) == 0:
			file.write("\n")
	writeend = time.time()
	writetotal = writeend - writestart
	file.write("\n-----------------------------\nTotal time to process: " + str(total))
	file.write("\nTotal time to write: " + str(writetotal))
	file.write("\nEnd of Test")
	file.close()

# 9 cores: 13.87118148803711
# 12 cores: 12.349988222122192