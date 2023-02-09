from typing import List
from selenium import webdriver
import time

class WebdriverGenerator:

    drivers = {
        "chrom": webdriver.Chrome,
        "firefox": webdriver.Firefox,
        "ie": webdriver.Ie,
    }

    def generate_driver(self, browser: str) -> webdriver:

        web_driver = webdriver

        if browser in self.drivers:
            web_driver = self.drivers[browser]()
        
        else:
            raise Exception("Browser Not Valid!")
        
        return web_driver

class WebRefresher:
    
    def __init__(self, driver: webdriver, url: str, period: int):
        self.driver = driver
        
        try:
            self.driver.get(url)
        except:
            print("Url not Valid!")
            exit(1)
        
        self.period = period
        self.run()

    def run(self):
        while True:
            self.driver.refresh()
            time.sleep(self.period)



def print_list(array_list: List[str]):

    for (index, item) in enumerate(array_list):
        print(f"{index+1}- {item}") 

if __name__ == "__main__":

    webderive_gen = WebdriverGenerator()

    borwsers = ["chrom", "firefox", "ie"]

    url = input("Enter Your URL: ")

    print("Select Your Browser:")
    print_list(borwsers)

    browser = int(input())-1

    if (browser > 3 or browser < 0):
        print("Browser Select Fault!")
        exit(1)
    else:
        browser = borwsers[browser]



    time_to_refresh_period = int(input("enter period time to refresh: "))

    try:
        web_driver =  webderive_gen.generate_driver(browser)
    except Exception as e:
        print(e)
        exit(1)

    try:
        refresher = WebRefresher(web_driver, url,  time_to_refresh_period)
    except KeyboardInterrupt:
        web_driver.close()

