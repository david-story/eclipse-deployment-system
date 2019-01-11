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
    for instance_list in created_instances:
        for instance in instance_list:
            instance.load()
            instance_name = "ubuntu@" + str(instance.public_dns_name)
            server_dns.append(instance_name)
    return server_dns

def create_log_file(instances, choice, mainScript, list):
    date_time = str(datetime.datetime.now())
    logName = "ecmega-server-log-" + str(datetime) +".txt"
    logFile = open(logName, 'w')

    logFile.write("- ECMEGA Server Log -\nCreated at:")
    logFile.write(datetime)
    logFile.write("------------- Instance Information -------------")
    for instance in instances:
        instance.load()
        instanceName = "Instance Name: " + str(instance.tags)
        instanceId = "Instance Id: " + str(instance.id)
        instanceDNS = "Instance connection name: " + str(instance.public_dns_name)
        instanceKey = "Instance Key: " + str(instance.key_name)
        instanceSG = "Instance SG: " + str(instance.security_groups)
        instanceImage = "Instance Image: " + str(instance.image_id)
        instanceStat = "Current Status: " + str(instance.state)

        logFile.write(instanceName)
        logFile.write(instanceId)
        logFile.write(instanceDNS)
        logFile.write(instanceKey)
        logFile.write(instanceSG)
        logFile.write(instanceImage)
        logFile.write(instanceStat)
    logFile.write("------------- Instance Information -------------\n")
    logFile.write("------------- Program Information -------------")
    mainInfo = "Main script: " + str(mainScript)
    logFile.write(mainInfo)
    logFile.write("Supporting files:")
    for files in list:
        logFile.write(files)
    logFile.write("------------- End Program Info -------------\n")
    logFile.write("------------- Copy & Machine Info -------------")
    copyInfo = "Copying files from: " + str(choice)
    logFile.write(copyInfo)
    logFile.write("---------------- End All Info -----------------")
    logFile.close()
    return



def run_gen(created_instances, choice, mainSoftware, softwareList):

    server_address = create_instance_address(created_instances)
    log = create_log_file(created_instances, choice, mainSoftware, softwareList)

    return log


