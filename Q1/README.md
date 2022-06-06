This directory contains the scripts needed for Question 1.

## Creating the topology
In order to create the topology we first added the namespaces using the command below:
```
ip netns add <NAMESPACE-NAME>
```

Then we should add two bridges using the following commad:
```
ip link add <Bridge-Name> type bridge
```

Afterwards, the virtual interfaces of the namespaces should be created using the following command:
```
ip link add <Interface-Name> type veth peer name <Peer-Name>
```
