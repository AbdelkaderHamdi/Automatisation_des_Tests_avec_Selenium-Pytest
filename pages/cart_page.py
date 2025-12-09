from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    # --- LOCATORS ---
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    
    # Note : Utiliser des sélecteurs relatifs est souvent plus robuste que nth-child
    # Pour le premier article, on prend simplement le premier élément trouvé par CSS
    FIRST_ITEM_NAME = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")

    DETAILED_PAGE_ITEM_NAME = (By.CSS_SELECTOR, ".inventory_details_name")

    REMOVE_BUTTON = (By.CSS_SELECTOR, ".cart_item button.cart_button")
    
    CHECKOUT_BTN = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")

    def __init__(self, driver):
        super().__init__(driver)

    # --- ACTIONS ---

    def obtenir_nombre_articles_panier(self):
        """Compte le nombre d'articles listés dans le panier."""
        # CORRECTION ICI : On ne fait pas -1.
        # La classe "cart_item" n'est présente que sur les vrais produits.
        items = self.driver.find_elements(*self.CART_ITEM)
        return len(items)

    def obtenir_nom_premier_article(self):
        """Récupère le nom du premier article pour vérification."""
        # On attend que l'élément soit visible avant de lire le texte
        return self.attendre_element(self.FIRST_ITEM_NAME).text
    
    def obtenir_nom_article_depuis_page_produit(self):
        """Récupère le nom du premier article pour vérification."""
        # On attend que l'élément soit visible avant de lire le texte
        return self.attendre_element(self.DETAILED_PAGE_ITEM_NAME).text
    
    def entrer_premier_article(self):
        """entrer au premier article pour vérification."""
        # On attend que l'élément soit visible avant de lire le texte
        return self.cliquer(self.FIRST_ITEM_NAME)

    def supprimer_premier_article(self):
        """Clique sur le bouton 'Remove' du premier article."""
        self.cliquer(self.REMOVE_BUTTON)

    def cliquer_checkout(self):
        self.cliquer(self.CHECKOUT_BTN)

    def cliquer_continue_shopping(self):
        self.cliquer(self.CONTINUE_SHOPPING_BTN)