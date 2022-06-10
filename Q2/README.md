## Notes before using the CLI
In this application, in order to use the CLI properly, it should be run using root privilage.

The CLI is written in python3 and in order to run it you should run it using python3 as shown below:
```
$ sudo python3 CLI.py <command>
```

Note that the application uses a directory called "rootfs" which contains the filesystem of ubuntu 20.04. If you already have the filesystem, just create a directory called "rootfs" in the same directory as CLI.py and copy the whole filesystem inside it. Otherwise, run the following command which will automatically create "rootfs" and downloads and saves the Ubunutu 20.04 filesystem inside it using debootstrap.
```
$ sudo ./create_root_fs.sh
```

In the explanation of the CLI, some examples are done in order. These examples are all captured using linux `script` saved in a file called `examples-script`. 
## CLI 
### Architecture
The CLI uses 3 directories for storing containers, storing their namespaces and the rootfs directory which was explained above, and a file as its database. The "rootfs" directory should be created either manually or using the script above. The other files and directories are automatically created by the CLI the first time you run any command. Lets run the command "list" (which is explained later) and see what is the output for the first time:
```
$ sudo python3 CLI.py list
Creating the containers directory...
Containers directory is created.
Creating the namespaces directory...
Namespace directory is created.
Creating database...
Database created.
```

After running the CLI for the first time using any command, the `containers` and `namespaces` directories and `containers_db.json` file are created. Now lets get deeper and find out what is the purpose of each of these files and dirs:
- **containers_db.json:** This file, is a json file containing the pairs of container ID's which is unique for each container and their equivalent hostname (not necessarily unique).
- **containers:** This directory, contains the filesystem of the created containers. This means that everytime a container is created, a directory with the ID of the container as its name is created and the whole filesystem is copied to it (from rootfs).
- **namespaces:** For the sake of persistency and in order to be able to continue using a container from its previous state after closing it, this directory saves the namespaces of each container in a different directory named after the ID of each container.

So now lets move on from the architecture and see how to actually use the CLI in order to create and use containers properly. Overall, the CLI has 4 different commands:
1. `add <hostname> <*memory>`: This command is for adding new containers, the memory argument can be ignored if you do not want any limitation.
2. `start <container-ID> <*memory>`: By using this command you can start an already added container using it's container ID.
3. `del <container-ID>`: Using this command, you can delete a container and every file and directory related to it.
4. `list`: this command lists the `{ <container ID> : <hostname> }` pairs of all added containers (excluding deleted ones)

In the next sections, each of these commands are explained in depth with an example.

### CLI add command
In order to add a new container with a given `hostname`, the following command should be run:
```
$ sudo python3 CLI.py add <hostname>
```
This will create a container with the given hostname, returns its `container-ID` for further use, and opens the bash of the terminal. As an example, I created a new container with the hostname `my-cont-1` and checked if its pid, mnt, uts and net namespaces are different or not:
```
$ sudo python3 CLI.py add my-cont-1
New container ID added to database.
Container successfully created with id: 99546370
root@my-cont-1:/# ### checking the pid namespace
root@my-cont-1:/# ps fax
   PID TTY      STAT   TIME COMMAND
     1 ?        S      0:00 bash
     4 ?        R+     0:00 ps fax
root@my-cont-1:/# ### checking net namespace
root@my-cont-1:/# ip addr
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
root@my-cont-1:/# ### checking the mount namespace
root@my-cont-1:/# mount 
/dev/sda1 on /proc type ext4 (rw,relatime,errors=remount-ro)
proc on /proc type proc (rw,relatime)
root@my-cont-1:/# ### checking the uts namespace
root@my-cont-1:/# hostname
my-cont-1
```
As can be seen, a new container with an ID is created which has new namespaces. By checking the directory `namespaces/<container-ID>/` the files related to these namespaces can be seen.

Now, lets exit this container and create a new container using called "my-cont-2" with a 10MB memory limitation:
```
$ sudo python3 CLI.py add my-cont-2 10
New container ID added to database.
Container successfully created with id: 88013473
Running scope as unit: run-r1a2282b20930490c9ba08c871c0b9608.scope
root@my-cont-2:/# ### running memory consuming app until it is killed
root@my-cont-2:/# python3 
Python 3.8.2 (default, Mar 13 2020, 10:14:16) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> x = []
>>> while (True):
...     x.append(1)
... 
Killed
root@my-cont-2:/# 
```

Actually, this part needs you to run the code yourself but if you do what I have done and run command `top` in another terminal (your terminal not container's) you can see that with this memory limitaion, the process is killed before it uses that much memory. But if you increase the memory or do not set a limit for it, it increases more than what it was able to reach before.

This was an example of how `add` command works with and without memory limitation.

### CLI list command
Using this command, you can list the pairs of `{ <container-id> : <hostname> }` for all of the created containers:
```
$ sudo python3 CLI.py list
```
If we run `list` command for the previous example, this would be our output:
```
$ sudo python3 CLI.py list
99546370  |  my-cont-1
88013473  |  my-cont-2
```

### CLI start command 
Using this command, you can start a previously created container using the `containes-id`. It is also worth mentioning that you can have the memory limitaion again or you can just continue without memory limitation ( even if you have use memory limitation in creating it):
```
$ sudo python3 CLI.py start <container-ID> <*memory>
```
Here is an example of restarting our container `my-cont-1`, setting `lo` interface to up, leaving the container and starting it again to check if our previous changes are still there or not:
```
$ sudo python3 CLI.py start 99546370
root@my-cont-1:/# ip addr
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
root@my-cont-1:/# hostname 
my-cont-1
root@my-cont-1:/# # we are in the first container again.
root@my-cont-1:/# # changing lo state       
root@my-cont-1:/# ip link set lo up
root@my-cont-1:/# ip link 
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
root@my-cont-1:/# exit 
exit
$ sudo python CLI.py start 99546370
root@my-cont-1:/# ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
root@my-cont-1:/# # the lo state is still up!
```
As can be seen, in these containers, the namespaces created are persistant and will not be destroyed after exiting the container.
So the question is if they are not destroyed by closing them, how should we delete a container which we don't want to use anymore? That is what `del` command does for us.

### CLI del command 
In order to delete an specific container with all it's belongings, we can simply run the following command:
```
$ sudo python3 CLI.py del <container-ID>
```
In order to conclude, lets do the final example and delete both containers `my-cont-1` and `my-cont-2`:
```
$ sudo python3 CLI.py del 99546370
Container ID removed from database.
$ sudo python3 CLI.py list
88013473  |  my-cont-2
$ sudo python3 CLI.py del 88013473
Container ID removed from database.
```

