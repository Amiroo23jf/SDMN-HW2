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
ip link set <Bridge-Name> up
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
ip -n <Namespace-Name> link set dev <Interface-Name> up
```

Finally the default gateways of the nodes should be set to the router:
```
ip netns exec <Namespace-Name> route add default via <Gateway>
```

**Note:** An extra script called "del_topo.sh" is also created that reverses all the changes that "create_topo.sh" makes including the namespaces and bridges.

## ping_nodes.sh script
This script simply finds the ip from the name of the given node and then, it runs the following command:
```
ip netns exec <First-Namespace-Name> ping <Second-Namespace-IP>
```

## What happens if the router namespace is removed?
In this case, we should add 6 new ip rules, 1 in each new namespace and 2 for the root namespace. The rules which are for the new namespaces simply state that we should route the packets which are destined for a different subnet to the interface connected to the bridge:
```
sudo ip netns exec node1 ip route add 10.10.0.0/24 dev veth-node1
sudo ip netns exec node2 ip route add 10.10.0.0/24 dev veth-node2
sudo ip netns exec node3 ip route add 172.0.0.0/24 dev veth-node3
sudo ip netns exec node4 ip route add 172.0.0.0/24 dev veth-node4
```

In addtion, for the rules which are written in the root namespace, we are simply forwarding the packet destined for each subnet to its equivalent bridge as shown below:
```
sudo ip route add 10.10.0.0/24 dev br2
sudo ip route add 172.0.0.0/24 dev b1
```

## What happens if each bridge and the nodes connecting to it were in different VMs
In this case, instead of 6 rules, 8 rules should be added. The 4 rules written in the new namespaces would be the same, but rules in the root namespaces of the VMs would change. We define the interfaces of VM1 and VM2 connected to the switch as `eth1` and `eth2` respectively. Then, the rules for VM1 would be as followed:
```
sudo ip route add 10.10.0.0/24 dev eth1
sudo ip route add 172.0.0.0/24 dev br1
```
And similarly for VM2:
```
sudo ip route add 172.0.0.0/24 dev eth2
sudo ip route add 10.10.0.0/24 dev br2
```

