import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.0.128.31',username = 'cda75',password = 'P@ssw0rd')

def get_vrf_int(vrf='all'):
    command = 'sh ip int br vrf ' + vrf
    stdin,stdout,stderr = ssh.exec_command(command)
    vrf_int = {}
    lines = stdout.readlines()
    for line in lines:
        s = line.strip().split(' ')
        line = [str(i) for i in s if i != '']
        if 'VRF' in line:
            vrf_new = str(line[5].replace('"','')[:-3])
            vrf_int[vrf_new] = {'interfaces':[]}
        if ('IP' in line) or (line == []):
            continue
        interface, ip, status = line
        i = status.find('-')
        j = status.find('/')
        status = status[i+1:j]
        vrf_int[vrf_new]['interfaces'].append({'interface':interface,'ip':ip,'status':status})
    return vrf_int


def print_vrf_int(vrf='all'):
    vrf_out = get_vrf_int(vrf)
    for k, v in vrf_out.iteritems():
        print '\n','VRF:\t%s' %k
        intf = v['interfaces']
        for i in intf:
            interface,ip,status = i.values()
            print '%s\t%s\t%s' %(interface,ip,status)


def get_vrf_routes(vrf='all'):
    command = 'sh ip route vrf ' + vrf
    stdin,stdout,stderr = ssh.exec_command(command)
    vrf_rt = {}
    lines = stdout.readlines()
    for line in lines:
        print line

get_vrf_routes()








