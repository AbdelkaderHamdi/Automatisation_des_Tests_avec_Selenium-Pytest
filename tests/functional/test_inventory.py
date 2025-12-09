import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.functional
def test_add_item_to_cart(driver):
    
    # --- 1. Préparation & Connexion ---
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")
    
    # --- 2. Vérification du nombre de produits ---
    nb_produits = inventory_page.obtenir_nombre_produits()
    print(f"Nombre de produits trouvés : {nb_produits}")
    assert nb_produits == 6, "Il devrait y avoir 6 produits affichés."
    
    # --- 3. Action : Ajout au panier ---
    inventory_page.ajouter_produit_au_panier()

    # --- 4. Vérification du panier ---
    nb_panier = inventory_page.obtenir_nombre_articles_panier()
    print(f"Articles dans le panier : {nb_panier}")
    assert nb_panier == 1, "Le panier devrait contenir 1 article."



@pytest.mark.functional
def test_remove_item_from_cart(driver):
    
    # --- 1. Préparation & Connexion ---
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    login_page.charger()
    login_page.se_connecter("problem_user", "secret_sauce")

    # --- 1.1. Action : Ajout au panier ---
    inventory_page.ajouter_produit_au_panier()

    # --- 2. Action : remove depuis panier ---
    inventory_page.retirer_produit_du_panier()

    # --- 3. Vérification du panier ---
    nb_panier = inventory_page.obtenir_nombre_articles_panier()
    print(f"Articles dans le panier : {nb_panier}")
    assert nb_panier == 0, "Le panier devrait contenir 0 article."