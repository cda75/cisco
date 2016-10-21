import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.0.128.31',username = 'cda75',password = 'P@ssw0rd')

stdin,stdout,stderr = ssh.exec_command("sh ip int br vrf all")
VRF = {}
lines = stdout.readlines()
for line in lines:
    s = line.strip().split(' ')
    line = [str(i) for i in s if i != '']

    if 'VRF' in line:
        vrf = str(line[5].replace('"','')[:-3])
        VRF[vrf] = {'interfaces':[]}
    if ('IP' in line) or (line == []):
        continue

    interface, ip, status = line
    i = status.find('-')
    j = status.find('/')
    status = status[i+1:j]
    VRF[vrf]['interfaces'].append({'interface':interface,'ip':ip,'status':status})

def print_vrf(*args):
    for k, v in VRF.iteritems():
        for arg in args:
            if  arg != []:
                print '\n','VRF:\t%s' %k
                for i in v[arg]:
                    p1,p2,p3 = i.values()
                    print '%s\t%s\t%s\t' %(p1,p2,p3)



print_vrf('interfaces')







