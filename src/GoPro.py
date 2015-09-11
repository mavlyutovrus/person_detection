from goprohero import GoProHero
import base64
import time
import os.path

def save_em():
   import os
   import glob
   import shutil

   src_dir = "C:/FaceRecognition/"
   dst_dir = "C:/FaceRecognition/GoPro/"
   for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
    shutil.copy(jpgfile, dst_dir)

def list_all_camera_images():
   import urllib2
   import re
   folder_url = "http://10.5.5.9:8080/videos/DCIM/100GOPRO/"
   html = urllib2.urlopen(folder_url).read().replace("\n", " ")
   jpeg_files = [(fname,date) for fname, date in \
      re.findall("""<a class="link" href="([a-zA-Z0-9]+\.JPG)".+?<span class="date">([^<]+)</span>""", html)]
   return jpeg_files

def upload_image(fname):
   folder_url = "http://10.5.5.9:8080/videos/DCIM/100GOPRO/"
   import urllib2
   image = urllib2.urlopen(folder_url + fname).read()
   return image

def get_timestamp() :
    import time
    import datetime
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%H-%S')
    timestamp = str(st)
    return timestamp

tester = 1
int(tester)

while tester <= 5 :



   already_on_camera = set(list_all_camera_images())

   camera = GoProHero(password='qwertyuiop')
   #camera.command("picres", "12MP wide")
   camera.command('record', 'on')


   time.sleep(3)
   new_images = set(list_all_camera_images()) - already_on_camera
   print new_images
   for image_fname, image_date in new_images:
      image = upload_image(image_fname)
      out = open("C:/FaceRecognition/GoPro/" + "snapshot" + get_timestamp() + ".jpg", "wb")
      out.write(image)
      out.close()
   print "done"

   tester = tester + 1

save_em()
