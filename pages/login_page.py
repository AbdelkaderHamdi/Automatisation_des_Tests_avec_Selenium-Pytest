from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    Sélecteurs et méthodes spécifiques à la page de Login.
    (Exemple pour SauceDemo)
    """

    # Sélecteurs (Locators)
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"

    def charger(self):
        """Ouvre la page de login."""
        self.ouvrir_url(self.url)

    def se_connecter(self, username, password):
        """Exécute une tentative de connexion."""
        self.ecrire_texte(self.USERNAME_INPUT, username)
        self.ecrire_texte(self.PASSWORD_INPUT, password)
        self.cliquer(self.LOGIN_BUTTON)

    def obtenir_message_erreur(self):
        """Récupère le texte du message d'erreur."""
        return self.attendre_element(self.ERROR_MESSAGE).text