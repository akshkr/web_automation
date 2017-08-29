from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import urllib3
import urllib3.request
import sys
import time
import certifi

"""READ THIS.
This file uses selenium to download images in their original size from google images search
"""

"""Google working requires the following line to authenticate the service"""
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

""" adding path to geckodriver to the OS environment variable. Download path is set further."""
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"

"""The following function takes 'the text to be searched' and 'maximum number of images to be saved' as arguments"""

def mai(searchtext, num_requested):
	#searchtext = sys.argv[1]
	#num_requested = int(sys.argv[2])
	number_of_scrolls = int(num_requested / 400 + 1)
	
	#If the download directory doesn't exists, the following command makes the path
	if not os.path.exists(download_path + searchtext.replace(" ", "_")):
		os.makedirs(download_path + searchtext.replace(" ", "_"))

	#The following lines prepare the actual format of the google search
	url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
	driver = webdriver.Firefox()
	driver.get(url)

	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
	extensions = {"jpg", "jpeg", "png", "gif"}
	img_count = 0
	downloaded_img_count = 0
	
	for _ in range(number_of_scrolls):
		for __ in range(10):
			# multiple scrolls needed to show all 400 images
			driver.execute_script("window.scrollBy(0, 1000000)")
			time.sleep(0.2)
		# to load next 400 images
		time.sleep(0.5)
		try:
			driver.find_element_by_xpath("//input[@value='Show more results']").click()
		except Exception as e:
			print("Less images found:", e)
			break

	imges = driver.find_elements_by_xpath("//div[@class='rg_meta']")
	print("Total images:", len(imges), "\n")
	for img in imges:
		img_count += 1
		img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
		img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
		#print("Downloading image", img_count, ": ", img_url)
		try:
			if img_type not in extensions:
				img_type = "jpg"
			response1 = http.request('GET', img_url)
			if sys.getsizeof(response1.data) > 120000:
				f = open(download_path+searchtext.replace(" ", "_")+"/"+str(downloaded_img_count)+"."+img_type, "wb")
				f.write(response1.data)
				f.close
				downloaded_img_count += 1
		except Exception as e:
			#print("Download failed:", e)
			pass
		if downloaded_img_count >= num_requested:
			break

	print("Total downloaded: ", downloaded_img_count, "/", img_count)
	driver.quit()

if __name__ == "__main__":
	main()
