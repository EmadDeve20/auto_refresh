from typing import List
from selenium import webdriver

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

def print_list(array_list: List[str]):

    for (index, item) in enumerate(array_list):
        print(f"{index+1}- {item}") 

if __name__ == "__main__":

    webderive_gen = WebdriverGenerator()

    borwsers = ["chrom", "firefox", "ie"]

    print("Select Your Browser:")
    print_list(borwsers)

    browser = borwsers[int(input()) - 1]

    try:
        web_driver =  webderive_gen.generate_driver(browser)
    except Exception as e:
        print(e)
        exit(1)

    web_driver.close()

