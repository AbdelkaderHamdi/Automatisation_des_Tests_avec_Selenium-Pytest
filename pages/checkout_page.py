from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """
    Gère l'intégralité du flux de commande (3 étapes).
    """

    # --- Étape 1 : Your Information ---
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    # --- Étape 2 : Overview ---
    FINISH_BUTTON = (By.ID, "finish")
    TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")
    TAX_PRICE = (By.CLASS_NAME, "summary_tax_label")
    CANCEL_BUTTON = (By.ID, "cancel")

    # --- Étape 3 : Complete! ---
    SUCCESS_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")


    def __init__(self, driver):
        super().__init__(driver)

    # --- Méthodes communes pour l'étape 1 ---
    
    def remplir_informations(self, first_name, last_name, postal_code):
        """Remplit le formulaire d'information client (Étape 1)."""
        self.ecrire_texte(self.FIRST_NAME_INPUT, first_name)
        self.ecrire_texte(self.LAST_NAME_INPUT, last_name)
        self.ecrire_texte(self.POSTAL_CODE_INPUT, postal_code)

    def cliquer_continuer(self):
        """Passe à l'étape 2 (Overview)."""
        self.cliquer(self.CONTINUE_BUTTON)

    def obtenir_message_erreur(self):
        """Récupère le message d'erreur de validation du formulaire."""
        return self.attendre_element(self.ERROR_MESSAGE).text

    # --- Méthodes communes pour l'étape 2 ---
    
    def obtenir_total_final(self):
        """Récupère le prix total final de la commande."""
        text = self.attendre_element(self.TOTAL_PRICE).text
        # Exemple: 'Total: $32.39' -> retourne 32.39 (conversion en nombre)
        return float(text.replace('Total: $', ''))

    def obtenir_taxe(self):
        """Récupère le montant de la taxe."""
        text = self.attendre_element(self.TAX_PRICE).text
        # Exemple: 'Tax: $2.40' -> retourne 2.40
        return float(text.replace('Tax: $', ''))

    def cliquer_finish(self):
        """Termine la commande et passe à l'étape 3."""
        self.cliquer(self.FINISH_BUTTON)
        
    # --- Méthodes communes pour l'étape 3 ---
    
    def obtenir_message_succes(self):
        """Vérifie le message de confirmation de commande."""
        return self.attendre_element(self.SUCCESS_HEADER).text