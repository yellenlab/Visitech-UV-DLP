from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_driver():
    driver = webdriver.Chrome()
    driver.get("http://192.168.0.10/cgi-bin/login.lua")
    return driver

def login():
    elem = driver.find_element_by_name('username')
    elem.clear()
    elem.send_keys("lbuser")
    elem = driver.find_element_by_name('password')
    elem.clear()
    elem.send_keys("4k6VT")
    elem.send_keys(Keys.RETURN)

def load_image(image_path, inum_location='0'):
    page_link = driver.find_element_by_link_text('Load Image')
    page_link.click()
    inum = driver.find_element_by_name('inum')
    inum.clear()
    inum.send_keys(inum_location)
    elem = driver.find_element_by_name('ufile')
    elem.send_keys(image_path)
    set_im = driver.find_element_by_xpath("//input[@value='Upload File']")
    set_im.click()

def load_sequence(seq_path):
    page_link = driver.find_element_by_link_text('Sequence Control')
    page_link.click()
    path = driver.find_element_by_name('seqfile')
    path.send_keys(seq_path)
    set_seq = driver.find_element_by_xpath("//input[@value='Load Selected File']")
    set_seq.click()