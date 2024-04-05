import os
from shutil import copyfile
import subprocess
import signal
import requests, json
import platform

def install_ttyd():
    #SafePath = self.file_system.path

    url = requests.get("https://api.github.com/repos/tsl0922/ttyd/releases/latest")
    text = url.text
    data = json.loads(text)
    assets = data["assets"]
    pf = platform.machine()
    #if pf == 'arm71':
    #    pf = 'armhf'
    #if pf == 'aarch64':
    #    pf = 'arm64'
    #if pf == 'x86_64':
    #    pf = 'x64'
    print(pf)
    for asset in assets:
        if pf in asset["name"]: 
            print(asset["name"])
            #filename = SafePath + '/ttyd.' + asset["name"]
            filename= '/home/ovos/.local/share/mycroft/filesystem/skills/ovos-skill-web-terminal.andlo/ttyd'
            r = requests.get(asset["browser_download_url"])
            f = open(filename, "wb")
            f.write(r.content)
            f.close
            os.chmod(filename,0o777)
            #f = tarfile.open(filename)
            #f.extractall(SafePath)
            #f.close()
            
            #olddir = filename
            #newdir = SafePath + '/' + 'ttyd'
            #os.rename(olddir, newdir)
            #os.remove(filename)


install_ttyd()
