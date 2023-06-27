from  upload_to_drive import main as main_syncer 
import os 


class Syncer():
#better than os change path shit
    
    def main_pfusch():
        main_syncer()


    def check_for_new_files(update_google_drive=True):
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

        if new_files:
            # Run your desired function here
            print("New files detected:", new_files)
            main_syncer()

        with open(file_list, 'w') as file:
            file.write('\n'.join(current_state))

if __name__ == '__main__':
    while True:
        Syncer.check_for_new_files()
