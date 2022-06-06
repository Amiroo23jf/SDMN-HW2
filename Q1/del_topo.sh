# This script deletes namespaces and bridges created by create_topo.sh
ip netns del node1
ip netns del node2
ip netns del node3
ip netns del node4
ip netns del router
ip link del br1
ip link del br2
