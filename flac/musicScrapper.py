import os
import subprocess
import shutil
from custom_except import captchaSolvedExcept
import time
import random 
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
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
class Flaccer(object):
    def main(self):
        self.captchaSolved= False
        self.folder_path = "/home/user/Musik/dir"
        self.mp3_path =  self.folder_path +"/MP3"
        self.FLAC_path = self.folder_path +"/FLAC"
        self.temp_download = self.folder_path +"/TEMP"
        self.flacfile = ""
#'/home/user/Musik/dir/MP3/Test  (6jbF)/Vial - Mr. Fuck You'
        all_files = self.get_all_files(self.mp3_path,endsWith="-_0.mp3")
        all_flacfiles = self.get_all_files(self.FLAC_path,endsWith=".flac")
        filtered_list_a = [mp3 for mp3 in all_files if mp3[:-7].replace("/MP3/", "/FLAC/")  in [flac[:-5] for flac in all_flacfiles]]
        #filtered_list_local = [mp3 for mp3 in filtered_list_a if os.path.basename(mp3[:-7])  in [os.path.basename(flac[:-5]) for flac in all_flacfiles]]
        filtered_list_local = [(mp3, flac[:-5]) for mp3 in filtered_list_a for flac in all_flacfiles if os.path.basename(mp3[:-7]) == os.path.basename(flac[:-5])]
        print(filtered_list_local)
        try:
            self.getLocalFlacs(all_files,True)
            self.getFlacs(all_files)
        except captchaSolvedExcept:
            print("second Captcha found wait till next execution")
            exit(0)
        except:
            exit(1)

    def copyFlac(self,source,flacPath=""):
        destPath = os.path.dirname(source).replace('/MP3/','/FLAC/')
        if not os.path.exists(destPath):
            os.makedirs(destPath)
            #self.copyOtherFiles(path,folder)
        flacs = flacPath if len(flacPath)> 1 else  self.get_all_files(self.temp_download)[0]
        destFilename = destPath + "/" + os.path.basename(source)[:-7] + ".flac"
        shutil.copy2(flacs,destFilename)
        self.flacfile=destFilename

    #def copyOtherFiles(self,src,dest):
      #  files = self.get_all_files(src,execlude=".mp3")
     #   for file in files:
       #     shutil.copy2(file,dest)
        #    filename = os.path.basename(file)
         #   if filename.endswith(".m3u8"):
          #      self.changePlaylist(dest + filename)
    
    def changePlaylist(self,src,type=".flac"): 
        with open(src, 'r') as f:
            content = f.read()
            # Replace .mp3 with .flac
            if type == ".flac":
                content = content.replace('.mp3', '.flac')
            else: 
                content = content.replace('.flac', '.mp3')
            # Write the updated content back to the file
        with open(src, 'w') as f:
            f.write(content)

    def get_all_files(self,folder_path, include="", execlude="", endsWith=""):
        allFiles = []
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                allFiles.append(os.path.join(dirpath, filename))
        filtertFiles = allFiles 
        if len(endsWith) > 1:
            filtertFiles = [txt for txt in allFiles if txt.endswith(endsWith) ]       
        if len(include) > 1:
            filtertFiles = [txt for txt in allFiles if include in txt  ]
        if len(execlude) > 1:
            filtertFiles = [txt for txt in allFiles if execlude not in txt]
        allFiles = filtertFiles
        return allFiles


    def renameStatus(self,file_path,status):
            pathSplt = os.path.splitext(os.path.basename(file_path))
            filename, extension = pathSplt[0],pathSplt[1]
            new_file_path = os.path.join(os.path.dirname(file_path), filename+ status + extension)
            os.rename(file_path, new_file_path)
            return True
    

    def checkFlac(self,path):

        try:
            audio = AudioSegment.from_file(path, format="flac")
            return True
        except CouldntDecodeError:
            print("FLAC file is not valid or cannot be played.")
            return False
    def getFlacs(self,file_paths,localrun=False):
        try:   #9222
            for paths in file_paths:
                self.copyandCheckFlac(self,paths,True)
        except:
            self.renameStatus(path,"9")
            exit(1)
        exit(0)

    from SeleniumScraper import SeleniumScraper
    def getFlacs(self,file_paths):
        path = ""
        try:   #9222
            fetcher = self.SeleniumScraper(self.temp_download,"db")
            fetcher.open_Chrome("https://free-mp3-download.net/" ,downloadDir=self.temp_download,timer=7)  
            random.shuffle(file_paths) # so the loop should not be stuck
            for path in file_paths:
                fetcher.getWaitUrl("https://free-mp3-download.net/")
                self.remove_folder_contents(self.temp_download)
                folder_path = 'mp3s'
                status = "1" if fetcher.downloadFlac(os.path.basename(path)) else "8"
                self.renameStatus(path,status)
                if status > "5" : return  
                for i in range(0, 25):
                    flacFile = self.get_all_files(self.temp_download,endsWith=".flac")
                    if(len(flacFile) > 0) :break
                    time.sleep(2)
                    if i == 25: raise Exception
            self.copyandCheckFlac(self,path,True)

        except  captchaSolvedExcept:
            raise captchaSolvedExcept
        except:
            self.renameStatus(path,"9")
            exit(1)
        exit(0)

    def copyandCheckFlac(self,source,flac="",updStatus=False):
        self.flacfile = flac
        status = "2" if self.copyFlac(source,flac) else "7"
        if updStatus: self.renameStatus(source,status)
        status = "3" if self.checkFlac(self.flacfile) else "7"
        if updStatus: 
            self.renameStatus(source,status)
            self.flacfile = ""
            time.sleep(random.randint(45,60))
        elif status =="7":
            self.renameStatus(self.flacfile,status)

        self.renameStatus(source,"9")
    def remove_folder_contents(self,folder_path):
        if not os.path.exists(folder_path):
            print(f"Error: {folder_path} does not exist")
            os.mkdir(folder_path)
            return
        try:
            shutil.rmtree(folder_path)
            os.mkdir(folder_path)
        except Exception as e:
            print(f"Error deleting files in {folder_path}: {e}")


if __name__ == "__main__":
    print("start")
    hi = Flaccer()
    hi.main()