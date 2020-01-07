import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass

driver = webdriver.Chrome(executable_path=os.popen('which chromedriver').read().strip())

# get the values from a file
try:
    fin=open('secret.txt',"r")
    a=fin.readlines()
    Email=a[0]
    Pass=a[1]
except:
    print("Error in finding the file")
    print("For now, enter the email and password, and we would create the file and store it there (as plaintext)")
    # get values from the user
    Email = input("Enter email : \t")
    Pass = getpass.getpass(prompt="Enter password : \t")
    # store the values in a file
    fout=open('secret.txt',"w")
    fout.write(Email)
    fout.write(Pass)

# login to the moodle page 
driver.get("https://moodle.iiit.ac.in/my")
driver.find_element(By.ID, "username").send_keys(Email)
driver.find_element(By.ID, "password").send_keys(Pass)
driver.find_element(By.NAME, "submit").click()
