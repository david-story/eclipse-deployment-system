
def main():
    print("Creating a file")
    newfile = open("output.txt", 'w')
    print("Writing file")
    for i in range(10000):
        newfile.write(str(i)+"\n")
    print("Closing file")
    newfile.close()
    print("Done")
main()