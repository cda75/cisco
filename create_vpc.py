import cli
import argparse

parser = argparse.ArgumentParser(description='Creating vpc Port-channel on Nexus switches')
parser.add_argument("-int", type=str, dest='intf')
parser.add_argument("-vpc", type=str, dest='vpc')
parser.add_argument("-vlans", type=str, default = 'all', nargs='+', dest='vlans')
parser.add_argument("-end", type=str, default = 'host', dest = 'end_point')
args = parser.parse_args()

vlans = args.vlans
intf = args.intf
vpc = args.vpc
end_point = args.end_point

if vlans == 'all':
	vlans = ''
else:
	vlans = vlans[0]

if end_point == 'host':
	stp = 'spanning-tree port type edge trunk'
else:
	stp = ''

peer_link = cli.cli("sh vpc br | xml | grep peerlink-ifindex | sed 's/<[^>]*>//g'")
pl = peer_link.strip()

cmd1 = "conf t ; int %s ; channel-gr %s ; no shut ; int Po%s ; sw mode tru ; sw tr all vl %s ; vpc %s ; %s ; no shut" %(intf,vpc,vpc,vlans,vpc,stp)
cli.cli(cmd1)

cmd2 = "conf t ; int %s ; sw tr all vl add %s" %(pl,vlans)
cli.cli(cmd2)

cmd3 = "sh run int %s ; sh run int po%s, %s" %(intf,vpc,pl)
print cli.cli(cmd3)






