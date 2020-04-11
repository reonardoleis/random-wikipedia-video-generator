import generate
import upload
import time


upload.start_browser()

old_uploader_url = 'https://www.youtube.com/upload?redirect_to_creator=true&fr=4&ar=1586612008057&nv=1'

for x in range (0, 3):
    filename = generate.generate('pt')
    upload.upload(filename, old_uploader_url, "Abrir")
    time.sleep(60)
