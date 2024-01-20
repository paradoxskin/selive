from selenium import webdriver
from time import sleep
import config

def start_se(echo, shutdown):
    ser = webdriver.firefox.service.Service(log_output="./log/se.log", executable_path=config.driver_path)
    ops = webdriver.firefox.options.Options()
    ops.add_argument("-profile")
    ops.add_argument(config.profile_dir_path)
    ops.add_argument("--headless")

    ff = webdriver.Firefox(service=ser, options=ops)
    ff.get(config.live_url)
    echo("[+] se ok.")
    echo('[i] press "q" to quit')

    sleep(5)
    try:
        ff.find_element("tag name", "video").click()
        ff.find_element("class name", "left-area").find_element("tag name", "span").click()
        echo("[i] player stop.")
    except:
        echo("[!] player cant stop.")

    with shutdown:
        shutdown.wait()
    ff.quit()
