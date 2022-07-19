from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


option = webdriver.ChromeOptions()
# option.add_argument("--headless")
option.add_experimental_option("debuggerAddress","127.0.0.1:9014")

driverService = Service(r'C:\Program Files (x86)\chromedriver.exe')

driver = webdriver.Chrome(service = driverService, options=option)
print()

# wait for download to start
def waitDownloadStart():
    sec = 30
    paperProgress = None
    while True:
        time.sleep(1)
        try:
            paperProgress = driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('downloads-item').shadowRoot.querySelector('paper-progress')")
        except:
            print(end='')
        # print(paperProgress)
        if paperProgress != None :
            return True
        sec -= 1
        if sec <= 0 :
            return False

# track down the download progress
def trackDownload():
    downloadProgress = None
    description = None
    statusLable = None
    while True:
        try:
            downloadProgress = driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('downloads-item').shadowRoot.querySelector('paper-progress').getAttribute('value');")
            description = driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('downloads-item').shadowRoot.getElementById('description').innerText;")
            statusLable = driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('downloads-item').shadowRoot.getElementById('tag').innerText;")
        except:
            print(end='')
        if str(statusLable) == 'Failed' in str(statusLable):
            print('\nDownload',statusLable)
            return False
        if '\n' not in str(description):
            print('Download Progress: '+downloadProgress+' % ( '+str(description)+' )   ',end="\r")
        else:
            print('Download Progress: '+downloadProgress+' %   ',end="\r")
        if downloadProgress == '100':
            print('\nDownload Complete')
            return True
    

def clickDownload(num):
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, r'//*[@id=":4"]/div/c-wiz/div[2]/c-wiz/div[1]/c-wiz/div/c-wiz/div[1]/c-wiz/c-wiz/div/c-wiz['+str(num)+r']/div/div').click()
        driver.find_element(By.XPATH, r'//*[@id=":4"]/div/c-wiz/div[2]/c-wiz/div[1]/c-wiz/div/c-wiz/div[1]/c-wiz/c-wiz/div/c-wiz['+str(num)+r']/div/div').send_keys(Keys.ENTER)
        time.sleep(1)

        # code to click the download button
        for element in driver.find_elements(By.CLASS_NAME,r'a-b-Da-d'):
            # print(element.get_dom_attribute('aria-label'),element.get_dom_attribute('role'))
            if element.get_dom_attribute('aria-label') == 'Download' and element.get_dom_attribute('role') == 'button':
                element.click()
                break
        scanComplete = False # imp
        #code to click "download anyway"(need atleast 1s to load)
        print('Scanning for virus...')
        while scanComplete == False :
            try:
                driver.find_element(By.NAME,'ok').click()
                scanComplete = True
            except:
                scanComplete = False
        print('Download started')
        #code to click Close
        for element in driver.find_elements(By.CLASS_NAME,r'a-b-Da-d'):
            # print(element.get_dom_attribute('aria-label'),element.get_dom_attribute('role'))
            if element.get_dom_attribute('aria-label') == 'Close' and element.get_dom_attribute('role') == 'button':
                element.click()
                break
    except Exception as e:
        print(e)

# The main code
handles = driver.window_handles

start = int(input('Enter the number of starting file : '))
end = int(input('Enter the number of ending file : '))

for i in range(start, end+1):
    driver.switch_to.window(handles[0])
    hrefValue = None
    mainTab = 0
    downTab = 0
    try:
        hrefValue = driver.find_element(By.TAG_NAME, 'base').get_dom_attribute('href')
    except:
        print(end="")

    if hrefValue == 'chrome://downloads':
        downTab = 0
        mainTab = 1 
    else:
        mainTab = 0
        downTab = 1
    result = False
    print(i)
    while result == False :
        driver.switch_to.window(handles[mainTab])
        time.sleep(2)
        clickDownload(i)
        driver.switch_to.window(handles[downTab])
        driver.refresh()
        if waitDownloadStart():
            result = trackDownload()

