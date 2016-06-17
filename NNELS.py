####################################################################################################
# Selenium Test Suite for nnels.ca created by Harris Mckay for the BC Libraries Coop               #
# Python unittest used to make test cases. Cases are independant.                                  #
####################################################################################################
import unittest
import os
import configparser
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class NNELSTests(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.conf")

        # To prevent download dialog
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', self.config['files']['dpath'])
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
        self.driver = webdriver.Firefox(profile)

    def test_login_and_create_doc(self):
        # Go to the NNELS home page and click Login
        self.driver.get("https://nnels.ca")
        self.driver.find_element_by_link_text("Login").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Log in |"))
        # Log in to NNELS
        self.driver.find_element_by_id("edit-name").send_keys(self.config['account']['username'])
        self.driver.find_element_by_id("edit-pass").send_keys(self.config['account']['password'])
        self.driver.find_element_by_xpath("//input[@id='edit-submit'][@value='Log in']").click()
        src = self.driver.page_source
        text_found = re.search(r'Log in successful for', src)
        self.assertNotEqual(text_found, None)
        # Search for "test" as an example
        searchField = self.driver.find_element_by_id("edit-search-api-views-fulltext-2")
        searchField.send_keys("test")
        searchField.submit()
        # Click a specific item
        self.driver.find_element_by_link_text("First test").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("First test |"))
        # Download the item and delete the local file
        self.driver.find_element_by_xpath("//span[@class='mp3']/a").click()
        time.sleep(120)
        os.remove(os.path.join(self.config['files']['dpath'],"3867_First_test.zip"))        

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
