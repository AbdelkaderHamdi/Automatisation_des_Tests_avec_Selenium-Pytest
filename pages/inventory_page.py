from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """
    Page d'inventaire (Liste des produits)
    """

    # On cible tous les blocs "article" qui ont la classe 'inventory_item'
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    
    # Le titre du premier produit (ex: Sauce Labs Backpack)
    FIRST_PRODUCT_TITLE = (By.CSS_SELECTOR, ".inventory_item:nth-of-type(1) .inventory_item_name")
    
    # Le bouton "Add to cart" du premier produit
    ADD_TO_CART_BTN_1 = (By.CSS_SELECTOR, ".inventory_item:nth-of-type(1) button")
    
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

    def ajouter_premier_produit_au_panier(self):
        """Clique sur le bouton 'Add to cart' du premier produit."""
        self.cliquer(self.ADD_TO_CART_BTN_1)

    def obtenir_titre_premier_produit(self):
        """Récupère le texte du premier produit (ex: Sauce Labs Backpack)."""
        element = self.attendre_element(self.FIRST_PRODUCT_TITLE)
        return element.text

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
        self.cliquer(self.CART_ICON)