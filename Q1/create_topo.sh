# creating namespaces
ip netns add node1
ip netns add node2
ip netns add node3
ip netns add node4
ip netns add router

# creating bridges and virtual interfaces
ip link add br1 type bridge
ip link set br1 up
ip link add veth-node1 type veth peer name veth-node1-br
ip link add veth-node2 type veth peer name veth-node2-br
ip link add veth-router-1 type veth peer name veth-router-br1

ip link add br2 type bridge
ip link set br2 up
ip link add veth-node3 type veth peer name veth-node3-br
ip link add veth-node4 type veth peer name veth-node4-br
ip link add veth-router-2 type veth peer name veth-router-br2

# Assigning veths to namespaces
ip link set veth-node1 netns node1
ip link set veth-node2 netns node2
ip link set veth-node3 netns node3
ip link set veth-node4 netns node4
ip link set veth-router-1 netns router
ip link set veth-router-2 netns router

# Assigning each veth peer to the bridges
ip link set veth-node1-br master br1
ip link set veth-node2-br master br1
ip link set veth-router-br1 master br1

ip link set veth-node3-br master br2
ip link set veth-node4-br master br2
ip link set veth-router-br2 master br2

# Adding ip addresses to interfaces
ip -n node1 addr add 172.0.0.2/24 dev veth-node1
ip -n node2 addr add 172.0.0.3/24 dev veth-node2
ip -n router addr add 172.0.0.1/24 dev veth-router-1

ip -n node3 addr add 10.10.0.2/24 dev veth-node3
ip -n node4 addr add 10.10.0.3/24 dev veth-node4
ip -n router addr add 10.10.0.1/24 dev veth-router-2

ip -n node1 link set dev veth-node1 up
ip -n node2 link set dev veth-node2 up
ip -n node3 link set dev veth-node3 up
ip -n node4 link set dev veth-node4 up
ip -n node1 link set dev lo up
ip -n node2 link set dev lo up
ip -n node3 link set dev lo up
ip -n node4 link set dev lo up

ip -n router link set dev veth-router-1 up
ip -n router link set dev veth-router-2 up
ip -n router link set dev lo up

ip link set veth-node1-br up
ip link set veth-node2-br up
ip link set veth-node3-br up
ip link set veth-node4-br up
ip link set veth-router-br1 up
ip link set veth-router-br2 up

# Adding default gateway
ip netns exec node1 ip route add default via 172.0.0.1
ip netns exec node2 ip route add default via 172.0.0.1

ip netns exec node3 ip route add default via 10.10.0.1
ip netns exec node4 ip route add default via 10.10.0.1

