import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.mark.state_transition
def test_successful_full_order(driver):
    """
    T-08 (State Transition Test Positif) : 
    Vérifie le flux de commande complet et la confirmation de succès.
    """
    
    # Préparation : Connexion, ajout, et aller à l'étape 1
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)
    
    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")
    inventory_page.ajouter_premier_produit_au_panier()
    inventory_page.aller_au_panier()
    cart_page.cliquer_checkout()
    
    # --- Étape 1 : Informations ---
    checkout_page.remplir_informations("Nom", "Prenom", "75001")
    checkout_page.cliquer_continuer()
    
    # --- Étape 2 : Overview / Vérification des Totaux (T-12, Performance) ---
    total = checkout_page.obtenir_total_final()
    tax = checkout_page.obtenir_taxe()
    
    # On sait que le prix du sac est 29.99$. 
    # Le site calcule : 29.99 (prix) + 2.40 (taxe) = 32.39 (total)
    print(f"Total calculé: {total} (Taxe: {tax})")
    assert total == 32.39, "Le prix total affiché n'est pas correct."

    checkout_page.cliquer_finish()
    
    # --- Étape 3 : Confirmation ---
    message_succes = checkout_page.obtenir_message_succes()
    assert message_succes == "Thank you for your order!", \
        "Le message de confirmation de commande n'est pas affiché."
    
    # Vérifier que le panier est vide (état final)
    assert inventory_page.obtenir_nombre_articles_panier() == 0, \
        "Le badge panier n'a pas été remis à zéro après la commande."