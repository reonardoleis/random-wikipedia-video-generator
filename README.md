# random-wikipedia-video-generator
A simple Python app which generates a TTS-narrated video from a random Wikipedia article and uploads to YouTube via Selenium.

# Usage

## 1. Place generate.py and upload.py on the same folder as your "main" Python file.
## 2. Import generate and upload
## 3. Run upload.start_browser(), click "Login with Google". Put your account credentials to login. When logged in, just press enter on the console.
## 4. Use generate.generate(DESIRED_LANGUAGE) to generate a video. Note that this function returns the generated file filename.
### -> DESIRED_LANGUAGE: Wikipedia random article's language (e.g: en, pt, ru...)

## 5. Use upload.upload(FILENAME, OLD_UPLOADER_URL, FILE_WINDOW_NAME) to upload the file.
### -> FILENAME: the generate.generate() return value
### -> OLD_UPLOADER_URL: your Google Account's old uploader URL. You can get it on YouTube.
### -> FILE_WINDOW_NAME: the title of the select file dialog (default is "Open")
