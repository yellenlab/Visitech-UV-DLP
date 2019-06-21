from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class VisitechDLP:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://192.168.0.10/cgi-bin/login.lua")

        self.login()

    def login(self):
        elem = self.driver.find_element_by_name('username')
        elem.clear()
        elem.send_keys("lbuser")
        elem = self.driver.find_element_by_name('password')
        elem.clear()
        elem.send_keys("4k6VT")
        elem.send_keys(Keys.RETURN)

    def load_image(self, image_path, inum_location='0'):
        page_link = self.driver.find_element_by_link_text('Load Image')
        page_link.click()
        inum = self.driver.find_element_by_name('inum')
        inum.clear()
        inum.send_keys(inum_location)
        elem = self.driver.find_element_by_name('ufile')
        elem.send_keys(image_path)
        set_im = self.driver.find_element_by_xpath(
                            "//input[@value='Upload File']")
        set_im.click()

    def load_sequence(self, seq_path):
        page_link = self.driver.find_element_by_link_text('Sequence Control')
        page_link.click()
        path = self.driver.find_element_by_name('seqfile')
        path.send_keys(seq_path)
        set_seq = self.driver.find_element_by_xpath(
                            "//input[@value='Load Selected File']")
        set_seq.click()