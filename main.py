from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib, urllib.request
import os
import selenium.common.exceptions as SE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def upload_img(img_path):
    driver.get('https://resizeimage.net/')
    upload_button = driver.find_element_by_css_selector('.LineBigBtn input')
    driver.execute_script("arguments[0].style.display = 'block';", upload_button)
    upload_button.send_keys(img_path)
    time.sleep(3)


def get_width_and_height():
    w_input = driver.find_element_by_id("InputResizeW")
    h_input = driver.find_element_by_id("InputResizeH")
    width = int(w_input.get_attribute("value"))
    height = int(h_input.get_attribute("value"))
    if width > height:
        max_dim = w_input
    else:
        max_dim = h_input
    max_dim.send_keys(Keys.CONTROL + "a")
    max_dim.send_keys("1200")


def set_compression(percentage):
    normal_compression_toggle = driver.find_element_by_id('opt_jpg_normal')
    normal_compression_toggle.click()
    img_quality = driver.find_element_by_id('InputJpgQuality')
    img_quality.send_keys(Keys.CONTROL + "a")
    img_quality.send_keys(percentage)


def click_resize():
    do_resize_btn = driver.find_element_by_id('doResize')
    do_resize_btn.click()
    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present())
        print('Switching to Alert')
        alert = driver.switch_to.alert
        time.sleep(5)
        alert.accept()
        click_resize()
        print("alert Exists in page")
    except TimeoutException:
        print("alert does not Exist in page")



def view_img():
    global p
    print(f'Valor do P = {p}')
    time.sleep(3)
    try:
        view_img_btn = driver.find_element_by_xpath('//*[@id="output_file_info"]/a[1]')
        view_img_btn.click()
        img_window = driver.window_handles[-1]
        driver.switch_to.window(img_window)
    except:
        get_width_and_height()
        p = str(int(p) - 10)
        set_compression(p)
        click_resize()
        time.sleep(3)
        view_img()


def get_img(file_folder, file_name):
    time.sleep(3)
    img_tag = driver.find_element_by_css_selector('body img')
    driver.execute_script("arguments[0].style.display = 'block';", img_tag)
    src = img_tag.get_attribute('src')
    print(src)
    urllib.request.urlretrieve(src, f'{file_folder}/{file_name}')
    root_window = driver.window_handles[0]
    driver.close()
    driver.switch_to.window(root_window)


driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')

massa_path = f'C:/Users/Ericbc/Squad/Clientes/MASSA/Imóveis'
imoveis = os.listdir(massa_path)


for imovel in imoveis:
    imovel_path = f'{massa_path}/{imovel}'
    galeria_path = f"{imovel_path}/Galeria"
    new_img_folder = f'{imovel_path}//Nova Galeria'
    for file in os.listdir(galeria_path):
        if file.endswith(".jpg"):
            p = '70'
            if not os.path.exists(f'{imovel_path}/Nova Galeria/{file}'):
                print(f'Starting file {file} in folder {imovel}')
                image_path = f'{galeria_path}/{file}'

                # Rodar funções para fazer o resize
                upload_img(image_path)
                get_width_and_height()
                set_compression(p)
                click_resize()
                view_img()
                get_img(new_img_folder, file)
                time.sleep(5)
            else:
                print(f"File {file} already exists in folder {imovel}")