from configparser import ConfigParser
from selenium import webdriver
from time import sleep

def start_se(echo, shutdown):
    config = ConfigParser()
    config.read("config.ini")

    profile = config.get("se", "profile_dir_path")
    url = config.get("se", "live_url")

    ser = webdriver.firefox.service.Service(log_output="./log/se.log")

    ops = webdriver.firefox.options.Options()
    ops.add_argument("-profile")
    ops.add_argument(profile)
    ops.add_argument("--headless")

    ff = webdriver.Firefox(service=ser, options=ops)
    ff.get(url)
    echo("[+] se ok.")
    echo('[i] press "q" to quit')

    sleep(5)
    ff.find_element("tag name", "video").click()
    ff.find_element("class name", "left-area").find_element("tag name", "span").click()

    with shutdown:
        shutdown.wait()
    ff.quit()
