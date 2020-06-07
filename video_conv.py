import cv2
import numpy as n
import glob
import os
from datetime import datetime
import re
import sys
import time
import threading
import pysurveillance_conf as conf


def find_days():
    dl=glob.glob("%s/????-??-??"%(conf.data_dir))
    dl.sort()
    return(dl)

def create_html():
    while True:
        print("creating html file")
        fl=glob.glob("%s/????-??-??/????-??-??.mp4"%(conf.data_dir))
        fl.sort()
        dfl=glob.glob("%s/????-??-??/det*.jpg"%(conf.data_dir))
        dfl.sort()
        dfl=dfl[::-1]
        html_str=""

        for df in dfl[0:20]:
            print(df)
            html_str += "<img src=\"%s\"></br>\n"%(df)
        
        for f in fl:
            date_str = re.search(".*(....-..-..).mp4",f).group(1)
            html_str += "<a href=\"%s\"> [%s] </a>\n"%(f,date_str)
        fo=open("%s/index.html"%(conf.data_dir),"w")
        fi=open("index.html_template","r")
        for l in fi.readlines():
            fo.write(l)
        fo.write(html_str)
        fo.write("</body></html>\n")
        fo.close()
        time.sleep(5)
    return(html_str)


def create_day_file(dir_name,ofname="out.mp4"):
    if  conf.show_labels:
        cmd="ffmpeg -framerate 2 -y -pattern_type glob -i \"%s/label*.jpg\" -c:v libx264 %s"%(dir_name,ofname)        
    else:
        cmd="ffmpeg -framerate 2 -y -pattern_type glob -i \"%s/det*.jpg\" -c:v libx264 %s"%(dir_name,ofname)

        
        
    print(cmd)
    os.system(cmd)

def create_animations():
    while True:
        # figure out how the files are organized.
        # we're going to create a video for each day
        dirs=find_days()
        n_dirs=len(dirs)
        for di,d in enumerate(dirs):
            print(d)
            day=re.search(".*/(....-..-..)",d).group(1)
            video_name="%s/%s.mp4"%(d,day)
            if os.path.exists(video_name) and di != (n_dirs-1):
                # if old directory, and file already exists
                print("video %s exists already"%(video_name))
            else:
                # current day. always make video
                create_day_file(d,ofname=video_name)
                os.system("cp %s %s/latest.mp4"%(video_name,conf.data_dir))
        time.sleep(5)

if __name__ == "__main__":
    html_thread=threading.Thread(target=create_html)
    html_thread.daemon=True
    anim_thread=threading.Thread(target=create_animations)
    html_thread.start()
    anim_thread.start()
    
#    create_html()
#    create_animations()
 #   time.sleep(5)
