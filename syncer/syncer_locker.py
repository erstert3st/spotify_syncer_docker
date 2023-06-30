from tendo import singleton
import os
import subprocess

def main_syncer(force=False):
        file_changed = False
        try:
            print("start  syncer")
            if force is False: 
                file_changed = check_for_new_files()  
                          
            if force is True or file_changed is True: 
                print("file changed start upload:")
                path = os.getenv("BASE_PATH","") + "/file_list.txt"
                if len(path) <=15:
                    print("BASE_PATH should be not ''")
                    raise Exception
                command = "rclone sync "+ os.getenv("BASE_PATH") +" drive:music"
                print(command)
                #process = subprocess.Popen(command, shell=True)
                #process.wait()
        except Exception as e:
            print("Error occurred:", e)

def check_for_new_files():
    previous_state = set()
    file_list_path = os.getenv("BASE_PATH","/home/user/Musik/music") 
    file_list = file_list_path + "/file_list.txt"
    
    if os.path.exists(file_list):
        with open(file_list, 'r') as file:
            previous_state.update(file.read().splitlines())

    current_state = set()
    for root, dirs, files in os.walk(file_list_path):
        for file in files:
            current_state.add(os.path.join(root, file))

    new_files = current_state - previous_state

    with open(file_list, 'w') as file:
        file.write('\n'.join(current_state))
    if new_files:
        # Run your desired function here
        print("New files detected:", new_files)
        return True
    return False



if __name__ == '__main__':
    try:
        me = singleton.SingleInstance()
        main_syncer()
    except:
        print("Already running")
        exit(0)

