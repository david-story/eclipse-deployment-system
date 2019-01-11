import sys
import time
import paramiko

def copy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect("ec2-13-58-27-182.us-east-2.compute.amazonaws.com",
                   username="ubuntu", key_filename="C:\\Users\\David\\Documents\\AWSKeys\\DavidDesktop.pem")

    sftp = client.open_sftp()
    print("Successfully opened SFTP")
    sftp.close()

