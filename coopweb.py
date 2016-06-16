####################################################################################################
# Selenium Test Suite for bc.libraries.coop created by Harris Mckay for the BC Libraries Coop      #
# Python unittest used to make test cases. Every case is independent.                              #
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

class CoopWebTests(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.conf")
        self.driver = webdriver.Firefox()

    def test_search_for_doc(self):
        # Go to the coop home page  
        self.driver.get("https://bc.libraries.coop/")
        # Search for "document"
        self.driver.find_element_by_id("searchbtn").click()
        searchField_present = EC.presence_of_element_located((By.XPATH, "//input[@name='s'][@title='Search for:']"))
        WebDriverWait(self.driver, 10).until(searchField_present)
        searchField = self.driver.find_element_by_xpath("//input[@name='s'][@title='Search for:']")
        searchField.send_keys("document")
        searchField.submit()
        # Click the specific document and ensure it opens
        WebDriverWait(self.driver, 10).until(EC.title_contains("document | Search Results"))
        self.driver.find_element_by_link_text("Joining the Co-op").click()
        src = self.driver.page_source
        text_found = re.search(r'Joining the Co-op', src)
        self.assertNotEqual(text_found, None)
		
    def test_login_and_create_doc(self):
        # Go to the coop home page  
        self.driver.get("https://bc.libraries.coop/")
        # Log in
        self.driver.find_element_by_id("loginbtn").click()
        usernameField_present = EC.presence_of_element_located((By.ID, 'user_login'))
        WebDriverWait(self.driver, 10).until(usernameField_present)
        self.driver.find_element_by_id("user_login").send_keys(self.config['account']['username'])
        time.sleep(2)
        self.driver.find_element_by_id("user_pass").send_keys(self.config['account']['password'])
        time.sleep(2)
        self.driver.find_element_by_id("user-submit").click()
        time.sleep(2)
        # Go to Profile, Docs tab, click Create New Doc
        self.driver.find_element_by_id("loginbtn").click()
        profileButton_present = EC.presence_of_element_located((By.LINK_TEXT, 'My Profile'))
        WebDriverWait(self.driver, 10).until(profileButton_present)
        self.driver.find_element_by_link_text("My Profile").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Profile |"))
        self.driver.find_element_by_id("user-docs").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Docs |"))
        self.driver.find_element_by_id("bp-create-doc-button").click()
        # Fill in Doc creation form
        titleField_present = EC.presence_of_element_located((By.ID, 'doc-title'))
        WebDriverWait(self.driver, 10).until(titleField_present)
        self.driver.find_element_by_id("doc-title").send_keys("Selenium Test Document")
        self.driver.find_element_by_id("doc_content-html").click()
        contentField_present = EC.presence_of_element_located((By.XPATH, "//textarea[@id='doc_content'][@name='doc_content']"))
        WebDriverWait(self.driver, 10).until(contentField_present)
        self.driver.find_element_by_xpath("//textarea[@id='doc_content'][@name='doc_content']").send_keys(
            "This is a test document created to test site functionality with Selenium Webdriver.")
        self.driver.find_element_by_xpath("//select[@id='settings-read']/option[text()='The Doc author only']").click()
        # Save doc and check it was succesfully created
        self.driver.find_element_by_id("doc-edit-submit").click()
        src = self.driver.page_source
        text_found = re.search(r'Doc successfully created', src)
        self.assertNotEqual(text_found, None)
        # Delete the doc and check it was succesfully deleted
        self.driver.find_element_by_link_text("Edit").click()
        deleteButton_present = EC.presence_of_element_located((By.LINK_TEXT, 'Permanently Delete'))
        WebDriverWait(self.driver, 10).until(deleteButton_present)
        self.driver.find_element_by_link_text("Permanently Delete").click()
        alert = self.driver.switch_to_alert() # This will cause a warning, but the "newer" method of this does not work.
        alert.accept()
        time.sleep(2)
        src = self.driver.page_source
        text_found = re.search(r'Doc successfully deleted', src)
        self.assertNotEqual(text_found, None)

    def test_login_and_post(self):
        # Go to the coop home page  
        self.driver.get("https://bc.libraries.coop/")
        # Log in
        self.driver.find_element_by_id("loginbtn").click()
        usernameField_present = EC.presence_of_element_located((By.ID, 'user_login'))
        WebDriverWait(self.driver, 10).until(usernameField_present)
        self.driver.find_element_by_id("user_login").send_keys(self.config['account']['username'])
        time.sleep(2)
        self.driver.find_element_by_id("user_pass").send_keys(self.config['account']['password'])
        time.sleep(2)
        self.driver.find_element_by_id("user-submit").click()
        time.sleep(2)
        # Navigate to My Dashboard
        self.driver.find_element_by_id("loginbtn").click()
        dashboardButton_present = EC.presence_of_element_located((By.LINK_TEXT, 'My Dashboard'))
        WebDriverWait(self.driver, 10).until(dashboardButton_present)
        self.driver.find_element_by_link_text("My Dashboard").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Dashboard |"))
        # Navigate to test group, write and publish a post
        self.driver.find_element_by_xpath("//span[@class='group-title']").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Home | Maple Public Library |"))
        self.driver.find_element_by_xpath("//textarea[@id='whats-new'][@name='whats-new']").send_keys(
            "This is a test post by Selenium Webdriver")
        self.driver.find_element_by_xpath(
            "//input[@id='aw-whats-new-submit']").send_keys("\n") # NOTE: Need to send "\n" instead of click for some weird wordpress buttons..
        # Check that the post is present, then delete it
        post_present = EC.presence_of_element_located((
            By.XPATH, "//div[@class='activity-inner']/p[text()='This is a test post by Selenium Webdriver']/../../div[@class='activity-meta']/a[text()='Delete']"))
        WebDriverWait(self.driver, 10).until(post_present)
        self.driver.find_element_by_xpath(
            "//div[@class='activity-inner']/p[text()='This is a test post by Selenium Webdriver']/../../div[@class='activity-meta']/a[text()='Delete']").send_keys("\n")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
