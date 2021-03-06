from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
import util


# username = "royzohar25@gmail.com"
# password = "1Qazwsxdcv"

FIRST = "https://my.arlo.com/?_ga=2.72087187.1057132506.1558461222-1738443716.1558191218#/login"

def get_url_selenium():
	username, password = util.get_creds()
	url = None
	try:
		profile = webdriver.FirefoxProfile()
		profile.set_preference("plugin.state.flash", 2)
		driver = webdriver.Firefox(profile)
		#print("There is a way to wait until an item loads, \
		#look it up and use it intead of the time.sleep() - \
		#it will shorten the waiting time and avoid errors.")
		driver.get(FIRST)
		elem = driver.find_element_by_name("userId")
		elem.send_keys(username)

		elem = driver.find_element_by_name("password")
		elem.send_keys(password)

		elem.send_keys(Keys.RETURN)

		#time.sleep(5)

		try:
			elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'cameras_play_idle_51D28573A1683')))
			elem.click()
		except TimeoutException:
			print("Loading took too much time!")

		#elem = driver.find_element_by_id("cameras_play_idle_51D28573A1683")
		#elem.click()

		time.sleep(3)

		# try:
		# 	elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'cameras_cameraSnapshot_51D28573A1683')))
		# 	elem.click()
		# except TimeoutException:
		# 	print("Loading took too much time!")


		time.sleep(20)

		elem = driver.find_element_by_id("cameras_cameraSnapshot_51D28573A1683")
		elem.click()


		# Close annoying alert on homepage that blocks library
		try:
			driver.find_element_by_xpath(
				"//div[@class='alert-body alert-body-visible']"
			).click()
		except Exception as e:
			pass

		elem = driver.find_element_by_id("footer_library")
		elem.click()

		time.sleep(5)

		try:
			elem = driver.find_element_by_id("modal_close")
			elem.click()
		except Exception as e:
			pass

		# Get image url
		url = driver.find_element_by_xpath(
			"//div[@id='day_record_0']//a//img"
		).get_attribute("src")

		# Try and delete prev image
		try:
			driver.find_element_by_xpath(
				"//div[@id='day_record_1']//div[@class='timeline-record-footer']//div[@class='timeline-record-more arlo-cp']"
			).click()

			driver.find_element_by_xpath(
				"//div[@class='timeline-action arlo-link'][5]"
			).click()

			driver.find_element_by_xpath(
				"//button[@id='buttonConfirm']"
			).click()
		except Exception as e:
			pass
			# print("Failed deleting previous image: ", e)

	except Exception as e:
		pass
		# print(e)
	finally:
		driver.close()
		driver.quit()

	return url
