from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re

class ProductDetailPage(BasePage):
    """
    Page de détail d'un produit spécifique.
    """
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_details_price")
    BACK_TO_PRODUCTS_BTN = (By.ID, "back-to-products")

    def __init__(self, driver):
        super().__init__(driver)

    def obtenir_nom_produit(self):
        return self.attendre_element(self.PRODUCT_NAME).text

    def obtenir_prix_produit(self):
        """Récupère le prix affiché (ex: '$29.99')."""
        return self.attendre_element(self.PRODUCT_PRICE).text

    def cliquer_retour_aux_produits(self):
        """Clique sur le bouton 'Back to products'."""
        self.cliquer(self.BACK_TO_PRODUCTS_BTN)

    def est_un_prix_valide(self, texte_prix):
        """
        Valide si le prix respecte le format strict $XX.XX
        Retourne False si le texte est '$√-1' ou autre anomalie.
        """
        # Regex : Commence par $, suivi de chiffres, un point, et 2 décimales.
        pattern = r"^\$\d+\.\d{2}$"
        return bool(re.match(pattern, texte_prix))