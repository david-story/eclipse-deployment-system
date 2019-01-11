"""

Generates a shell script that uses the name of a main program that will run on the AWS servers for Eclipse MegaMovie
data processing

Written by: David Story

"""
import sys, os, boto3
import datetime

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

def create_instance_address(created_instances):
    server_dns = []
    for instance in created_instances:
        instance.load()
        instance_name = "ubuntu@" + str(instance.public_dns_name)
        server_dns.append(instance_name)
    return server_dns

def create_log_file(instances, choice, mainScript, list):
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
    return



def run_gen(created_instances, choice, mainSoftware, softwareList):

    server_address = create_instance_address(created_instances)
    log = create_log_file(created_instances, choice, mainSoftware, softwareList)

    return log, server_address


