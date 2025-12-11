from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class DriverFactory:
    @staticmethod
    def get_driver(browser_name):
        driver = None
        if browser_name.lower() == "chrome":
            options = ChromeOptions()
            options.add_argument("--headless") 
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options=options)
        elif browser_name.lower() == "firefox":
            options = FirefoxOptions()
            driver = webdriver.Firefox(options=options)
        elif browser_name.lower() == "edge":
            options = EdgeOptions()
            options.add_argument("--start-maximized")
            driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Browser '{browser_name}' is not supported.")
        
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        return driver
