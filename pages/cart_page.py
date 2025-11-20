from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Page du panier (Your Cart)
    Contient les articles sélectionnés et les boutons de navigation.
    """

    # --- LOCATORS (Sélecteurs) ---
    # Conteneur de tous les articles dans le panier
    CART_ITEMS_LIST = (By.CLASS_NAME, "cart_list")
    
    # Un article spécifique dans le panier
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    
    # Nom du premier article dans le panier (pour vérification)
    FIRST_ITEM_NAME = (By.CSS_SELECTOR, ".cart_item:nth-child(3) .inventory_item_name")
    
    # Bouton "Remove" (Supprimer) pour le premier article
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".cart_item:nth-child(3) button.cart_button")
    
    # Bouton de navigation "Continue Shopping"
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    
    # Bouton de navigation "Checkout"
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        super().__init__(driver)

    # --- ACTIONS (Méthodes) ---

    def obtenir_nombre_articles_panier(self):
        """Compte le nombre d'articles listés dans le panier."""
        # On utilise find_elements et on ignore le header (3 premiers éléments de la liste)
        items = self.driver.find_elements(*self.CART_ITEM)
        # Comme la liste contient aussi des headers (QTY, Description), on filtre les vrais produits
        # Sur Sauce Labs, le premier vrai produit est le 3ème élément du .cart_list
        return len(items) - 1 # Il y a toujours 1 élément de plus qui est le header

    def obtenir_nom_premier_article(self):
        """Récupère le nom du premier article pour vérification."""
        return self.attendre_element(self.FIRST_ITEM_NAME).text

    def supprimer_premier_article(self):
        """Clique sur le bouton 'Remove' du premier article."""
        self.cliquer(self.REMOVE_BUTTON)

    def cliquer_checkout(self):
        """Clique sur le bouton pour démarrer le processus de paiement."""
        self.cliquer(self.CHECKOUT_BTN)
        
    def cliquer_continue_shopping(self):
        """Clique sur le bouton pour retourner à la page d'inventaire."""
        self.cliquer(self.CONTINUE_SHOPPING_BTN)