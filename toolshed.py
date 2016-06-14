####################################################################################################
# Selenium Test Suite for www.librarytoolshed.ca created by Harris Mckay for the BC Libraries Coop #
# Python unittest used to make test cases. Not every case is fully independent.                    #
# Tests may fail due to Toolshed's unpredictable captcha requests if run too frequently.           #
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

class ToolshedTests(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.conf")

        # To prevent download dialog
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', self.config['files']['dpath'])
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.driver = webdriver.Firefox(profile)

    def test_alogin_and_upload(self):
        # NOTE: This is an independent test.
        # Go to the toolshed home page  
        self.driver.get("https://librarytoolshed.ca/")
        # Click login button
        self.driver.find_element_by_link_text("Login").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("User login | The Library Toolshed"))
        # Enter Username and Password from config.conf
        username = self.config['account']['username']
        self.driver.find_element_by_name("name").send_keys(username)
        self.driver.find_element_by_name("pass").send_keys(self.config['account']['password'])
        # Click Login
        self.driver.find_element_by_xpath("//input[@name='op'][@value='Log in']").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains(username + " | The Library Toolshed"))
        # Click Add Training Resource
        self.driver.find_element_by_link_text("Add Training Resource").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Create Training Resource"))
        # Filling in new resource
        # Title
        self.driver.find_element_by_id("edit-title").send_keys("Test Resource")
        # Topic selection
        topicSelect = self.driver.find_element_by_id('edit-field-training-topic-und')
        for option in topicSelect.find_elements_by_tag_name('option'):
            if option.text == 'ILS':
                option.click()
                break
        # Resource Type
        self.driver.find_element_by_xpath("//select[@id='edit-field-resource-type-und']/option[text()='Word']").click()
        # File upload from config.conf
        browseButton = self.driver.find_element_by_xpath("//input[@name='files[field_training_doc_file_und_0]'][@id='edit-field-training-doc-file-und-0-upload']")
        browseButton.send_keys(self.config['files']['upath'])
        # Description
        self.driver.find_element_by_id("switch_edit-field-description-und-0-value").click()
        textbox_present = EC.presence_of_element_located((By.ID, 'edit-field-description-und-0-value'))
        WebDriverWait(self.driver, 10).until(textbox_present)
        self.driver.find_element_by_id("edit-field-description-und-0-value").send_keys("This is a test resource for checking Toolshed's functionality.")
        # Source Library
        self.driver.find_element_by_xpath("//select[@id='edit-field-source-library-region-und']/option[text()='-BC Libraries Coop']").click()
        # Click Upload button and wait for remove button to appear
        self.driver.find_element_by_xpath("//input[@name='field_training_doc_file_und_0_upload_button'][@id='edit-field-training-doc-file-und-0-upload-button']").click()
        removeButton_present = EC.presence_of_element_located((By.ID, 'edit-field-training-doc-file-und-0-remove-button'))
        WebDriverWait(self.driver, 30).until(removeButton_present)
        # Click Save Button
        self.driver.find_element_by_xpath("//input[@name='op'][@id='edit-submit'][@value='Save']").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Test Resource | The Library Toolshed"))

    def test_browse_and_download(self):
        # NOTE: This test will probably fail if any extra "test resource" items are currently uploaded (IE if the delete test failed)
        # As such, it is NOT a fully independent test and relies on the upload and delete tests.
        self.driver.get("https://librarytoolshed.ca/")
        # Hover over Browse menu and click All Resources
        mouse = webdriver.ActionChains(self.driver)
        browseMenu = self.driver.find_element_by_id("menu-2881-1")
        mouse.move_to_element(browseMenu).perform()
        resourcesButton_present = EC.presence_of_element_located((By.LINK_TEXT, 'All Resources'))
        WebDriverWait(self.driver, 10).until(resourcesButton_present)
        self.driver.find_element_by_link_text("All Resources").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("All Training Resources | The Library Toolshed"))
        # Filter for previously uploaded resource and click Go to browse
        regionField = self.driver.find_element_by_id('s2id_autogen1')
        regionField.send_keys("British Columbia\n")
        libField_present = EC.presence_of_element_located((By.ID, 's2id_autogen5'))
        WebDriverWait(self.driver, 10).until(libField_present)
        libField = self.driver.find_element_by_id('s2id_autogen5')
        libField.send_keys("-BC Libraries Coop\n")
        self.driver.find_element_by_id('edit-submit-training-resources').click()
        # Find and click the desired resource
        testResource_present = EC.presence_of_element_located((By.LINK_TEXT, 'Test Resource'))
        WebDriverWait(self.driver, 10).until(testResource_present)
        self.driver.find_element_by_link_text("Test Resource").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Test Resource"))
        # Download the file
        self.driver.find_element_by_link_text("test.docx").click()
        time.sleep(10)
        # Delete the downloaded file
        os.remove(os.path.join(self.config['files']['dpath'],"test.docx"))        

    def test_clogin_and_delete(self):
        # NOTE: This test will fail if the upload test was not run first/failed.
        # As such, it is NOT an independent test.
        self.driver.get("https://librarytoolshed.ca/")
        # Click login button
        self.driver.find_element_by_link_text("Login").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("User login | The Library Toolshed"))
        # Enter Username and Password from config.conf
        username = self.config['account']['username']
        self.driver.find_element_by_name("name").send_keys(username)
        self.driver.find_element_by_name("pass").send_keys(self.config['account']['password'])
        # Click Login
        self.driver.find_element_by_xpath("//input[@name='op'][@value='Log in']").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains(username + " | The Library Toolshed"))
        # Click Your Content
        self.driver.find_element_by_link_text("Your Content").click()
        testResource_present = EC.presence_of_element_located((By.LINK_TEXT, 'Test Resource'))
        WebDriverWait(self.driver, 30).until(testResource_present)
        # Select the resource
        self.driver.find_element_by_link_text("Test Resource").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Test Resource | The Library Toolshed"))
        # Click the edit tab and the delete button (twice)
        self.driver.find_element_by_link_text("Edit").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Edit Training Resource Test Resource"))
        self.driver.find_element_by_id("edit-delete").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Are you sure you want to delete Test Resource"))
        self.driver.find_element_by_xpath("//input[@name='op'][@id='edit-submit'][@value='Delete']").click()
        # Check for the deletion confirmation on the main page
        src = self.driver.page_source
        text_found = re.search(r'has been deleted', src)
        self.assertNotEqual(text_found, None)

    def test_csearch_and_download(self):
        # NOTE: This is an independent test.
        self.driver.get("https://librarytoolshed.ca/")      
        # Find the element that's name attribute is keys (the search box)
        inputElement = self.driver.find_element_by_name("keys")
        # Type in the search (for some specific existing item)
        inputElement.send_keys("Computer Basics Glossary in Mandarin")
        inputElement.submit()
        # We have to wait for the page to refresh
        WebDriverWait(self.driver, 10).until(EC.title_contains("Search"))
        # Select the desired item
        self.driver.find_element_by_link_text("Computer Basics Glossary in Mandarin Chinese").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Computer Basics Glossary"))
        # Download the resource
        self.driver.find_element_by_link_text("VPL - PLG - Training Script - Computer Basics 1 and 2 in Mandarin - Glossary Handout.DOCX").click()
        time.sleep(10)
        # Delete the downloaded file
        os.remove(os.path.join(self.config['files']['dpath'],"VPL - PLG - Training Script - Computer Basics 1 and 2 in Mandarin - Glossary Handout.DOCX"))

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
