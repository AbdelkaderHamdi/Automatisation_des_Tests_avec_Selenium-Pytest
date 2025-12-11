import pytest
import time
from pages.login_page import LoginPage

@pytest.mark.performance
def test_login_load_time(driver):
    start_time = time.time()
    
    login_page = LoginPage(driver)
    login_page.load()
    
    end_time = time.time()
    load_time = end_time - start_time
    
    print(f"Login Page Load Time: {load_time} seconds")
    assert load_time < 2.0, "Login page took too long to load"
