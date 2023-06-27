import os
import shutil
import time
import random 

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from .custom_except import captcha_solved_except


#0 = new
#1 = downloaded
#2 = copy done
#
#
#
#
#7 = error while copying
#8 = error while downloading
#9 = fatal error
# Function to get all files in a folder and its subfolders
#Todo Main 
#Todo DockerVars 
#Todo TestLoop 
#Todo DockerArm -
#Todo Google login -> and maybe adblocker but why ?
#Todo testen 
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
        #Todo Test
        flac_files_name =  list(set([os.path.basename(path) for path in flac_files]))

        file_list_exist ,file_list_duplicat,file_list_new = [],[],[]


        for mp3_file in mp3_files:
            flac_file_name =  mp3_file[:-7].replace("/MP3/", "/FLAC/") + ".flac"

            if flac_file_name in flac_files:
                file_list_exist.append(mp3_file)
            elif os.path.basename(flac_file_name) in flac_files_name:
                file_list_duplicat.append(mp3_file)
            else:
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
        #Todo: testing
        print(run_test)
        try:
            if run_test is False:
                if len(file_list_duplicat) > 0 : self.copy_duplicate(file_list_duplicat)           
            
                if len(file_list_new) > 0 : self.download_flacs(download_flacer_list)
           
            else:
                #debug:
                path = os.getenv("BASE_PATH","/home/user/Musik/music")
                self.download_flacs([path+'/MP3/liked  (like)/Metallica - Fuel.mp3'],run_test)

        except captcha_solved_except:
            print("second Captcha found wait till next execution")
            #Todo test 
            exit(0)
        except:
            exit(1)
        return True
    
    def copy_duplicate(self, destinations,flac_files):
        #same song but different playlist -> dont neeed to download same Song twice 
        for destination in destinations:
            #Todo learn that loop 
            flac= os.path.basename(destination[:-7])+ ".flac"
            #destination_flac=    os.path.dirname(destination).replace("/MP3/","/FLAC/") + "/"+ flac
            source_path = [text for text in flac_files if flac in text]            
            self.copy_flac_file(destination,source_path[0])
    
    def copy_flac_file(self,dest,source=""):
        #
        dest_path = os.path.dirname(dest).replace('/MP3/','/FLAC/')
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            #self.copyOtherFiles(path,folder)
        flacs = source if len(source)> 1 else  self.get_all_files(self.temp_download)[0]
        dest_file_name = dest_path + "/" + os.path.basename(dest)[:-7] + ".flac"
        shutil.copy2(flacs,dest_file_name)
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
            return True
        except CouldntDecodeError:
            print("FLAC file is not valid or cannot be played.")
            return False
    


    def copy_check_flac(self,source,flac=""):
        self.flac_file = flac
        self.copy_flac_file(source,flac)
        self.flac_file = ""
   #need ?      ##time.sleep(random.randint(45,60))
    
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
        from .selenium_scraper import selenium_scraper
        
        scraper = self.selenium_scraper("/download","db")
       # scraper.login_google("URL: https://accounts.spotify.com/authorize?client_id=33bbbfe2ba9a486ebd39ff4db06c689d&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A9090&code_challenge_method=S256&code_challenge=injfBYkw9jRd8CBtKrWoagEC-Vr2mz-TVgHJKCBrpQ8&scope=+playlist-read-collaborative++playlist-read-private+user-library-read")
        scraper.check_browser()

    def download_flacs(self,file_paths,run_test=False):
        from .selenium_scraper import selenium_scraper
        import threading

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

                for i in range(0, 25):
                    flac_file = self.get_all_files(self.temp_download,ends_with=".flac")
                    if(len(flac_file) > 0) :break
                    time.sleep(2)
                    if i == 25: raise Exception
            #
            
            if run_test is False: 
                self.copy_check_flac(self,path,True)


        except:
            raise Exception
        return True

    # def get_flacs(self,file_paths,localrun=False):
    #     temp_path_Exception=""
    #     try:   #9222
    #         for paths in file_paths:
    #             temp_path_Exception= paths
    #             self.copy_check_flac(self,paths,True)
    #     except:
    #         self.rename_status(temp_path_Exception,"9")
    #         exit(1)
    #     exit(0)

    # def changePlaylist(self,src,type=".flac"): 
    #     with open(src, 'r') as f:
    #         content = f.read()
    #         # Replace .mp3 with .flac
    #         if type == ".flac":
    #             content = content.replace('.mp3', '.flac')
    #         else: 
    #             content = content.replace('.flac', '.mp3')
    #         # Write the updated content back to the file
    #     with open(src, 'w') as f:
    #         f.write(content)

    #def copyOtherFiles(self,src,dest):
      #  files = self.get_all_files(src,execlude=".mp3")
     #   for file in files:
       #     shutil.copy2(file,dest)
        #    filen_name = os.path.basename(file)
         #   if filen_name.ends_with(".m3u8"):
          #      self.changePlaylist(dest + filen_name)
if __name__ == "__main__":
    print("start")
    hi = Flacer()
    hi.main()