import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.mark.functional
def test_remove_item_from_cart(driver):
    """
    Scénario Négatif (T-08) : S'assurer qu'on peut supprimer un article.
    1. Se connecter.
    2. Ajouter l'article 'Sauce Labs Backpack'.
    3. Aller au panier.
    4. Vérifier que l'article est présent (1 article).
    5. Supprimer l'article.
    6. Vérifier que le panier est vide (0 article).
    """
    
    # 1. Initialisation des pages
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    # Connexion et ajout d'un article
    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")
    inventory_page.ajouter_produit_au_panier()
    
    # Aller au panier (via l'icône)
    inventory_page.aller_au_panier()
    
    # --- 4. Vérification avant suppression ---
    articles_avant = cart_page.obtenir_nombre_articles_panier()
    nom_article = cart_page.obtenir_nom_premier_article()
    
    assert articles_avant == 1, "Le panier devrait commencer avec 1 article."
    assert nom_article == "Sauce Labs Backpack", "Le mauvais article est dans le panier."
    
    # --- 5. Action : Suppression ---
    cart_page.supprimer_premier_article()
    
    # --- 6. Vérification après suppression ---
    articles_apres = cart_page.obtenir_nombre_articles_panier()
    assert articles_apres == 0, "Le panier devrait être vide après la suppression."

@pytest.mark.functional
def test_proceed_to_checkout(driver):
    """
    Scénario Positif (T-08) : S'assurer qu'on peut aller à l'étape suivante.
    """
    # ... (code de connexion et ajout d'article identique) ...
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")
    inventory_page.ajouter_produit_au_panier()
    inventory_page.aller_au_panier()
    
    # Action
    cart_page.cliquer_checkout()
    
    # Vérification : on vérifie que l'URL a changé et contient 'checkout-step-one'
    assert "checkout-step-one" in driver.current_url, "Échec de la redirection vers la page de commande."


@pytest.mark.functional
def test_proceed_to_continue_shopping(driver):
    """
    Scénario Positif : S'assurer qu'on peut aller à l'étape precedante.
    """
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")
    inventory_page.ajouter_produit_au_panier()
    inventory_page.aller_au_panier()
    
    # Action
    cart_page.cliquer_continue_shopping()
    
    # Vérification : on vérifie que l'URL a changé et contient 'checkout-step-one'
    assert "inventory" in driver.current_url, "Échec de la redirection vers la page de commande."


@pytest.mark.functional
def test_proceed_to_enter_first_article(driver):
    """
    Vérifie qu'on peut accéder à la page produit depuis le panier.
    """
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    login_page.charger()
    login_page.se_connecter("problem_user", "secret_sauce")
    inventory_page.ajouter_produit_au_panier()
    inventory_page.aller_au_panier()
    
    # Récupérer le nom AVANT de cliquer
    nom_dans_panier = cart_page.obtenir_nom_premier_article()
    
    # Cliquer pour entrer dans la page produit
    cart_page.entrer_premier_article()
    
    # Récupérer le nom APRÈS navigation
    nom_dans_details = cart_page.obtenir_nom_article_depuis_page_produit()
    
    # Comparer
    assert nom_dans_panier == nom_dans_details, f"Noms différents: '{nom_dans_panier}' != '{nom_dans_details}'"

@pytest.mark.functional
def test_add_to_cart_restricted_for_guest(driver):
    """
    Vérifier que l'ajout au panier est restreint pour un utilisateur non connecté.
    1. Un utilisateur n'est PAS connecté au système.
    2. (Optionnel) L'utilisateur essaie d'accéder directement à `/inventory.html`.
    """

    # 1. Initialisation des pages
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # 2. Tenter d'accéder à la page `/inventory.html`
    driver.get("https://www.saucedemo.com/inventory.html")

    # 3. Attendre que l'URL soit redirigée
    WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))

    # 4. Vérification : Redirection vers la page de connexion ou base URL
    assert driver.current_url == "https://www.saucedemo.com/", "L'utilisateur n'a pas été redirigé vers la page de connexion."

    # 5. Si la page est accessible, tenter d'ajouter un produit au panier
    if "/inventory" in driver.current_url:
        inventory_page.ajouter_produit_au_panier()

        # Vérifier que le compteur du panier ne s'incrémente pas
        compteur_panier = inventory_page.obtenir_nombre_articles_panier()
        assert compteur_panier == 0, "Le compteur du panier ne devrait pas s'incrémenter pour un utilisateur non connecté."

        # Vérifier qu'aucun produit n'est ajouté au panier
        assert driver.current_url == "https://www.saucedemo.com/", "L'utilisateur n'a pas été redirigé vers la page de connexion après la tentative d'ajout."



@pytest.mark.functional
def test_add_all_products_to_cart(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")

    # Attendre que les produits soient chargés
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(inventory_page.INVENTORY_ITEMS))

    # Compter les produits
    nombre_produits = inventory_page.obtenir_nombre_produits()
    
    # Action : Ajouter TOUS les produits
    inventory_page.ajouter_tous_les_produits()
    
    # Petite attente explicite pour laisser le badge se mettre à jour
    time.sleep(2) 

    # Vérification
    compteur_final = inventory_page.obtenir_nombre_articles_panier()
    assert compteur_final == nombre_produits, f"Attendu: {nombre_produits}, Obtenu: {compteur_final}"