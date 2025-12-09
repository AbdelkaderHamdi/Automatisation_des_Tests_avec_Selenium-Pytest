from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re

class InventoryPage(BasePage):
    # Locators
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BTNS = (By.CLASS_NAME, "btn_primary")
    REMOVE_FROM_CART_BTNS = (By.CLASS_NAME, "btn_secondary")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    # Titres et Prix pour validation
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_DESCRIPTIONS = (By.CLASS_NAME, "inventory_item_desc")

    def __init__(self, driver):
        super().__init__(driver)

    def ajouter_produit_au_panier(self, index=0):
        boutons = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        if index < len(boutons):
            boutons[index].click()

    def retirer_produit_du_panier(self, index=0):
        boutons = self.driver.find_elements(*self.REMOVE_FROM_CART_BTNS)
        if index < len(boutons):
            boutons[index].click()
    def obtenir_nombre_produits(self):
        """Compte combien de produits sont affichés sur la page."""
        # Note: Ici on utilise 'find_elements' (pluriel) qui retourne une liste
        produits = self.driver.find_elements(*self.INVENTORY_ITEMS)
        return len(produits)
    
    def obtenir_nombre_articles_panier(self):
        try:
            element = self.driver.find_element(*self.CART_BADGE)
            return int(element.text)
        except:
            return 0

    def aller_au_panier(self):
        self.cliquer(self.CART_ICON)

    # --- Nouvelles méthodes (Prix & Détails) ---

    def obtenir_tous_les_prix(self):
        """Retourne une liste des textes des prix (ex: ['$29.99', '$9.99'])"""
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [e.text for e in elements]

    def obtenir_prix_depuis_liste(self, index=0):
        items = self.driver.find_elements(*self.ITEM_PRICES)
        return items[index].text

    def cliquer_titre_produit(self, index=0):
        items = self.driver.find_elements(*self.ITEM_NAMES)
        items[index].click()
    