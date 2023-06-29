from  .upload_to_drive import main as upload_syncer 
import os 
    

class Syncer():
#better than os change path shit
    syncer_run = False
    def main_syncer(check_file_changed=True):
        global syncer_run
        if syncer_run is False:
            syncer_run  = True  
            file_changed = True
            try:
                print("start uploud syncer")
                if check_file_changed is True: file_changed = upload_syncer()
                if file_changed is True: 
                    upload_syncer()
            except Exception as e:
                print("Error occurred:", e)
                print("flaccer error")
        syncer_run = False

    def check_for_new_files():
        previous_state = set()
        file_list = os.getenv("BASE_PATH","/home/user/Musik/music") + "/file_list.txt"
        file_list_path = os.getenv("BASE_PATH","/home/user/Musik/music")
        
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
    while True:
        Syncer.check_for_new_files()
