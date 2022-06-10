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

After running the CLI for the first time using any command, the containers and namespaces directories and containers_db.json file. Now lets get deeper and find out what is the purpose of each of these files and dirs.
- **containers_db.json:** This file, is a json file containing the pairs of container ID's which is unique for each container and their equivalent hostname (not necessarily unique).
- **containers:** This directory, contains the filesystem of the created containers. This means that everytime a container is created, a directory with the ID of the container as its name is created and the whole filesystem is copied to it (from rootfs).
- **namespaces:** For the sake of persistency and in order to be able to continue using a container from its previous state after closing it, this directory saves the namespaces of each container in a different directory named the ID of each container.

So now lets move on from the architecture and see how to actuallty use the CLI in order to create and use it properly. Overall, the CLI has 4 command:
1. add <hostname> <*memory>: This command is for adding new containers, the memory argument can be ignored if you do not want any limitation.
2. start <container ID> <*memory>: By using this command you can start an already added container using it's container ID.
3. del <container ID>: Using this command, you can delete a container and everything file and directory related to it.
4. list: this command lists the { <container ID> : <hostname> } pairs of all added containers (excluding deleted ones)

In the next sections, each of these commands are explained in depth with an example.

