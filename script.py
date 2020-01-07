import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass

driver = webdriver.Chrome(executable_path=os.popen('which chromedriver').read().strip())

# get values from the user
Email = input("Enter email : \t")
Pass = getpass.getpass(prompt="Enter password : \t")

# login to the moodle page 
driver.get("https://moodle.iiit.ac.in/my")
driver.find_element(By.ID, "username").send_keys(Email)
driver.find_element(By.ID, "password").send_keys(Pass)
driver.find_element(By.NAME, "submit").click()

