from  .upload_to_drive import main as main_syncer 
import os 
class Syncer():
#better than os change path shit
    
    def main():
        main_syncer()


    def check_for_new_files():
        previous_state = set()
        file_list_path = os.getenv("BASE_PATH","/home/user/Musik/dir") + "/file_list.txt"
        
        if os.path.exists(file_list_path):
            with open(file_list_path, 'r') as file:
                previous_state.update(file.read().splitlines())

        current_state = set(os.listdir(os.getenv("BASE_PATH","/home/user/Musik/dir")))
        new_files = current_state - previous_state

        if new_files:
            print("New files detected:", new_files)
            main_syncer()

        with open(file_list_path, 'w') as file:
            file.write('\n'.join(current_state))

if __name__ == '__main__':
    Syncer.main()
