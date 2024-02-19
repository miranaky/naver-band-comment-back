# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Test2():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_2(self):
    self.driver.get("https://auth.band.us/")
    self.driver.set_window_size(1504, 1667)
    self.driver.find_element(By.CSS_SELECTOR, "#email_login_a > .text").click()
    self.driver.find_element(By.ID, "input_email").send_keys("ril_k")
    self.driver.find_element(By.ID, "input_email").click()
    self.driver.find_element(By.ID, "input_email").click()
    self.driver.find_element(By.ID, "input_email").click()
    element = self.driver.find_element(By.ID, "input_email")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.ID, "input_email").click()
    self.driver.find_element(By.ID, "input_email").send_keys("smkang0321@gmail.com")
    self.driver.find_element(By.CSS_SELECTOR, ".uBtn").click()
    self.driver.find_element(By.ID, "pw").click()
    self.driver.find_element(By.ID, "pw").send_keys("cjdfyd2024!")
    self.driver.find_element(By.CSS_SELECTOR, ".uBtn").click()
    self.driver.find_element(By.CSS_SELECTOR, ".bandCardItem:nth-child(3) .uCoverImage").click()
    self.driver.find_element(By.CSS_SELECTOR, ".cCard:nth-child(1) .postSet").click()
    self.driver.find_element(By.LINK_TEXT, "주소 복사").click()
  
