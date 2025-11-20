from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Contient les méthodes communes à toutes les pages (helpers).
    C'est la base de votre architecture POM (T-03).
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10) # 10 secondes d'attente explicite max

    def ouvrir_url(self, url):
        """Ouvre une URL donnée."""
        self.driver.get(url)

    def attendre_element(self, by_locator):
        """Attend qu'un élément soit visible."""
        return self.wait.until(EC.visibility_of_element_located(by_locator))
        
    def cliquer(self, by_locator):
        """Clique sur un élément après avoir attendu qu'il soit cliquable."""
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    def ecrire_texte(self, by_locator, texte):
        """Écrit du texte dans un champ input."""
        element = self.attendre_element(by_locator)
        element.clear()
        element.send_keys(texte)

    def obtenir_titre_page(self):
        """Retourne le titre de la page actuelle."""
        return self.driver.title