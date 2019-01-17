import os
import platform
import csv
import sys
import boto3
import paramiko
import time


def get_instances(instance_file_path):
    created_instances = []
    with open(instance_file_path, newline='') as csvfile:
        instanceRead = csv.reader(csvfile, delimiter=',', quotechar="|")
        for instance in instanceRead:
            created_instances.append(instance)
    csvfile.close()
    fixed_file = []
    for item in created_instances[0]:
        fixed_file.append(item)
    created_instances = fixed_file

    return created_instances


def create_instance_addresses(created_instances):
    server_dns = []
    for instance in created_instances:
        instance.load()
        instance_name = str(instance.public_dns_name)
        server_dns.append(instance_name)

    return server_dns


def run_server(instance_file_name, keyname):
    keyname = str(keyname) + ".pem"
    current = str(os.getcwd())
    if platform.system() == "Windows":
        shellPath = current + "\\shell"
        instancePath = current + "\\instances"
        instanceNamePath = current + "\\instances\\" + str(instance_file_name)
        key = current + "\\keys" + "\\" + str(keyname)
    else:
        shellPath = current + "/shell/"
        instancePath = current + "/instances/"
        instanceNamePath = current + "/instances/" + str(instance_file_name)
        key = current + "/keys/" + str(keyname)

    instanceFiles = os.listdir(instancePath)
    shellFiles = os.listdir(shellPath)

    FileExists = False
    for file in instanceFiles:
        if str(instance_file_name) == file:
            FileExists = True
    if FileExists:
        createdInstances = get_instances(instanceNamePath)
        print(createdInstances)
    else:
        print("Was unable to parse instances from file")
        sys.exit()

    for file in shellFiles:
        print(file)
        if str(file) == "shell-template.txt":
            shellFiles.remove(file)
    shellFiles.sort()

    ec2 = boto3.resource('ec2')
    runningInstances = []
    for instance in createdInstances:
        if len(str(instance)) >= 2:
            runningInstances.append(ec2.Instance(instance))
    dnsAddresses = create_instance_addresses(runningInstances)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in range(len(runningInstances)):
        print("\n--------------------\nConnecting to Server:", runningInstances[i])
        client.connect(dnsAddresses[i], username='ubuntu', key_filename=key)
        print("Connection successful")
        getSudo = "sudo -i"
        getServerFolder = "cd /home/ubuntu/"
        print("Changing to root")
        print("Changing to: /home/ubuntu/")
        client.exec_command(getSudo)
        client.exec_command(getServerFolder)
        print("Entering server folder")
        print("Running server program")
        sudoCommand = "sudo ./" + str(shellFiles[i])
        print("Running shell script with:", sudoCommand)
        client.exec_command(sudoCommand)

        """
        do1 = "tarname=`date +\"SERVER_2_RUN_FILES_\"%Y_%m_%d_%H_%M_%S\".tgz\"`"
        do2 = "tar -zcvf $tarname ./server/"
        do3 = "sudo aws s3 cp $tarname s3://ecmega-project-bucket/server-outputs/"

        print("Changing to: /home/ubuntu/")
        client.exec_command(do1)
        print("taring file")
        client.exec_command(do2)
        print("sending to s3")
        client.exec_command(do3)
        """

        print("Closing connection to server")
        client.close()
    print("--------------------\nCompleted")
    return

