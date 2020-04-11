from selenium import webdriver
import time
import autoit
from selenium.webdriver.common.action_chains import ActionChains

driver = ''
options = ''
def start_browser():
    global driver
    global options
    options = webdriver.ChromeOptions()
    options.add_argument('lang=pt-br')
    driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
    driver.get('https://pt.stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fpt.stackoverflow.com%2f')
    input('login then press enter')

def upload(filename, old_uploader_url, file_window_title, file_folder):
    driver.get(old_uploader_url)
    time.sleep(10)
    upload_btn = driver.find_element_by_id('start-upload-button-single')
    hover = ActionChains(driver).move_to_element(upload_btn)
    time.sleep(3)
    hover.click().perform()
    time.sleep(3)
    autoit.win_active(file_window_title)
    filename = file_folder + filename
    autoit.control_send(file_window_title,"Edit1", filename)
    autoit.control_send(file_window_title,"Edit1","{ENTER}")
    time.sleep(10)
    driver.find_elements_by_class_name('save-changes-button')[0].click()



