import os
import shutil
import time
import random 

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from .custom_except import captcha_solved_except
import threading

#Todo captcha multiple times handler
class Flacer(object):
    def main(self,run_test=False):
        #Make Vars Maybe change that with DockerVars!
        print("run test:" + str(run_test))
        self.captcha_solved= False
        self.base_path = os.getenv("BASE_PATH","/home/user/Musik/music")
        print(self.base_path)
        self.mp3_folder =  os.path.join(self.base_path , "MP3")
        self.flac_folder = os.path.join(self.base_path ,"FLAC")
        self.temp_download = os.path.join(self.base_path ,"TEMP")
        #'/home/user/Musik/music/MP3/Test  (6jbF)/Vial - Mr. Fuck You'        
        #get music files compare new/existing
        mp3_files = self.get_all_files(self.mp3_folder,ends_with=".mp3")
        flac_files = self.get_all_files(self.flac_folder,    ends_with=".flac")
        #all_flac_ignore_playlist = self.get_all_files(self.flac_folder,    ends_with=".flac", file_name_only=True)
        all_flac_ignore_playlist = self.get_all_files(self.flac_folder,    ends_with=".flac", file_name_only=True)
       
        #list set -> remove duplicate
        flac_files_name =  list(set([os.path.basename(path) for path in flac_files]))
        file_list_exist ,file_list_duplicat,file_list_new,file_name_duplicate_check = [],[],[],[]
        for mp3_file in mp3_files:
            flac_file_name =  mp3_file[:-7].replace("/MP3/", "/FLAC/") + ".flac"
            file_name_only = os.path.basename(flac_file_name)

            #already done
            if flac_file_name in flac_files:
                file_list_exist.append(mp3_file)
            #duplicate copy is enough 
            elif file_name_only in flac_files_name:
                file_list_duplicat.append(mp3_file)
            #if file is not already in list add it if is in list the duplicate will handle it next time
            elif file_name_only not in file_name_duplicate_check:             
                file_name_duplicate_check.append(file_name_only)
                file_list_new.append(mp3_file)
        # may remove 
        with open(self.mp3_folder + "/flacer_list.txt", "r") as file:
            liste = file.read()
        
        # for now on only download list in filelist #Todo find better solution
        # get include list
        folder_list = [f'/{folder.strip()}/' for folder in liste.split(',')]   
        # remove all whats not in include list 
        download_flacer_list  = [path for path in file_list_new if any(folder in path for folder in folder_list)]

        #print("file_list_new:" +file_list_new)
        ##print("file_list_duplicat:" +file_list_duplicat)
        #print("file_list_exist:" +file_list_exist)
        print(run_test)
        try:
            if run_test is False:
                if len(file_list_duplicat) > 0 : self.copy_duplicate(file_list_duplicat,flac_files) #          
            
                if len(file_list_new) > 0 : self.download_flacs(download_flacer_list)
           
            else:
                #debug:
                path = os.getenv("BASE_PATH","/home/user/Musik/music")
                print(path+'/MP3/liked  (like)/Metallica - Fuel.mp3')
                self.download_flacs([path+'/MP3/liked  (like)/Metallica - Fuel.mp3'],run_test)

        except captcha_solved_except:
            print("second Captcha found wait till next execution")
        except:
            return False
        return True
    
    def copy_duplicate(self, destinations,flac_files):
        #same song but different playlist -> dont neeed to download same Song twice 
        for destination in destinations:
            #Todo learn that loop 
            flac= os.path.basename(destination[:-7])+ ".flac"
            #destination_flac=    os.path.dirname(destination).replace("/MP3/","/FLAC/") + "/"+ flac
            source_path = [flacs for flacs in flac_files if flac in flacs]            
            self.copy_flac_file(destination,source_path[0])
    
    def copy_flac_file(self,dest,source=""):
        #
        dest_path = os.path.dirname(dest).replace('/MP3/','/FLAC/')
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            #self.copyOtherFiles(path,folder)
        # if source is not give check donwload folder - so it can handle duplicate files! 
        flacs = source if len(source)> 1 else  self.get_all_files(self.temp_download)[0] 
        dest_file_name = dest_path + "/" + os.path.basename(dest)[:-7] + ".flac"
        print("copy_flac_file -> start copy")
        if self.check_flac(flacs) is True:
            shutil.copy2(flacs,dest_file_name)
            print("copy_flac_file -> finished copy")
        self.flac_file=dest_file_name

    def get_all_files(self,path, include="", execlude="", ends_with="", starts_with="",file_name_only=False):
        # get files from folder . optional with  filter
        all_files = []
        for dir_path, dir_names, filen_names in os.walk(path):
            for filen_name in filen_names:
                if file_name_only is False:
                    all_files.append(os.path.join(dir_path, filen_name))
                else:
                    all_files.append(filen_name)

        filtert_files = all_files 
        #wenn filter gesetzt sind 
        if len(ends_with) > 1:
            filtert_files = [txt for txt in all_files if txt.endswith(ends_with) ]       
        if len(include) > 1:
            filtert_files = [txt for txt in all_files if include in txt  ]
        if len(execlude) > 1:
            filtert_files = [txt for txt in all_files if execlude not in txt]
        all_files = filtert_files
        return all_files

    def rename_status(self,file_path):
            path_split = os.path.splitext(os.path.basename(file_path))
            filen_name, extension = path_split[0],path_split[1]
            new_file_path = os.path.join(os.path.dirname(file_path), filen_name+ extension)
            os.rename(file_path, new_file_path)
            return True
    

    def check_flac(self,path):
        try:
            audio = AudioSegment.from_file(path, format="flac")
            print(path + " is valid" )
            return True
        except CouldntDecodeError:
            print(path + " FLAC file is not valid or cannot be played.")
            return False
    
    def remove_folder_contents(self,path):
        if not os.path.exists(path):
            print(f"Error: {path} does not exist")
            os.mkdir(path)
            return
        try:
            shutil.rmtree(path)
            os.mkdir(path)
        except Exception as e:
            print(f"Error deleting files in {path}: {e}")
            
    from .selenium_scraper import selenium_scraper

    def build(self):
        scraper = self.selenium_scraper("/download","db")
        scraper.login_google()

    def test(self):
        scraper = self.selenium_scraper("/download","db")
       # scraper.login_google("URL: https://accounts.spotify.com/authorize?client_id=33bbbfe2ba9a486ebd39ff4db06c689d&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A9090&code_challenge_method=S256&code_challenge=injfBYkw9jRd8CBtKrWoagEC-Vr2mz-TVgHJKCBrpQ8&scope=+playlist-read-collaborative++playlist-read-private+user-library-read")
        scraper.check_browser()

    def download_flacs(self,file_paths,run_test=False):

        path = ""
        try:   #9222
            scraper = self.selenium_scraper(self.temp_download,"db")
            # solve captcha -> try again -> if new captcha Wait x Seconds  
            scraper.captcha_solved = False                        
            random.shuffle(file_paths) # so the loop should not be stuck
            self.counter = 0
            for path in file_paths:
                #clear downloads
                self.remove_folder_contents(self.temp_download)
                try:
                    scraper.download_flac(os.path.basename(path),self.temp_download) 
                except  captcha_solved_except:
                    self.counter += 1
                    time.sleep(random.randint(153, 255))
                    if self.counter <=2: 
                        continue
                    else:
                        del self.counter
                        raise Exception
                print("flacer -> try to copy file")
                for i in range(0, 25):
                    flac_file = self.get_all_files(self.temp_download,ends_with=".flac")
                    if len(flac_file) > 0 :
                        break
                    time.sleep(2)
                    if i == 25: raise Exception
            #
            
                if run_test is False: 
                    print("flacer -> copy file")
                    self.flac_file = path
                    self.copy_flac_file(path,flac_file[0])
                    self.flac_file = ""


        except:
            raise Exception
        return True
if __name__ == "__main__":
    print("start")
    hi = Flacer()
    hi.main()