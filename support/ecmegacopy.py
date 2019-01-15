import boto3
import os
import platform
import paramiko

def copy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect("ec2-13-58-27-182.us-east-2.compute.amazonaws.com",
                   username="ubuntu", key_filename="C:\\Users\\David\\Documents\\AWSKeys\\DavidDesktop.pem")

    sftp = client.open_sftp()
    print("Successfully opened SFTP")
    sftp.close()


def create_instance_address(created_instances):
    server_dns = []
    for instance in created_instances:
        instance.load()
        instance_name = "ubuntu@" + str(instance.public_dns_name)
        server_dns.append(instance_name)

    return server_dns


def makePaths(keyname):
    if str(platform.system()) == "Windows:":
        current = str(os.getcwd())
        shell = current + "\\shell"
        key = current + "\\keys"
        keyname = current + "\\keys" + "\\" + str(keyname)
        software = current + "\\software"
    else:
        current = str(os.getcwd())
        shell = current + "/shell/"
        key = current + "/keys/"
        keyname = current + "/keys/" + "/" + str(keyname)
        software = current + "/software/"

    return current, shell, key, keyname, software


def get_dir_contents(shell_path, key_path, software_path):
    shellFiles = os.listdir(shell_path)
    keyFiles = os.listdir(key_path)
    softFiles = os.listdir(software_path)

    for file in shellFiles:
        if str(file) == "shell-template.txt":
            shellFiles.pop()

    return shellFiles, keyFiles, softFiles


def copy_files(created_instances, keyname):
    # creates paths to all folders
    current_path, shell_path, key_path, keyname_path, software_path = makePaths(keyname)
    # creates dns address for each instance type
    shellFiles, keyFiles, softFiles = get_dir_contents(shell_path, key_path, software_path)
    client = paramiko.SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # creates server address from DNS
    instance_list = create_instance_address(created_instances)

    shell_iter = 0
    for instance in instance_list:
        client.connect(instance, username="ubuntu", key_filename=keyname_path)
        sftp = client.open_sftp()
        print("Opened:", instance)
        sftp.close()
        shell_iter += 1

    return
