#####################################################################################################
# Selenium Test Suite for dev.bclaconnect.ca created by Harris Mckay for the BC Libraries Coop      #
# Python unittest used to make test cases. Cases are NOT independant, two rely on the same account. #
# The test browser windows (one per account) will be left open so the tester can check emails.      #
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

class BCLATests(unittest.TestCase):
    # Unfortunately, the same random string is required for both tests that use the individual account, so it is defined here
    individualRandomString = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(5))
    
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.conf")
        self.driver = webdriver.Firefox()

    def test_aregister_as_individual(self):
        # This test creates the account that "test_donate_as_individual" uses, hence the "a" in the name, so Selenium runs it first
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
        mailAddress = BCLATests.individualRandomString + '@mailinator.com'
        self.driver.find_element_by_id("email-5").send_keys(mailAddress)
        self.driver.find_element_by_id("cms_name").send_keys(self.config['account']['username'] + BCLATests.individualRandomString)
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
        self.driver.get("https://www.mailinator.com/inbox2.jsp?public_to=" + BCLATests.individualRandomString + "#/#public_maildirdiv")
        WebDriverWait(self.driver, 30).until(EC.title_contains("Mailinator"))
        print("Mailbox at:")
        print("https://www.mailinator.com/inbox2.jsp?public_to=" + BCLATests.individualRandomString + "#/#public_maildirdiv")
        print("Should contain a welcome message and receipt for an individual membership.")
        self.driver.quit()
        #self.driver.find_element_by_xpath("//div[@class='innermail ng-binding'][contains(.,'Welcome to BCLA')]").click()
        #mailText_present = EC.presence_of_element_located((By.ID, "publicshowmaildivcontent"))
        #WebDriverWait(self.driver, 20).until(mailText_present)
        #src = self.driver.page_source
        #text_found = re.search(mailAddress, src)
        #self.assertNotEqual(text_found, None)

    def test_donate_as_individual(self):
        # Go to the bcla home page  
        self.driver.get("https://dev.bclaconnect.ca")
        WebDriverWait(self.driver, 10).until(EC.title_contains("BCLA Connect"))
        # Hover over myBCLA button, click login button
        mouse = webdriver.ActionChains(self.driver)
        myBCLA = self.driver.find_element_by_xpath("//a[@href='/mybcla']")
        mouse.move_to_element(myBCLA).perform()
        loginButton_present = EC.presence_of_element_located((By.XPATH, "//a[@href='/login'][@class='bcla-login-link']"))
        WebDriverWait(self.driver, 10).until(loginButton_present)
        self.driver.find_element_by_xpath("//a[@href='/login'][@class='bcla-login-link']").click()
        # Log in
        WebDriverWait(self.driver, 10).until(EC.title_contains("Log In |"))
        time.sleep(1)
        self.driver.find_element_by_id("user_login").send_keys(self.config['account']['username'] + BCLATests.individualRandomString)
        time.sleep(1)
        self.driver.find_element_by_id("user_pass").send_keys(self.config['account']['password'])
        self.driver.find_element_by_id("wp-submit").click()
        # Navigate to donation page and fill in form
        mailAddress = BCLATests.individualRandomString + '@mailinator.com'
        self.driver.find_element_by_xpath("//*[@id='menu-item-2857']/a").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Donate to BCLA |"))
        self.driver.find_element_by_id("price_187").send_keys("12.34")
        self.driver.find_element_by_id("CIVICRM_QFID_BCLA_Awards_and_Scholarships_4").click()
        self.driver.find_element_by_xpath("//a[@class='crm-credit_card_type-icon-mastercard']").click()
        self.driver.find_element_by_id("credit_card_number").send_keys('5555555555554444')
        self.driver.find_element_by_id("cvv2").send_keys('066')
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_M']/option[text()='Jan']").click()
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_Y']/option[text()='2026']").click()
        self.driver.find_element_by_id("_qf_Main_upload-bottom").click()
        # Make payment
        paymentButton_present = EC.presence_of_element_located((By.ID, "_qf_Confirm_next-top"))
        WebDriverWait(self.driver, 10).until(paymentButton_present)
        self.driver.find_element_by_id("_qf_Confirm_next-top").click()
        # Check that payment went through
        WebDriverWait(self.driver, 60).until(EC.title_contains("Thank you for your donation! |"))
        src = self.driver.page_source
        text_found = re.search(r'Your transaction has been processed successfully. Please print this page for your records.', src)
        self.assertNotEqual(text_found, None)
        # Check the email was sent and received
        self.driver.get("https://www.mailinator.com/inbox2.jsp?public_to=" + BCLATests.individualRandomString + "#/#public_maildirdiv")
        WebDriverWait(self.driver, 30).until(EC.title_contains("Mailinator"))
        print("Mailbox at:")
        print("https://www.mailinator.com/inbox2.jsp?public_to=" + BCLATests.individualRandomString + "#/#public_maildirdiv")
        print("Should contain a receipt for an individual donation.")
        #self.driver.find_element_by_xpath("//div[@class='innermail ng-binding'][contains(.,'Donate to BCLA')]").click()
        #mailText_present = EC.presence_of_element_located((By.ID, "publicshowmaildivcontent"))
        #WebDriverWait(self.driver, 20).until(mailText_present)
        #src = self.driver.page_source
        #text_found = re.search(mailAddress, src)
        #self.assertNotEqual(text_found, None)

    def test_register_as_institution(self):
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
        # Choose institutional membership
        WebDriverWait(self.driver, 10).until(EC.title_contains("Join BCLA |"))
        self.driver.find_element_by_link_text("Institutional Membership").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Institutional Membership"))
        # Fill in form
        self.driver.find_element_by_id("CIVICRM_QFID_490_16").click()
        randomString = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(5))
        mailAddress = randomString + '@mailinator.com'
        self.driver.find_element_by_id("email-5").send_keys(mailAddress)
        usrName = self.config['account']['username'] + randomString
        self.driver.find_element_by_id("onbehalf_organization_name").send_keys(usrName)
        self.driver.find_element_by_id("onbehalf_phone-3-1").send_keys(self.config['account']['phone'])
        self.driver.find_element_by_id("onbehalf_email-3").send_keys(mailAddress)
        self.driver.find_element_by_id("onbehalf_street_address-3").send_keys(self.config['account']['address'])
        self.driver.find_element_by_id("onbehalf_city-3").send_keys(self.config['account']['city'])
        self.driver.find_element_by_id("onbehalf_postal_code-3").send_keys(self.config['account']['postal'])
        self.driver.find_element_by_id("cms_name").send_keys(usrName)
        self.driver.find_element_by_id("cms_pass").send_keys(self.config['account']['password'])
        self.driver.find_element_by_id("cms_confirm_pass").send_keys(self.config['account']['password'])
        self.driver.find_element_by_id("first_name").send_keys(self.config['account']['firstname'])
        self.driver.find_element_by_id("last_name").send_keys(self.config['account']['lastname'])
        self.driver.find_element_by_xpath("//a[@class='crm-credit_card_type-icon-mastercard']").click()
        self.driver.find_element_by_id("credit_card_number").send_keys('5555555555554444')
        self.driver.find_element_by_id("cvv2").send_keys('066')
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_M']/option[text()='Jan']").click()
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_Y']/option[text()='2026']").click()
        self.driver.find_element_by_id("billing_first_name").send_keys(self.config['account']['firstname'])
        self.driver.find_element_by_id("billing_last_name").send_keys(self.config['account']['lastname'])
        self.driver.find_element_by_id("billing_street_address-5").send_keys(self.config['account']['address'])
        self.driver.find_element_by_id("billing_city-5").send_keys(self.config['account']['city'])
        self.driver.find_element_by_id("billing_postal_code-5").send_keys(self.config['account']['postal'])
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
        print("Mailbox at:")
        print("https://www.mailinator.com/inbox2.jsp?public_to=" + randomString + "#/#public_maildirdiv")
        print("Should contain a welcome message and receipt for an institutional membership.")

    def test_donate_as_anonymous(self):
        # Go to the bcla home page  
        self.driver.get("https://dev.bclaconnect.ca")
        WebDriverWait(self.driver, 10).until(EC.title_contains("BCLA Connect"))
        # Navigate to donation page and fill in form
        self.driver.find_element_by_xpath("//*[@id='menu-item-2857']/a").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Donate to BCLA |"))
        randomString = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(5))
        mailAddress = randomString + '@mailinator.com'
        self.driver.find_element_by_id("email-5").send_keys(mailAddress)
        self.driver.find_element_by_id("price_187").send_keys("12.34")
        self.driver.find_element_by_id("CIVICRM_QFID_BCLA_Awards_and_Scholarships_4").click()
        self.driver.find_element_by_xpath("//a[@class='crm-credit_card_type-icon-mastercard']").click()
        self.driver.find_element_by_id("credit_card_number").send_keys('5555555555554444')
        self.driver.find_element_by_id("cvv2").send_keys('066')
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_M']/option[text()='Jan']").click()
        self.driver.find_element_by_xpath("//select[@id='credit_card_exp_date_Y']/option[text()='2026']").click()
        self.driver.find_element_by_id("billing_first_name").send_keys(self.config['account']['firstname'])
        self.driver.find_element_by_id("billing_last_name").send_keys(self.config['account']['lastname'])
        self.driver.find_element_by_id("billing_street_address-5").send_keys(self.config['account']['address'])
        self.driver.find_element_by_id("billing_city-5").send_keys(self.config['account']['city'])
        self.driver.find_element_by_id("billing_postal_code-5").send_keys(self.config['account']['postal'])
        self.driver.find_element_by_id("_qf_Main_upload-bottom").click()
        # Make payment
        paymentButton_present = EC.presence_of_element_located((By.ID, "_qf_Confirm_next-top"))
        WebDriverWait(self.driver, 10).until(paymentButton_present)
        self.driver.find_element_by_id("_qf_Confirm_next-top").click()
        # Check that payment went through
        WebDriverWait(self.driver, 60).until(EC.title_contains("Thank you for your donation! |"))
        src = self.driver.page_source
        text_found = re.search(r'Your transaction has been processed successfully. Please print this page for your records.', src)
        self.assertNotEqual(text_found, None)
        # Check the email was sent and received
        self.driver.get("https://www.mailinator.com/inbox2.jsp?public_to=" + randomString + "#/#public_maildirdiv")
        WebDriverWait(self.driver, 30).until(EC.title_contains("Mailinator"))
        print("Mailbox at:")
        print("https://www.mailinator.com/inbox2.jsp?public_to=" + randomString + "#/#public_maildirdiv")
        print("Should contain a receipt for an anonymous donation.")
        #self.driver.find_element_by_xpath("//div[@class='innermail ng-binding'][contains(.,'Donate to BCLA')]").click()
        #mailText_present = EC.presence_of_element_located((By.ID, "publicshowmaildivcontent"))
        #WebDriverWait(self.driver, 20).until(mailText_present)
        #src = self.driver.page_source
        #text_found = re.search(mailAddress, src)
        #self.assertNotEqual(text_found, None)
        
#    def tearDown(self):
#        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
