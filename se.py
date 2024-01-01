from configparser import ConfigParser
from selenium import webdriver
from time import sleep

config = ConfigParser()
config.read("config.ini")

profile = config.get("se", "profile_dir_path")
url = config.get("se", "live_url")

ops = webdriver.firefox.options.Options()
ops.add_argument("-profile")
ops.add_argument(profile)
ops.add_argument("--headless")
ff = webdriver.Firefox(options=ops)

try:
    sleep(5)
    ff.get(url)
    input()
except:
    ff.quit()
