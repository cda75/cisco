import paramiko
import time
from ConfigParser import SafeConfigParser
import argparse



def runHostCommands(host,user,password,commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username = user, password = password)
    shell = ssh.invoke_shell()
    print "[+] ... SSH connection established to %s" %host
    for command in commands:
        shell.send("terminal length 0\n")
        time.sleep(1)
        shell.recv(1000)
        shell.send('\n')
        shell.send(command+'\n')
        time.sleep(1)
        print shell.recv(65535)
        print '------------------------------------------------------------------------------'
        print '\n'


def runCmd(conf='sw.conf', os = 'all'):
    config = SafeConfigParser()
    config.read(conf)
    user = config.get('AAA', 'User')
    password = config.get('AAA', 'Password')
    hosts = dict(config.items('HOSTS'))
    commands = dict(config.items('COMMANDS'))
    for k,v in hosts.iteritems():
        hosts[k] = filter(None, [ip.strip() for ip in v.splitlines()])
    for k,v in commands.iteritems():
        commands[k] = filter(None, [cmd.strip() for cmd in v.splitlines()])
    if os != 'all':
        for host in hosts[os]:
            runHostCommands(host, user, password, commands[os])
    else:
        for os, ip in hosts.iteritems():
            for host in ip:
                runHostCommands(host, user, password, commands[os])



def main():
# Persing arguments from commmand line
# Default value - all devices
    parser = argparse.ArgumentParser(description='Running commands in batch mode via ssh-shell')
    parser.add_argument("-conf", type=str, dest='conf', default='sw.conf', help='Configuration File')
    parser.add_argument("-os", type=str, dest='os', default='all', help='Tag of devices group or <all> for every device in config file')
    args = parser.parse_args()
    conf = args.conf
    os = args.os
# Run main 
    runCmd(conf, os)



if __name__ == '__main__':
    main()


