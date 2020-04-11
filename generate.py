import cv2
import numpy as np
from PIL import ImageEnhance
from PIL import Image
import glob
from moviepy.editor import *
import imageio
import requests
import wikipedia
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

from comtypes.client import CreateObject




output_name = ''

def save_image(image_url, im_name):
    img_data = requests.get(image_url).content
    with open('./images/'+im_name, 'wb') as handler:
        handler.write(img_data)


def random_page(lang):
   global output_name
   wikipedia.set_lang(lang)
   random = wikipedia.random(1)
   try:
       if len(wikipedia.page(random).images) < 4:
           result = random_page(lang)
       else:
           images = wikipedia.page(random).images
           output_name = wikipedia.page(random).title.replace(':', '', 10)
           print(output_name)
           for image in images:
            save_image(image, image.split('/')[len(image.split('/')) - 1])
            if ('svg' in image):
                drawing = svg2rlg('./images/'+image.split('/')[len(image.split('/')) - 1])
                renderPM.drawToFile(drawing, './images/'+image.split('/')[len(image.split('/')) - 1] + ".jpg", fmt="JPG")

            result = wikipedia.page(random).summary
   except wikipedia.exceptions.DisambiguationError as e:
       result = random_page(lang)
   return result

def generate(lang):
    global output_name
    text = random_page(lang)

    engine = CreateObject("SAPI.SpVoice")
    stream = CreateObject("SAPI.SpFileStream")
    from comtypes.gen import SpeechLib
    stream.Open('audio.mp3', SpeechLib.SSFMCreateForWrite)
    engine.AudioOutputStream = stream
    engine.speak(text)
    stream.Close()


    RESOLUTION = {800, 600}
    images = []
    for filename in glob.glob('./images/*.jpg'):
        images.append(filename)

    IMAGE_NUMBER = len(images)


    audioclip = AudioFileClip("audio.mp3")
    duration = audioclip.duration

    seconds = duration
    print(seconds)
    fps = 30



    total_frames = int(seconds * fps)

    FRAMES_PER_IMAGE = (total_frames) / IMAGE_NUMBER

    color_percentage_for_each_frame = (100 / total_frames) / 100

    write_to = 'output/{}.mp4'.format('project') # have a folder of output where output files could be stored.

    writer = imageio.get_writer(write_to, format='mp4', mode='I', fps=fps)

    current_image = 0
    next_change = FRAMES_PER_IMAGE

    for i in range(total_frames):
        if i < total_frames:
            im = Image.open(images[current_image])
            im = im.resize(RESOLUTION)
            if (i >= next_change):
                current_image += 1
                next_change += FRAMES_PER_IMAGE
                if (i >= len(images)):
                    i = 0
            processed = ImageEnhance.Color(im).enhance(
                color_percentage_for_each_frame * i)
            writer.append_data(np.asarray(processed))
        else:
            writer.append_data(np.asarray(im))
    writer.close()



    videoclip = VideoFileClip("./output/project.mp4")

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip = videoclip.subclip(0, duration)
    videoclip.write_videofile('./' + output_name + ".mp4")

    import os, shutil
    folder = './images'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return output_name + ".mp4"