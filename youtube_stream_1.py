#!/usr/bin/env python 
import os 
import time 
import io
import picamera 
import subprocess


YOUTUBE="rtmp://a.rtmp.youtube.com/live2/"		 
KEY= "abdq-sv6g-5a1m-2d72"

#stream_cmd = 'ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer -f alsa -ac 1 -i hw:1,0 -vcodec copy -acodec aac -ac 1 -ar 8000 -ab 32k -map 0:0 -map 1:0 -strict experimental -f flv ' + YOUTUBE + KEY
#stream_cmd = 'ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer -vcodec copy -map 0:0 -map 1:0 -strict experimental -f flv ' + YOUTUBE + KEY

# this ffmpeg command is working 
#stream_cmd = 'ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 32k -t 60 -b 2000 -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/abdq-sv6g-5a1m-2d72'				 
stream_cmd = 'ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 32k -t 60 -b 2000 -g 50 -strict experimental -f flv ' + YOUTUBE + KEY				 

# using raspivid for testing
#stream_cmd = 'raspivid -o - -t 0 -w 640 -h 480 -fps 10 -b 500000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 32k -t 300 -b 2000 -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/abdq-sv6g-5a1m-2d72'				 


stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE) 
camera = picamera.PiCamera() 
#camera.resolution = (1280, 720)
camera.resolution = (320, 240)
camera.rotation   = 0	 
#camera.crop       = (0.0, 0.0, 1.0, 1.0) 
camera.framerate  = 20 
rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)

#def stream():
#    print('stream function')
#    camera.wait_recording(1)

	
#def shutdown_pi():
#    print('shutdown pi function') 
#    os.system("sudo shutdown -h now")

#def preview():
#    print('preview  function')
#    stream = io.BytesIO()
#    camera.vflip = True
#    camera.hflip = True
#    camera.capture(stream, use_video_port=True, format='rgb', resize=(320, 240))
#    stream.seek(0)
#    stream.readinto(rgb)
#    stream.close() 

#stream()
#camera.vflip = True 
#camera.hflip = True 
#camera.start_recording(stream_pipe.stdin, format='h264', bitrate = 500000)


print('...start recoding')

camera.start_preview()
camera.start_recording(stream_pipe.stdin, format='h264', bitrate = 500000) 
#camera.start_recording('my_video.h264')

#sleep(60)
camera.wait_recording(60)


camera.stop_recording()
camera.stop_preview()
os.system('killall ffmpeg')
print('...stop recoding and ffmpeg pump to Youtube')


