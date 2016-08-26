#####################################################################################################
# Selenium Test Suite for Libpress websites created by Harris Mckay for the BC Libraries Coop       #
# Specifically tests the maple.bc.libraries.coop site and checks www.vanderhooflibrary.com          #
# Python unittest used to make test cases. Cases are independant, and log out of accounts.          #
# Several Warnings are generated by Selenium/Python, this is okay, just look for the "OK" message.  #
#####################################################################################################
import unittest
import configparser
import time
import re
import random
import string
from selenium import webdriver
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LibPressTests(unittest.TestCase):
    
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.conf")
        self.driver = webdriver.Firefox()

    def test_check_maple(self):
        # Go to the maple public library home page and check for "Total load:" text
        self.driver.get("http://maple.bc.libraries.coop")
        WebDriverWait(self.driver, 10).until(EC.title_contains("Maple Public Library"))
        src = self.driver.page_source
        text_found = re.search(r'Total load:', src)
        self.assertNotEqual(text_found, None)
        
    def test_check_customdomain(self):
        # Go to the vanderhoof library home page  
        self.driver.get("http://www.vanderhooflibrary.com")
        WebDriverWait(self.driver, 10).until(EC.title_contains("Vanderhoof Public Library"))
        src = self.driver.page_source
        text_found = re.search(r'Total load:', src)
        self.assertNotEqual(text_found, None)
        # Navigate to search page, check redirection worked and try a search
        self.driver.find_element_by_xpath("//button[@class='btn btn-round search-form-btn']").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Search Results:"))
        URL = self.driver.current_url
        text_found = re.search(r'bvdh.bc.catalogue.libraries.coop/eg/opac', URL)
        self.assertNotEqual(text_found, None)
        self.driver.find_element_by_id("search_box").send_keys("test")
        self.driver.find_element_by_id("search-submit-go").click()
        result_present = EC.presence_of_element_located((By.XPATH, "//a[@class='record_title search_link'][@name='record_103332573']"))
        WebDriverWait(self.driver, 20).until(result_present)

    def test_login_maple(self):
        # Go to the maple public library wordpress login; log in
        self.driver.get("http://maple.bc.libraries.coop/wp-login.php")
        result_present = EC.presence_of_element_located((By.ID, "user_login"))
        WebDriverWait(self.driver, 10).until(result_present)
        self.driver.find_element_by_id("user_login").send_keys(self.config['account']['username'])
        self.driver.find_element_by_id("user_pass").send_keys(self.config['account']['password'])
        self.driver.find_element_by_id("wp-submit").click()
        # navigate to sitka-lists page
        WebDriverWait(self.driver, 10).until(EC.title_contains("Dashboard ‹ Maple Public Library — WordPress"))
        self.driver.find_element_by_id("toplevel_page_site-manager").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Contact Information"))
        self.driver.find_element_by_xpath("//a[@href='admin.php?page=sitka-lists']").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Sitka List Titles"))
        # Rebuild picklist
        self.driver.find_element_by_xpath("//button[@class='button sitka-rebuild-picklist-btn']").click()
        alert = self.driver.switch_to_alert() # This will cause a warning, but the "newer" method of this does not work.
        alert.accept()
        time.sleep(2)
        # Hover over "New" dropdown, click "Highlight" button
        mouse = webdriver.ActionChains(self.driver)
        newDrop = self.driver.find_element_by_xpath("//a[@href='http://maple.bc.libraries.coop/wp-admin/post-new.php'][@class='ab-item'][@aria-haspopup='true']")
        mouse.move_to_element(newDrop).perform()
        highlightButton_present = EC.presence_of_element_located((By.XPATH, "//a[@class='ab-item'][text()='Highlight']"))
        WebDriverWait(self.driver, 10).until(highlightButton_present)
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[@class='ab-item'][text()='Highlight']").click()
        # Create and publish a new highlight
        WebDriverWait(self.driver, 10).until(EC.title_contains("Add New Highlight"))
        self.driver.find_element_by_xpath("//select[@id='coop-sitka-lists']/option[text()='Adult Fiction']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@id='publish']").send_keys("\n") # NOTE: Need to send "\n" instead of click for some weird wordpress buttons..
        # View the new post
        viewPost_present = EC.presence_of_element_located((By.XPATH, "//a[text()='View post']"))
        WebDriverWait(self.driver, 10).until(viewPost_present)
        self.driver.find_element_by_xpath("//a[text()='View post']").click()
        # Check that the carousel in the post/highlght is present
        carousel_present = EC.presence_of_element_located((By.XPATH, "//img[@class='sitka-carousel-image']"))
        WebDriverWait(self.driver, 10).until(carousel_present)
        # Hover over account dropdown, click "Log Out" button
        mouse = webdriver.ActionChains(self.driver)
        acctDrop = self.driver.find_element_by_xpath("//a[@href='http://maple.bc.libraries.coop/wp-admin/profile.php'][@class='ab-item'][@aria-haspopup='true']")
        mouse.move_to_element(acctDrop).perform()
        logOutButton_present = EC.presence_of_element_located((By.XPATH, "//a[@class='ab-item'][text()='Log Out']"))
        WebDriverWait(self.driver, 10).until(logOutButton_present)
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[@class='ab-item'][text()='Log Out']").click()

        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
