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
driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/section/div/aside/div/div[2]/div/div[6]/div[1]/h2/a").click()# select a random course
driver.find_element(By.XPATH, "//span[contains(.,'Attendance')]").click() # click on its attendance
driver.find_element(By.LINK_TEXT, "All courses").click() # click on every other course
i = 1
attendance=list()
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
            l1=[cname,att,tot]
            attendance.append(l1)
        i += 1
    except:
        break
print()
driver.find_element(By.XPATH,"/html/body/div[3]/nav[2]/ul/li[1]/a").click()

# get the list of TAs per course
print('TAs per course')
print()
course_with_TA=[]
i=1
while True:
    try:
        driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/section/div/aside/div/div[2]/div/div["+str(i)+"]/div[1]/h2/a").click()
        cname=driver.find_element(By.ID, "courseheader").text        
        # Go to the participants page
        driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/aside/div[1]/div[2]/ul/li/ul/li[3]/ul/li/ul/li[1]/p/a').click()
        # Select to view only the Teaching Assistants
        el_to_select=driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/section/div/div/div[1]/div/form/div/select')
        for option in el_to_select.find_elements_by_tag_name('option'):
            if (option.text == 'Teaching Assistant'):
                option.click()
                break
        # Extract only the TAs names
        j=1
        TA_list=[]
        while True:
            try:
                TA_name=driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div/section/div/div/div[5]/table/tbody/tr["+str(j)+"]/td[2]").text
                if(TA_name!=""):
                    TA_list.append(TA_name)
                j+=1
            except:
                break
        l1=[cname,TA_list]
        course_with_TA.append(l1)
        if (j!=1):
            print(cname)
            for TA in TA_list:
                print(TA)
            print()
        # go back to the dashboard
        driver.find_element(By.XPATH,"/html/body/div[3]/nav[2]/ul/li[1]/a").click()
        i+=1
    except Exception as e:
        # print (e.args)
        break

driver.quit()


# write the attendance to a file
fout=open('attendance.txt',"w")
for c in attendance:
    fout.write(c[0]+':'+c[1]+'/'+c[2]+'\n')

# write the TA details to a file
fout=open('TA.txt',"w")
for c in course_with_TA:
    fout.write(c[0]+"\n")
    for i in c[1]:
        fout.write(i+"\n")
    fout.write("\n")
    