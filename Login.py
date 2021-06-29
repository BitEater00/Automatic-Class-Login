from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from tkinter import *
from selenium.common.exceptions import WebDriverException

def openwindow(s = ""):
	options = webdriver.ChromeOptions()
	options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
	driver = webdriver.Chrome('./chromedriver' , chrome_options=options)
	driver.get(s)
	time.sleep(10)
	inputRoll = driver.find_element_by_css_selector("input.ant-input.msg-input.false")
	text = inputRoll.text
	print("The text in textbox {}".format(text))
	inputRoll.send_keys("18BCD7008_Aditya")

	checkBox = driver.find_elements_by_css_selector("input.ant-checkbox-input")
	for i in checkBox:
		text = i.text
		print("The text in checkbox {}".format(text))
		if i != checkBox[0]:
			i.click()

	inputElement = driver.find_elements_by_css_selector("div.button-large.undefined")
	for i in inputElement:
		text = i.text
		print("THe text is button{}".format(text))
		if text == "OK":
			print("Thumps up")
			i.click()
			while True:
				try:
					driver.title
				except WebDriverException:
					print("WWW")
					break

SStart = "https://meet.teamlink.co/room/"
SID = "4239791121"
SEnd = "?i=true&fbclid=IwAR2z9qFjTIJOnMSgJZNs9Kt4R2Ru-v17ZaqTfhONLeLoEb5rdBKbM-QYNaI"
s = SStart + SID + SEnd 
openwindow(s)

