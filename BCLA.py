####################################################################################################
# Selenium Test Suite for dev.bclaconnect.ca created by Harris Mckay for the BC Libraries Coop     #
# Python unittest used to make test cases. Cases are independant.                                  #
####################################################################################################
import unittest
import os
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

class NNELSTests(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.conf")
        self.driver = webdriver.Firefox()

    def test_register_as_individual(self):
        # Go to the bcla home page  
        self.driver.get("https://dev.bclaconnect.ca")
        WebDriverWait(self.driver, 10).until(EC.title_contains("BCLA Connect"))
        # Hover over myBCLA button, click join button
        mouse = webdriver.ActionChains(self.driver)
        myBCLA = self.driver.find_element_by_xpath("//a[@href='/mybcla']")
        mouse.move_to_element(myBCLA).perform()
        joinButton_present = EC.presence_of_element_located((By.XPATH, "//a[@href='/membership/join-bcla/'][@class='bcla-login-link']"))
        WebDriverWait(self.driver, 10).until(joinButton_present)
        self.driver.find_element_by_xpath("//a[@href='/membership/join-bcla/'][@class='bcla-login-link']").click()
        # Choose individual membership
        WebDriverWait(self.driver, 10).until(EC.title_contains("Join BCLA |"))
        self.driver.find_element_by_link_text("Individual Membership").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Individual Membership |"))
        # Fill in form
        randomString = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(5))
        mailAddress = randomString + '@mailinator.com'
        self.driver.find_element_by_id("email-5").send_keys(mailAddress)
        self.driver.find_element_by_id("cms_name").send_keys(self.config['account']['username'] + randomString)
        self.driver.find_element_by_id("cms_pass").send_keys(self.config['account']['password'])
        self.driver.find_element_by_id("cms_confirm_pass").send_keys(self.config['account']['password'])
        self.driver.find_element_by_id("first_name").send_keys(self.config['account']['firstname'])
        self.driver.find_element_by_id("last_name").send_keys(self.config['account']['lastname'])
        self.driver.find_element_by_id("street_address-Primary").send_keys(self.config['account']['address'])
        self.driver.find_element_by_id("city-Primary").send_keys(self.config['account']['city'])
        #self.driver.find_element_by_xpath("//div[@id='s2id_state_province-Primary']").click()
        self.driver.find_element_by_id("postal_code-Primary").send_keys(self.config['account']['postal'])
        self.driver.find_element_by_xpath("//a[@class='crm-credit_card_type-icon-mastercard']").click()
        self.driver.find_element_by_id("credit_card_number").send_keys('5555555555554444')
        self.driver.find_element_by_id("cvv2").send_keys('066')
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_M']/option[text()='Jan']").click()
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_Y']/option[text()='2026']").click()
        self.driver.find_element_by_id("CIVICRM_QFID_0_12").click()
        self.driver.find_element_by_id("_qf_Main_upload-bottom").click()
        #Click "make payment"
        paymentButton_present = EC.presence_of_element_located((By.ID, "_qf_Confirm_next-top"))
        WebDriverWait(self.driver, 10).until(paymentButton_present)
        self.driver.find_element_by_id("_qf_Confirm_next-top").click()
        # Check that payment went through
        WebDriverWait(self.driver, 60).until(EC.title_contains("Welcome to BCLA"))
        src = self.driver.page_source
        text_found = re.search(r'Your transaction has been processed successfully. Please print this page for your records.', src)
        self.assertNotEqual(text_found, None)
        # Check the email was sent and received
        self.driver.get("https://www.mailinator.com/inbox2.jsp?public_to=" + randomString + "#/#public_maildirdiv")
        WebDriverWait(self.driver, 30).until(EC.title_contains("Mailinator"))
        self.driver.find_element_by_xpath("//div[@class='innermail ng-binding'][contains(., 'Welcome to BCLA Connect')]").click()
        mailText_present = EC.presence_of_element_located((By.ID, "publicshowmaildivcontent"))
        WebDriverWait(self.driver, 20).until(mailText_present)
        src = self.driver.page_source
        text_found = re.search(mailAddress, src)
        self.assertNotEqual(text_found, None)
        print("Transaction completed succesfully, confirmation email received succesfully at")
        print("https://www.mailinator.com/inbox2.jsp?public_to=" + randomString + "#/#public_maildirdiv")
                                                                       
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
