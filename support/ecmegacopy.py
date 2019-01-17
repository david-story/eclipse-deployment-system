import paramiko
import time
import boto3
import platform
import os
import csv
import sys

"""
connection.py 

This file connects to EC2 instances for the AWS deployment notebook by using 
paramiko for ssh and sftp

written by: David Story

"""
"""
deF sample_copy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('ec2-18-188-214-186.us-east-2.compute.amazonaws.com', username='ubuntu', key_filename='ecmega-master-key.pem')
    print("Opened server!")
    sftp = client.open_sftp()
    print("Opened Safe Transfer Protocal!")
    sftp.put('sunspot.txt','/home/ubuntu/sunspots.txt')
    client.close()
    print("Connection closed!")
"""


def send_to_server(instances, key, software_files, shell_files, addresses, software_path, shell_path):
    try:

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # for each instances
        for i in range(len(instances)):
            # first connect to server using paramiko ssh function .connect, with our current dns address
            # and our given user and ssh key
            print("\n--------------------\nConnecting to Server:", instances[i])
            client.connect(addresses[i], username='ubuntu', key_filename=key)

            # we will create a folder that will be where we have all our software and outputs,
            # as well as where we run our code
            client.exec_command("sudo mkdir \"server\"")

            # we will also give our folder full permissions
            print("Giving server folder permissions")
            client.exec_command("sudo chmod 755 server")

            # we will now open a safe FTP channel to transfer our local files to the machine
            print("Connection successful")
            sftp = client.open_sftp()
            print("Opened SFTP")

            # for each file in our software list
            for file in software_files:
                # determine the type of local machine so we can create our path
                if platform.system() == "Windows":
                    local_path = str(software_path) + "\\" + str(file)

                else:
                    local_path = str(software_path) + str(file)

                # create the remote path with our new file that we would like to add
                remote_path = "/home/ubuntu/" + str(file)
                print("Remote:", remote_path)
                # remote_path = str(file)

                # send a new file to that path
                print("Sending software from this path to server:", local_path)
                sftp.put(local_path, remote_path)

                # we copy that new file in the server to the server folder
                print("Moving software file to server folder")
                move_file = "sudo mv " + str(file) + " server"
                client.exec_command(move_file)

            # determine system for our shell file local path
            if platform.system() == "Windows":
                local_shell = str(shell_path) + "\\" + str(shell_files[i])
            else:
                local_shell = str(shell_path) + str(shell_files[i])

            # we send the shell file from the local folder to the server
            print("Sending shell from this path to server:", local_shell)
            # we generate the local path name
            remote_shell = "/home/ubuntu/" + str(shell_files[i])
            # remote_shell = str(shell_files[i])
            # we transfer the file using SFTP
            sftp.put(local_shell, remote_shell)

            # cleans the shell file for any Windows formatting shenanigans
            print("Cleaning shell file")
            client.exec_command("sudo sed -i -e 's/\r$//' " + str(shell_files[i]))
            # does one of those good old 'add permissions' stuff to the file
            print("Modifying shell file permissions")
            client.exec_command("sudo chmod 755 " + str(shell_files[i]))

            # we move the shell file to the server folder
            print("Moving shell file to server folder")
            move_shell = "sudo mv " + str(shell_files[i])
            client.exec_command(move_shell)

            # we close the client
            client.close()
            print("Closing server\n--------------------")

        print("Successfully copied files to all servers.")
    except:
        print("Error: Could not copy files to servers, shutting down.")
        sys.exit(-5)



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


def make_paths(instancename, keyname):
    if platform.system() == "Windows":
        current = str(os.getcwd())
        shell = current + "\\shell"
        key = current + "\\keys"
        keyname = current + "\\keys" + "\\" + str(keyname) + ".pem"
        software = current + "\\software"
        instancePath = current + "\\instances"
        instanceNamePath = current + "\\instances\\" + str(instancename)
    else:
        current = str(os.getcwd())
        shell = current + "/shell/"
        key = current + "/keys/"
        keyname = current + "/keys/" + str(keyname) + ".pem"
        software = current + "/software/"
        instancePath = current + "/instances/"
        instanceNamePath = current + "/instances/" + str(instancename)

    return current, shell, key, keyname, software, instancePath, instanceNamePath


def get_dir_contents(shell_path, key_path, software_path, instance_path):
    shellFiles = os.listdir(shell_path)
    keyFiles = os.listdir(key_path)
    softFiles = os.listdir(software_path)
    instanceFiles = os.listdir(instance_path)

    for file in shellFiles:
        print(file)
        if str(file) == "shell-template.txt":
            shellFiles.remove(file)

    return shellFiles, keyFiles, softFiles, instanceFiles


def local_copy_to_servers(instance_file_name, keyname):
    # creates paths to all folders
    current_path, shell_path, key_path, keyname_path, software_path, \
    instance_path, instanceName_path = make_paths(instance_file_name, keyname)

    # creates list of file contents
    shellFiles, keyFiles, softFiles, instanceFiles = get_dir_contents(shell_path, key_path,
                                                                      software_path, instance_path)
    FileExists = False
    for file in instanceFiles:
        if str(instance_file_name) == file:
            FileExists = True
    if FileExists:
        createdInstances = get_instances(instanceName_path)
        print(createdInstances)
    else:
        print("Was unable to parse instances from file")
        sys.exit()

    ec2 = boto3.resource('ec2')
    runningInstances = []
    for instance in createdInstances:
        if len(str(instance)) >= 2:
            runningInstances.append(ec2.Instance(instance))
    dnsAddresses = create_instance_addresses(runningInstances)
    shellFiles.sort()
    print(shellFiles)
    print(softFiles)
    print(shellFiles)
    print(software_path)
    print(shell_path)
    send_to_server(runningInstances, keyname_path, softFiles, shellFiles, dnsAddresses, software_path, shell_path)

    return
