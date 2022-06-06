This directory contains the scripts needed for Question 1.

**Note:** In my Virtual Machine, the parameters `net.bridge.bridge-nf-call-iptables`, `net.bridge.bridge.bridge-nf-call-ip6tables` and `net.bridge.bridge-nf-call-arptables` were set to 1 by default. In order to let iptables handle bridged packets and route the traffic automatically this parameters should be set to 1 using the following code (You might not face any issue if these parameters were set to 0 by default in your OS, if so ignore this part):
```
echo "0" > /proc/sys/net/bridge/bridge-nf-call-iptables
echo "0" > /proc/sys/net/bridge/bridge-nf-call-ip6tables
echo "0" > /proc/sys/net/bridge/bridge-nf-call-arptables
```
## Creating the topology
In order to create the topology the namespaces should be added using the command below:
```
ip netns add <Namespace-Name>
```

Then two bridges should be addded and set to up using the following commands:
```
ip link add <Bridge-Name> type bridge
ip link set dev <Bridge-Name> up
```

Afterwards, the virtual interfaces of the namespaces should be created using the following command:
```
ip link add <Interface-Name> type veth peer name <Peer-Name>
```

After creating the interfaces and bridges, it is time to assign the interfaces to their namespaces and the setting the master of each veth using the following command:
```
ip link set <Interface-Name> netns <Namespace-Name>
ip link set <Peer-Name> master <Bridge-Name>
```

Next, the ip addresses of each interface should be added and set to up:
```
ip -n <Namespace-Name> addr add <ip-address> dev <Interface-Name>
ip -n <Namespace-Name> link set <Interface-Name> up
```

Finally the default gateways of the nodes should be set to the router:
```
ip netns exec <Namespace-Name> route add default via <Gateway>
```
