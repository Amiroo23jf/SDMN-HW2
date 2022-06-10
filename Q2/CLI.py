from cmath import exp
from genericpath import isdir
import os
import sys
import json
import random

def CLI():
    arg_num = len(sys.argv) - 1
    if (arg_num < 1 or arg_num > 3):
        print("Invalid Arguments")
    else:
        if (os.path.isdir("./containers") == False):
            print("Creating the containers directory...")
            try:
                os.mkdir("./containers")
            except:
                print("Creating the containers directory failed...")
                return
            print("Containers directory is created.")
        if (os.path.isdir("./namespaces") == False):
            # The namespace directory stores the namespaces of the created containers
            print("Creating the namespaces directory...")
            try:
                os.mkdir("./namespaces")
            except:
                print("Creating the namespace directory failed...")
                return
            print("Namespace directory is created.")
        if (os.path.isfile("containers_db.json") == False):
            print("Creating database...")
            with open('containers_db.json', 'w', encoding='utf-8') as db:
                json.dump({}, db)
            print("Database created.")
        
        # commands {list, add, start, del}
        if (arg_num == 1 and sys.argv[1] == "list"):
            with open('containers_db.json', 'r', encoding='utf-8') as db:
                db_json = json.loads(db.read())
                for id in db_json.keys():
                    print(str(id) + "  |  " + str(db_json[id]))
        elif (sys.argv[1] == "add"):
            # creating container's ID
            with open('containers_db.json', 'r', encoding='utf-8') as db:
                db_json = json.loads(db.read())
                cont_id = create_random_id(db_json)
            if (arg_num == 1):
                print("add requires at least 1 argument")
                return 
            elif (arg_num == 2):
                cont_hostname = sys.argv[2]
                has_mem = False
            else:
                cont_hostname = sys.argv[2]
                cont_mem = sys.argv[3]
                has_mem = True
            
            # copying the filesystem
            cont_path = "./containers/" + str(cont_id)
            ns_path = "./namespaces/" + str(cont_id)
            netns_path = "./namespaces/"+str(cont_id)+"/net"
            mntns_path = "./namespaces/"+str(cont_id)+"/mnt"
            utsns_path = "./namespaces/"+str(cont_id)+"/uts"
            usrns_path = "./namespaces/"+str(cont_id)+"/usr"
            cwd_path = os.getcwd()

            os.system("cp -r rootfs " + cont_path)

            # creating namespaces dir and files
            os.system("mkdir -p ./namespaces/"+str(cont_id))

            ## mounting the whole namespace path and making it private in order to
            ## make unshare able to mount the given mnt namespace
            os.system("mount --bind " + ns_path + " " + ns_path)
            os.system("mount --make-private " + ns_path)

            os.system("touch " + netns_path) # net namespace
            os.system("touch " + mntns_path) # mnt namespace
            os.system("touch " + utsns_path) # uts namespace
            os.system("touch " + usrns_path) # usr namespace
            

            # mounting /proc and making it private
            os.system("mount --bind " + cont_path + "/proc " + cont_path + "/proc")
            os.system("mount --make-private " + cont_path + "/proc") 
            db_json[str(cont_id)] = cont_hostname
            with open('containers_db.json', 'w', encoding='utf-8') as db:
                json.dump(db_json, db)
                print("New container ID added to database.")

            
            # creating the container and its namespaces
            # creating the container and changing the hostname
            os.system('unshare -pfr --user=' + usrns_path +' --uts='+utsns_path+' --net='+netns_path + ' --mount='+mntns_path +
            ' hostname '+cont_hostname)
            #+ ' && mount -t proc proc ' + cont_path + '/proc'

            print("Container successfully created with id: "+str(cont_id))

            if (has_mem):
                # running bash
                os.system('systemd-run --scope -p MemoryLimit='+ cont_mem +'M nsenter --user=' + usrns_path +  ' --uts='+ utsns_path +' --net='+ netns_path + ' --mount='+ mntns_path + 
                ' unshare -pf chroot ' + cwd_path + '/containers/' + str(cont_id) + ' bash -c "mount -t proc proc /proc && bash"')

            else:
                # running bash
                os.system('nsenter --user=' + usrns_path +  ' --uts='+ utsns_path +' --net='+ netns_path + ' --mount='+ mntns_path + 
                ' unshare -pf chroot ' + cwd_path + '/containers/' + str(cont_id) + ' bash -c "mount -t proc proc /proc && bash"')
                

        elif (sys.argv[1] == "start"):
            with open('containers_db.json', 'r', encoding='utf-8') as db:
                db_json = json.loads(db.read())
            
            if (arg_num == 1):
                print("add requires at least 1 argument")
                return 
            elif (arg_num == 2):
                cont_id = sys.argv[2]
                has_mem = False
            else:
                cont_id = sys.argv[2]
                cont_mem = sys.argv[3]
                has_mem = True

            if (cont_id not in db_json):
                print("Container doesn't exist!")
                return 
            cont_hostname = db_json[cont_id]

            cont_path = "./containers/" + str(cont_id)
            ns_path = "./namespaces/" + str(cont_id)
            netns_path = "./namespaces/"+str(cont_id)+"/net"
            mntns_path = "./namespaces/"+str(cont_id)+"/mnt"
            utsns_path = "./namespaces/"+str(cont_id)+"/uts"
            usrns_path = "./namespaces/"+str(cont_id)+"/usr"
            cwd_path = os.getcwd()

            if (has_mem):
                # running bash
                os.system('systemd-run --scope -p MemoryLimit='+ cont_mem +'M nsenter --user=' + usrns_path +  ' --uts='+ utsns_path +' --net='+ netns_path + ' --mount='+ mntns_path + 
                ' unshare -pf chroot ' + cwd_path + '/containers/' + str(cont_id) + ' bash -c "mount -t proc proc /proc && bash"')

            else:
                # running bash
                os.system('nsenter --user=' + usrns_path +  ' --uts='+ utsns_path +' --net='+ netns_path + ' --mount='+ mntns_path + 
                ' unshare -pf chroot ' + cwd_path + '/containers/' + str(cont_id) + ' bash -c "mount -t proc proc /proc && bash"')
            

            

        elif (sys.argv[1] == "del"):
            # creating container's ID
            with open('containers_db.json', 'r', encoding='utf-8') as db:
                db_json = json.loads(db.read())
            if (arg_num == 1 or arg_num == 3):
                print("del requires exactly 1 argument")
                return
            else:
                cont_id = sys.argv[2]
                if cont_id not in db_json.keys():
                    print("The container with the given ID doesn't exist!")
                    return
                cont_path = "./containers/" + cont_id
                ns_path = "./namespaces/" + cont_id

                if (os.path.isdir(cont_path)):
                    # unmounting /proc
                    os.system("umount " + cont_path + "/proc")
                    # unmounting namespaces dir
                    os.system("umount ./namespaces/" + cont_id + "/*")
                    os.system("umount ./namespaces/" + cont_id )

                    # deleting the filesystem and namespaces
                    os.system("rm -r " + cont_path)
                    os.system("rm -r " + ns_path)

                
                # removing ID-Hostname pair from database
                db_json.pop(cont_id)
                with open('containers_db.json', 'w', encoding='utf-8') as db:
                    json.dump(db_json, db)
                    print("Container ID removed from database.")
        

        else: 
            print("Unsupported Command!")



                            

def create_random_id(db_json):
    '''Creates a random id which is not already in the database'''
    unique = False
    while (unique == False):
        new_id = random.randint(10000000, 99999999)
        if str(new_id) not in db_json.keys():
            unique = True
    return new_id
if __name__ == "__main__":
    CLI()