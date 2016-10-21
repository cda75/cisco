import paramiko
import time
from ConfigParser import SafeConfigParser


def getCred(conf = 'sw.conf'):
    config = SafeConfigParser()
    config.read(conf)
    user = config.get('AAA', 'User')
    password = config.get('AAA', 'Password')
    return user, password


def readSwIp(conf = 'sw.hosts'):
    with open(conf) as f:
        swIp = [x.strip('\n') for x in f.readlines() if x.strip() != '']
    return swIp


def readSwCmd(conf = 'sw.cmd'):
    with open(conf) as f:
        cmd = [x for x in f.readlines() if x.strip() != '']
    return cmd


def getVersion(host, user, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username = user, password = password)
    stdin,stdout,strerr = ssh.exec_command('show version')
    return stdout.read()


def runCommands(host,user,password,cmdList):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username = user, password = password)
    print "[+] ... SSH connection established to %s" %host
    shell = ssh.invoke_shell()
	shell.send("terminal length 0\n")
    for command in cmdList:
        time.sleep(1)
        shell.recv(1000)
        shell.send('\n')
        shell.send(command)
        time.sleep(2)
        print shell.recv(65535)
        print '------------------------------------------------------------------------------'


def main():
    hosts = readSwIp()
    user, password = getCred()
    commands = readSwCmd()

    for host in hosts:
        runCommands(host, user, password, commands)



if __name__ == '__main__':
    main()




