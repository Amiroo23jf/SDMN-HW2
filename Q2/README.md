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
