from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """
    Page d'inventaire (Liste des produits)
    """

    # On cible tous les blocs "article" qui ont la classe 'inventory_item'
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
        
    # Le bouton "Add to cart" du premier produit
    ADD_TO_CART_BTNS = (By.CLASS_NAME, "btn_primary")
    REMOVE_FROM_CART_BTNS = (By.CLASS_NAME, "btn_secondary")
    
    # Le bouton du panier en haut à droite
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    
    # Le petit badge rouge qui compte les articles (n'existe que si panier > 0)
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        super().__init__(driver)
        # Pas d'URL ici car on y accède souvent après le login, pas directement

    def obtenir_nombre_produits(self):
        """Compte combien de produits sont affichés sur la page."""
        # Note: Ici on utilise 'find_elements' (pluriel) qui retourne une liste
        produits = self.driver.find_elements(*self.INVENTORY_ITEMS)
        return len(produits)

    def ajouter_produit_au_panier(self, index=0):
        """Clique sur le bouton 'Add to cart' d'un produit spécifique.
        """
        boutons = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        if index < len(boutons):
            boutons[index].click()

    def retirer_produit_du_panier(self, index=0):
        """Clique sur le bouton 'Remove' d'un produit spécifique.
        """
        boutons = self.driver.find_elements(*self.REMOVE_FROM_CART_BTNS)
        if index < len(boutons):
            boutons[index].click()

    def obtenir_nombre_articles_panier(self):
        """Récupère le chiffre affiché sur le panier (Badge rouge)."""
        try:
            # On essaie de trouver le badge
            element = self.attendre_element(self.CART_BADGE)
            return int(element.text)
        except:
            # Si le badge n'existe pas (panier vide), on retourne 0
            return 0

    def aller_au_panier(self):
        """Clique sur l'icône du panier."""
        self.cliquer(*self.CART_ICON)