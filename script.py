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

# get the list of all courses
i=1
list_courses= []
print("\r",end="")
while True:
    try:
        name = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/section/div/aside/div/div[2]/div/div["+str(i)+"]/div[1]/h2/a").text
        list_courses.append(name)
        i+=1
    except:
        break
print("All courses taken this semester are: ")
print()
for course in list_courses:
    print(course)
print()

# get attendance of each course
print('Attendance per course is:')
driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/section/div/aside/div/div[2]/div/div[6]/div[1]/h2/a").click() # select a random course
driver.find_element(By.XPATH, "//span[contains(.,'Attendance')]").click() # click on its attendance
driver.find_element(By.LINK_TEXT, "All courses").click() # click on every other course
i = 1
while True:
    try:
        cname = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div/section/div/table/tbody/tr/td[2]/h3['+str(i)+']').text
        if cname in list_courses:
            tot = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div/div/section/div/table/tbody/tr/td[2]/table['+str(i)+']/tbody/tr[1]/td[2]').text
            att = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div/div/section/div/table/tbody/tr/td[2]/table['+str(i)+']/tbody/tr[2]/td[2]').text
            print(cname+":" + att + "/"+tot)
        i += 1
    except:
        break

driver.quit()