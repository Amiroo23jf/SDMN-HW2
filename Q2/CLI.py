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
        if (arg_num == 1 and sys.argv[1] == "list"):
            with open('containers_db.json', 'r', encoding='utf-8') as db:
                db_json = json.loads(db.read())
                for id in db_json.keys():
                    print(str(id) + "  |  " + str(db_json[id]))
        if (sys.argv[1] == "add"):
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
            os.system("cp -r rootfs " + cont_path)

            # mounting /proc and making it private
            os.system("mount --bind " + cont_path + "/proc " + cont_path + "/proc")
            os.system("mount --make-private " + cont_path + "/proc") 
            db_json[str(cont_id)] = cont_hostname
            with open('containers_db.json', 'w', encoding='utf-8') as db:
                json.dump(db_json, db)
                print("New container ID added to database.")

            
            # creating the container and its namespaces
            if (has_mem == False):
                os.system('unshare -Umnpruf --mount-proc='+cont_path+'/proc chroot '+cont_path+' /bin/bash -c "hostname '+cont_path+'; /bin/bash')

            

        if (sys.argv[1] == "del"):
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

                if (os.path.isdir(cont_path)):
                     # unmounting /proc
                    os.system("umount " + cont_path + "/proc")

                    # deleting the filesystem
                    os.system("rm -r " + cont_path)
                
                # removing ID-Hostname pair from database
                db_json.pop(cont_id)
                with open('containers_db.json', 'w', encoding='utf-8') as db:
                    json.dump(db_json, db)
                    print("Container ID removed from database.")



                            

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