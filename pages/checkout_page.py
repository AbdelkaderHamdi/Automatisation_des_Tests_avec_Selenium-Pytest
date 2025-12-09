from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    # --- Étape 1 : Informations ---
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    # --- Étape 2 : Overview ---
    FINISH_BUTTON = (By.ID, "finish")
    INVENTORY_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SUMMARY_SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    
    # --- Étape 3 : Succès ---
    SUCCESS_HEADER = (By.CLASS_NAME, "complete-header")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def remplir_informations(self, first_name, last_name, postal_code):
        """Remplit les champs du formulaire."""
        self.ecrire_texte(self.FIRST_NAME_INPUT, first_name)
        self.ecrire_texte(self.LAST_NAME_INPUT, last_name)
        self.ecrire_texte(self.POSTAL_CODE_INPUT, postal_code)
    
    def cliquer_continuer(self):
        """Clique sur Continue."""
        self.cliquer(self.CONTINUE_BUTTON)
    
    def obtenir_message_erreur(self):
        """Récupère le message d'erreur affiché."""
        return self.attendre_element(self.ERROR_MESSAGE).text
    
    def calculer_somme_sous_total(self):
        """Calcule la somme des prix des articles."""
        elements_prix = self.driver.find_elements(*self.INVENTORY_ITEM_PRICES)
        total_calcule = 0.0
        
        for element in elements_prix:
            texte_prix = element.text.replace("$", "")
            total_calcule += float(texte_prix)
        
        # Arrondir à 2 décimales pour éviter les erreurs de précision
        return round(total_calcule, 2)
    
    def obtenir_sous_total_affiche(self):
        """Récupère le sous-total affiché."""
        text = self.attendre_element(self.SUMMARY_SUBTOTAL_LABEL).text
        return float(text.replace("Item total: $", ""))
    
    def obtenir_taxe(self):
        """Récupère la taxe affichée."""
        text = self.attendre_element(self.SUMMARY_TAX_LABEL).text
        return float(text.replace("Tax: $", ""))
    
    def obtenir_total_final(self):
        """Récupère le total final affiché."""
        text = self.attendre_element(self.SUMMARY_TOTAL_LABEL).text
        return float(text.replace("Total: $", ""))
    
    def cliquer_finish(self):
        """Clique sur Finish."""
        self.cliquer(self.FINISH_BUTTON)
    
    def obtenir_message_succes(self):
        """Récupère le message de succès."""
        return self.attendre_element(self.SUCCESS_HEADER).text