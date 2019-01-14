"""

Generates a shell script that uses the name of a main program that will run on the AWS servers for Eclipse MegaMovie
data processing

Written by: David Story

"""
import sys, os, boto3, csv
import datetime

def create_shell(main_program, serverNumber):
    # opens and reads template
    template = open("shell-template.txt", "r")
    contents = template.read()

    # makes shell name
    shell_name = "ECMEGA-Program-Run-" + str(serverNumber) + ".sh"

    # opens shell file and writes contents
    shellFile = open(shell_name, "w")
    shellFile.write(contents)

    # creates strings for new shell contents with program name
    py_output_file = "\npyout=`date +\"PythonOutput-\"%Y-%m-%d.%H:%M:%S\".txt\"`\n"
    exit_file = "pyexit=`date +\"ExitOutput-\"%Y-%m-%d.%H:%M:%S\".txt\"`\n"
    program_line = "sudo python " + str(main_program) + " > $pyout\n"
    exit_code = "sudo echo $? > $pyexit\n"
    moveLog = "sudo mv $pyout log/\n"
    moveExit = "sudo mv $pyexit output/\n"

    if (int(serverNumber) > 0):
        tarstring = "SERVER_" + str(serverNumber)
        tarstring = "tarname=`date +\"" + tarstring +"_RUN_FILES_\"%Y_%m_%d_%H_%M_%S\".tgz\"`\n"
    else:
        sys.exit(-1)
    tarFiles = "tar -zcvf $tarname .\n"
    awsCopy = "sudo aws s3 cp $tarname s3://ecmega-project-bucket/server-outputs/\n"

    lineList = [py_output_file, exit_file, program_line, exit_code, moveLog, moveExit,
                tarstring, tarFiles, awsCopy]
    shellFile = ez_write(lineList, shellFile)

    # closes file
    shellFile.close()

    os.chmod(shell_name, 755)

    return shellFile

def ez_write(list, file):
    for items in list:
        file.write(items)
    return file

def create_instance_address(created_instances):
    server_dns = []
    for instance in created_instances:
        instance.load()
        instance_name = "ubuntu@" + str(instance.public_dns_name)
        server_dns.append(instance_name)
    return server_dns

def create_log_file(instances, choice, mainScript, list):
    try:
        date_time_str = str(datetime.datetime.now()).split()
        date_time_str = date_time_str[0]
        logName = "ecmega-server-log-" + str(date_time_str) +".txt"
        logFile = open(logName, 'w')

        logFile.write("- ECMEGA Server Log -\nCreated at:")
        logFile.write(str(datetime.datetime.now()))
        logFile.write("\n")
        logFile.write("------------- Instance Information -------------\n")

        instance_iter = 1
        for instance in instances:
            logFile.write("\n")
            instance.load()
            instanceName = "\tInstance Name: " + str(instance.tags) + "\n"
            instanceId = "\tInstance Id: " + str(instance.id) + "\n"
            instanceDNS = "\tInstance connection name: " + str(instance.public_dns_name) + "\n"
            instanceKey = "\tInstance Key: " + str(instance.key_name) + "\n"
            instanceSG = "\tInstance SG: " + str(instance.security_groups) + "\n"
            instanceImage = "\tInstance Image: " + str(instance.image_id) + "\n"
            instanceStat = "\tCurrent Status: " + str(instance.state) + "\n"

            instance_iter_text = "Instance Number: " + str(instance_iter) + "\n"
            instance_iter += 1

            logFile.write(instance_iter_text)
            logFile.write(instanceName)
            logFile.write(instanceId)
            logFile.write(instanceDNS)
            logFile.write(instanceKey)
            logFile.write(instanceSG)
            logFile.write(instanceImage)
            logFile.write(instanceStat)


        logFile.write("------------- End Instance Info -------------\n")
        logFile.write("------------- Program Information -------------\n")
        mainInfo = "Main script: " + str(mainScript) + "\n"
        logFile.write(mainInfo)
        logFile.write("Supporting files:\n")
        for files in list:
            logFile.write(str(files))
            logFile.write("\n")

        logFile.write("------------- End Program Info -------------\n")
        logFile.write("------------- Copy & Machine Info -------------\n")
        copyInfo = "Copying files from: " + str(choice) + "\n"
        logFile.write(copyInfo)
        logFile.write("---------------- End All Info -----------------\n")
        logFile.close()
    except:
        return -1

    return logFile

def create_instance_file(created_instances):
    date_time_str = str(datetime.datetime.now()).split()
    date_time_str = date_time_str[0]
    fileName = "ecmega-instance-file-" + str(date_time_str) + ".csv"

    with open(fileName, "w", newline="") as csvFile:
        csvWriter = csv.writer(csvFile)
        for instance in created_instances:
            csvFile.write(str(instance))
            csvFile.write(",")
        csvFile.close()

    return csvFile

def create_log(created_instances, choice, mainSoftware, softwareList):
    server_address = create_instance_address(created_instances)
    log = create_log_file(created_instances, choice, mainSoftware, softwareList)
    return log

create_shell("ServerTesters.py", 1)

file = []
for i in range(5):
    file.append(i)