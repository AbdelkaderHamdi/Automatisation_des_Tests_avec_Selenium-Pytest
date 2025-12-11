import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.mark.responsive
def test_mobile_layout():
    mobile_emulation = { "deviceName": "iPhone X" }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://www.saucedemo.com/")
        # Check if a specific mobile element is visible or layout is correct
        # For this example, we just check title, but in real world we check hamburger menu etc.
        assert "Swag Labs" in driver.title
    finally:
        driver.quit()
