import os
import shutil
import time
import random 

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from .custom_except import captchaSolvedExcept

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
class Flaccer(object):
    def main(self):
        #Make Vars Maybe change that with DockerVars!
        self.captcha_solved= False
        self.base_path = os.getenv("BASE_PATH","/home/user/Musik/dir")
        print(self.base_path)
        self.mp3_folder =  self.base_path +"/MP3"
        self.flac_folder = self.base_path +"/FLAC"
        self.temp_download = self.base_path +"/TEMP"
        #'/home/user/Musik/dir/MP3/Test  (6jbF)/Vial - Mr. Fuck You'
        
        #get music files compare new/existing
        all_files = self.get_all_files(self.mp3_folder,     endsWith="-_0.mp3")
        all_flac_files = self.get_all_files(self.flac_folder,    endsWith=".flac")
        all_flac_ignore_playlist = self.get_all_files(self.flac_folder,    endsWith=".flac", fileNameOnly=True)
        file_list_exist ,file_list_duplicat,file_list_new = [],[],[]
        
        for mp3_file in all_files:
            flac_file_name =  mp3_file[:-7].replace("/MP3/", "/FLAC/") + ".flac"

            if flac_file_name in all_flac_files:
                file_list_exist.append(mp3_file)
            elif os.path.basename(flac_file_name) in all_flac_ignore_playlist:
                file_list_duplicat.append(mp3_file)
            else:
                file_list_new.append(mp3_file)
     
        #print("file_list_new:" +file_list_new)
        ##print("file_list_duplicat:" +file_list_duplicat)
        #print("file_list_exist:" +file_list_exist)
        #Todo: testing
        try:
            if len(file_list_duplicat) > 0 : self.copy_duplicate(file_list_duplicat,all_flac_files)           
            if len(file_list_new) > 0 : self.download_flacs(file_list_duplicat,all_flac_files)

        except captchaSolvedExcept:
            print("second Captcha found wait till next execution")
            exit(0)
        except:
            exit(1)
    
    def copy_duplicate(self, destinations,flacList):
        #same song but different playlist -> dont neeed to download same Song 
        for destination in destinations:
            #Todo learn that loop 
            flac= os.path.basename(destination[:-7])+ ".flac"
            #destination_flac=    os.path.dirname(destination).replace("/MP3/","/FLAC/") + "/"+ flac
            source_path = [text for text in flacList if flac in text]            
            self.copy_flac_file(destination,source_path[0])
    
    def copy_flac_file(self,dest,source=""):
        #
        destPath = os.path.dirname(dest).replace('/MP3/','/FLAC/')
        if not os.path.exists(destPath):
            os.makedirs(destPath)
            #self.copyOtherFiles(path,folder)
        flacs = source if len(source)> 1 else  self.get_all_files(self.temp_download)[0]
        destFilename = destPath + "/" + os.path.basename(dest)[:-7] + ".flac"
        shutil.copy2(flacs,destFilename)
        self.flacfile=destFilename


    def get_all_files(self,base_path, include="", execlude="", endsWith="", fileNameOnly=False):
        allFiles = []
        for dirpath, dirnames, filenames in os.walk(base_path):
            for filename in filenames:
                if fileNameOnly is False:
                    allFiles.append(os.path.join(dirpath, filename))
                else:
                    allFiles.append(filename)


        filtertFiles = allFiles 
        #wenn filter gesetzt sind 
        if len(endsWith) > 1:
            filtertFiles = [txt for txt in allFiles if txt.endswith(endsWith) ]       
        if len(include) > 1:
            filtertFiles = [txt for txt in allFiles if include in txt  ]
        if len(execlude) > 1:
            filtertFiles = [txt for txt in allFiles if execlude not in txt]
        allFiles = filtertFiles
        return allFiles


    def rename_status(self,file_path,status):
            pathSplt = os.path.splitext(os.path.basename(file_path))
            filename, extension = pathSplt[0],pathSplt[1]
            new_file_path = os.path.join(os.path.dirname(file_path), filename+ status + extension)
            os.rename(file_path, new_file_path)
            return True
    

    def check_flac(self,path):
        try:
            audio = AudioSegment.from_file(path, format="flac")
            return True
        except CouldntDecodeError:
            print("FLAC file is not valid or cannot be played.")
            return False
    


    from .SeleniumScraper import SeleniumScraper
    def download_flacs(self,file_paths):
        path = ""
        try:   #9222
            fetcher = self.SeleniumScraper(self.temp_download,"db")
            random.shuffle(file_paths) # so the loop should not be stuck
            for path in file_paths:
                #clear downloads
                self.remove_folder_contents(self.temp_download)
                status = "1" if fetcher.download_flac(os.path.basename(path),self.temp_download) else "8"
                self.rename_status(path,status)

                if status > "5" : return  
                for i in range(0, 25):
                    flacFile = self.get_all_files(self.temp_download,endsWith=".flac")
                    if(len(flacFile) > 0) :break
                    time.sleep(2)
                    if i == 25: raise Exception
            #
            self.copy_check_flac(self,path,True)

        except  captchaSolvedExcept:
            raise captchaSolvedExcept
        except:
           # self.rename_status(path,"9")
            exit(1)
        exit(0)

    def copy_check_flac(self,source,flac="",updStatus=False):
        self.flacfile = flac
        status = "2" if self.copy_flac_file(source,flac) else "7"
        if updStatus: self.rename_status(source,status)
        status = "3" if self.check_flac(self.flacfile) else "7"
        if updStatus: 
            self.rename_status(source,status)
            self.flacfile = ""
            time.sleep(random.randint(45,60))
        elif status =="7":
            self.rename_status(self.flacfile,status)
        self.rename_status(source,"9")
    
    def remove_folder_contents(self,base_path):
        if not os.path.exists(base_path):
            print(f"Error: {base_path} does not exist")
            os.mkdir(base_path)
            return
        try:
            shutil.rmtree(base_path)
            os.mkdir(base_path)
        except Exception as e:
            print(f"Error deleting files in {base_path}: {e}")

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
        #    filename = os.path.basename(file)
         #   if filename.endswith(".m3u8"):
          #      self.changePlaylist(dest + filename)
if __name__ == "__main__":
    print("start")
    hi = Flaccer()
    hi.main()