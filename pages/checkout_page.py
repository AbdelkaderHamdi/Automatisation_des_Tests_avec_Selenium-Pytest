from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    # ... (Vos locators existants pour l'étape 1) ...
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    
    # --- Étape 2 : Overview (Nouveaux Locators) ---
    FINISH_BUTTON = (By.ID, "finish")
    
    # Locator pour TOUS les prix des articles dans la liste
    INVENTORY_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    
    # Labels de résumé
    SUMMARY_SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    
    SUCCESS_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        super().__init__(driver)

    # ... (Vos méthodes existantes pour remplir info) ...

    def remplir_informations(self, first_name, last_name, postal_code):
        self.ecrire_texte(self.FIRST_NAME_INPUT, first_name)
        self.ecrire_texte(self.LAST_NAME_INPUT, last_name)
        self.ecrire_texte(self.POSTAL_CODE_INPUT, postal_code)

    def cliquer_continuer(self):
        self.cliquer(self.CONTINUE_BUTTON)

    # --- NOUVELLES MÉTHODES DE CALCUL DYNAMIQUE ---

    def calculer_somme_sous_total(self):
        """
        Récupère tous les prix des articles affichés et retourne leur somme.
        """
        elements_prix = self.driver.find_elements(*self.INVENTORY_ITEM_PRICES)
        total_calcule = 0.0
        
        for element in elements_prix:
            # Le texte est sous la forme "$29.99" -> on enlève le $
            texte_prix = element.text.replace("$", "")
            total_calcule += float(texte_prix)
            
        return total_calcule

    def obtenir_sous_total_affiche(self):
        """Récupère le sous-total affiché par le site (Item total)."""
        text = self.attendre_element(self.SUMMARY_SUBTOTAL_LABEL).text
        # Format: "Item total: $29.99"
        return float(text.replace("Item total: $", ""))

    def obtenir_taxe(self):
        """Récupère la taxe affichée."""
        text = self.attendre_element(self.SUMMARY_TAX_LABEL).text
        # Format: "Tax: $2.40"
        return float(text.replace("Tax: $", ""))

    def obtenir_total_final(self):
        """Récupère le total final affiché."""
        text = self.attendre_element(self.SUMMARY_TOTAL_LABEL).text
        # Format: "Total: $32.39"
        return float(text.replace("Total: $", ""))

    def cliquer_finish(self):
        self.cliquer(self.FINISH_BUTTON)

    def obtenir_message_succes(self):
        return self.attendre_element(self.SUCCESS_HEADER).text