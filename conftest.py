import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def pytest_addoption(parser):
    """Ajoute des options de ligne de commande à pytest."""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Navigateur à utiliser : chrome, firefox, ou edge"
    )

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture Pytest pour initialiser et fermer le WebDriver.
    S'exécute une fois par fonction de test.
    """
    browser_name = request.config.getoption("browser")
    driver_instance = None

    print(f"\nInitialisation du navigateur : {browser_name}")

    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless") # Exécuter sans ouvrir de fenêtre
        #options.add_argument("--start-maximized")
        driver_instance = webdriver.Chrome(options=options)
        
    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        # options.add_argument("--headless")
        driver_instance = webdriver.Firefox(options=options)
        
    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        driver_instance = webdriver.Edge(options=options)
        
    else:
        pytest.fail(f"Navigateur '{browser_name}' non supporté.")

    driver_instance.implicitly_wait(5) # Attente implicite de 5s

    # 'yield' passe le driver au test
    yield driver_instance
    
    # Ce code s'exécute APRÈS la fin du test a cause du 'yield'
    print(f"\nFermeture du navigateur : {browser_name}")
    driver_instance.quit()