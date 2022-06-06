ip_dest="" # the ip of the second node


# finding the ip of the first node
if [ "$2" = "node1" ]; then
    ip_dest="172.0.0.2"
    echo "1"
elif [ "$2" = "node2" ]; then
    ip_dest="172.0.0.3"
    echo "2"
elif [ "$2" = "node3" ]; then
    ip_dest="10.10.0.2"
elif [ "$2" = "node4" ]; then
    ip_dest="10.10.0.3"
elif [ "$2" = "router"]; then
    ip_dest="10.10.0.1"
else
    echo "Error: Invalid second node"
    exit
fi

# starting the pinging
ip netns exec $1 ping $ip_dest
