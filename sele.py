from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui


def run_sele(otp):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    print("Page Title: ",driver.title)
    time.sleep(3)

    pyautogui.moveTo(1336,1042) #bring google to fronmt
    pyautogui.click()
    time.sleep(3)

    pyautogui.moveTo(1226,31) #enlarge
    pyautogui.click()
    time.sleep(2)

    search_box = driver.find_element(By.NAME,"q")
    search_box.send_keys("Nykaa")
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    pyautogui.moveTo(62,295) #captcha
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(658,559) #nykaa click
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(1517,276) #signin click
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(1457,474) #mobileno click
    pyautogui.click()
    time.sleep(5)

    login_no = driver.find_element(By.NAME,"emailMobile") #enter mobile no
    login_no.send_keys("7433045743")
    login_no.send_keys(Keys.ENTER)

    pyautogui.moveTo(664,645) #proceed click
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(1212,1045) #back vscode
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(1437,981) #vscode console click
    pyautogui.click()
    time.sleep(1)

    if otp is None:
        otp = input("Enter OTP: ")

    pyautogui.moveTo(1320,1053) #back to nykaa
    pyautogui.click()
    time.sleep(5)

    otp_verify = driver.find_element(By.NAME,"otpValue") #enter otp in nykaa
    otp_verify.send_keys(otp)
    otp_verify.send_keys(Keys.ENTER)
    time.sleep(5)

    pyautogui.moveTo(978,708) #verify click
    pyautogui.click()
    time.sleep(2)

    searchnykaa = driver.find_element(By.NAME,"search-suggestions-nykaa") #search nykaa lipstick
    searchnykaa.send_keys("Sugar Lipstick")
    searchnykaa.send_keys(Keys.ENTER)
    time.sleep(5)

    pyautogui.moveTo(1129,719) #seeproduct click
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(732,844) #wishlist click
    pyautogui.click()
    time.sleep(5)

    input("Press Enter to close...")
    driver.quit()
    
    pyautogui.moveTo(1071,1049) #back to nykaa
    pyautogui.click()
    time.sleep(5)