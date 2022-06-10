# This is for the case which you do not have the ubuntu 20.04 filesystem. If you have the filesystem just create a directory 
# called "rootfs" and copy it to this dir. Otherwise, run this code.
mkdir rootfs
apt instll debootstrap
debootstrap focal ./rootfs

