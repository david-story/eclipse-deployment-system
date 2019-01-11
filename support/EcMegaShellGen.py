"""

Generates a shell script that uses the name of a main program that will run on the AWS servers for Eclipse MegaMovie
data processing

Written by: David Story

"""
import sys

def create_shell(program, parameters):
    # creates shell name
    minusExt = len(program) - 3
    name = str(program[:minusExt]) + "-ECMEGA-AWS-RUN.sh"

    # opens shell template and gets information
    temp = open('shell-template.txt', 'r')
    hold = temp.read()
    temp.close()

    # writes to new shell file
    shellFile = open(name, 'w')
    shellFile.write(hold)

    # writes main program
    shellFile.write("\npython " + str(program))

    # writes all parameters
    if (parameters != None) and (len(parameters) > 0):
        for item in parameters:
            shellFile.write(" "+str(item))

    shellFile.close()


def run_gen():
    args = sys.argv
    argc = len(args)
    #print("Passed arguments:", args)
    #print("Total number of arguments:", argc)

    # mode when just entering in program with no parameter files

    if argc < 2:
        sys.exit(-1)
    elif argc == 2:
        program = args[1]
        create_shell(program, None)

        #print("Main program to run:", program)
        #print("No Parameters")

    elif argc > 2:
        program = args[1]
        parameters = args[2:]
        create_shell(program, parameters)

        #print("Main program to run:", program)
        #print("Program Parameters:", parameters)
    else:
        sys.exit(-2)
