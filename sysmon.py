from flask import Flask
app = Flask(__name__)

from os import system
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException


@app.route('/sysmon')
def sysmon():
    return remote_call("hostname")

def remote_call(command):
    host = "polarbear.vs.mythic-beasts.com"
    username = "root"
    key_path = "/Users/daveh/.ssh/id_rsa"

    try:
        ssh_key = RSAKey.from_private_key_file(key_path)
        print(f"Found SSH key at self {key_path}")
    except SSHException as e:
        print(e)

    try:
        system(f"ssh-copy-id -i {key_path}.pub {username}@{host}>/dev/null 2>&1")
        print(f"{key_path} uploaded to {host}")
    except FileNotFoundError as error:
        print(error)

    try:
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            host,
            username=username,
            password="",
            key_filename=key_path,
            timeout=5000,
            )
    except AuthenticationException as e:
        print(f"Authentication failed: did you remember to create an SSH key? {e}")
        raise e

    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()
    response = stdout.readlines()
    for line in response:
        print(line)

    if client:
        client.close()

    return line
