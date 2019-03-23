import os 
import platform 
import csv 
import sys 
import boto3 
import paramiko 
import time

def get_instance(instance_file_path):
	created_instance = []
	with open(instance_file_path, newline='') as csvfile:
	# reads each entry
		instanceRead = csv.reader(csvfile, delimiter=',', quotechar="|")
	# appends that entry to the created_instance list
	for instance in instanceRead:
		created_instances.append(instance)
    # closes the csv file when done
	csvfile.close()
	fixed_file = []
	for item in created_instances[0]:
		fixed_file.append(item)
	
	created_instances = fixed_file
    # returns a list of the created instances
	return created_instances
	
def create_instance_addresses(created_instances):
    # empty list for server dns that we will use to ssh to servers with
    server_dns = []
    # for each element in created_instances
    for instance in created_instances:
	# load the instance from aws to ensure its current
        instance.load()
	# we get a string name of the dns from the instance object
        instance_name = str(instance.public_dns_name)
	# we append that name to the list
        server_dns.append(instance_name)
	# return list of dns names
    return server_dns

def run_server(instance_file_name, keyname):
    # appends the .pem extension to the string of the keyname
	keyname = str(keyname) + ".pem"
    # gets the current working path that we want to remember
	current = str(os.getcwd())
    # if on a windows computer we use windows formatting
	if platform.system() == "Windows":
		shellPath = current + "\\shell"
		instancePath = current + "\\instances"
		instanceNamePath = current + "\\instances\\" + str(instance_file_name)
		key = current + "\\keys" + "\\" + str(keyname)
    # else we use Linux formating (Mac shares this formating?)
	else:
		shellPath = current + "/shell/"
		instancePath = current + "/instances/"
		instanceNamePath = current + "/instances/" + str(instance_file_name)
		key = current + "/keys/" + str(keyname)
    # instances files are put into a list from the instance folder
	instanceFiles = os.listdir(instancePath)
    # shell files are put into list from the shell folder
	shellFiles = os.listdir(shellPath)
    # while the instance file doesn't exist or is 'seen' yet
	FileExists = False
    # for each file in the list of files from instance folder
	for file in instanceFiles:
	# if it is the same name as the instance file we want
		if str(instance_file_name) == file:
			# it exists
			FileExists = True
        # if it exists we can create the instance objects
	if FileExists:
		createdInstances = get_instances(instanceNamePath)
		print(createdInstances)
        # else it doesn't exist and we leave the program to avoid bad errors :(
	else:
		print("Was unable to parse instances from file")
		sys.exit()
	
    # we get all the files in the shell folder
	for file in shellFiles:
		print(file)
		if str(file) == "shell-template.txt":
			shellFiles.remove(file)
    # sorts the shell files so they are from 1 to n
	shellFiles.sort()
    # creates ec2 resource to deal with instances
	ec2 = boto3.resource('ec2')
	runningInstances = []
    # makes a list of running instances and gets the instances from instance file
	for instance in createdInstances:
		if len(str(instance)) >= 2:
			runningInstances.append(ec2.Instance(instance))
    # gets dns address after creating instances from the determined running instances
	dnsAddresses = create_instance_addresses(runningInstances)
    # sets up SSH client using paramiko
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # for each running instance
	for i in range(len(runningInstances)):
	# we connect to the instance with the dns address and key
		print("\n--------------------\nConnecting to Server:", runningInstances[i])
		client.connect(dnsAddresses[i], username='ubuntu', key_filename=key)
		print("Connection successful")
	# we change to sudo user
		getSudo = "sudo -i"
	# we cd to our main directory
		getServerFolder = "cd /home/ubuntu/"
		print("Changing to root")
		print("Changing to: /home/ubuntu/")
		client.exec_command(getSudo)
		client.exec_command(getServerFolder)
		print("Entering server folder")
		print("Running server program")
	# we run the command to run the shell script that excutes all the
	# script processe 
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
	# once we start running, we disconnect from the server
		print("Closing connection to server")
		client.close()
	print("--------------------\nCompleted")
	return