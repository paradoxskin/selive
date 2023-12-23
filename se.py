import configparser
from selenium import webdriver

config = configparser.ConfigParser()
config.read("config.ini")

profile = config.get("se", "profile_dir_path")
url = config.get("se", "live_url")

ops = webdriver.firefox.options.Options()
ops.add_argument("-profile")
ops.add_argument(profile)
ff = webdriver.Firefox(options=ops)

ff.get(url)
