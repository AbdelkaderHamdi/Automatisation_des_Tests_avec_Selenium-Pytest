import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

# --- FIXTURE : Préparation commune ---
@pytest.fixture
def setup_checkout(driver):
    """
    Cette fixture s'exécute avant chaque test de ce fichier.
    Elle connecte l'utilisateur, ajoute un produit, va au panier 
    et clique sur Checkout.
    Elle retourne les pages nécessaires aux tests.
    """
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")
    inventory_page.ajouter_produit_au_panier()
    inventory_page.aller_au_panier()
    cart_page.cliquer_checkout()

    # On retourne un dictionnaire ou un tuple pour y accéder dans les tests
    return {
        "checkout": checkout_page,
        "inventory": inventory_page # Utile pour vérifier le stock à la fin
    }

# --- TEST 1 : Remplir informations et Continuer (Happy Path) ---
@pytest.mark.functional
def test_checkout_step_one_valid(driver, setup_checkout):
    """Vérifie qu'on peut passer à l'étape 2 avec des infos valides."""
    checkout_page = setup_checkout["checkout"]
    
    # Action
    checkout_page.remplir_informations("John", "Doe", "75000")
    checkout_page.cliquer_continuer()
    
    # Vérification : L'URL doit changer pour 'checkout-step-two'
    assert "checkout-step-two" in driver.current_url, \
        "La redirection vers l'étape 2 a échoué."

# --- TEST 2 : Informations manquantes (Negative Path) ---
@pytest.mark.functional
def test_checkout_step_one_missing_info(driver, setup_checkout):
    """Vérifie qu'on ne peut PAS continuer si des infos manquent."""
    checkout_page = setup_checkout["checkout"]
    
    # Action : On ne remplit que le prénom, on laisse le reste vide
    checkout_page.remplir_informations("John", "", "") 
    checkout_page.cliquer_continuer()
    
    # Vérification 1 : On est toujours sur l'étape 1
    assert "checkout-step-one" in driver.current_url
    
    # Vérification 2 : Message d'erreur affiché
    msg = checkout_page.obtenir_message_erreur()
    assert "Error: Last Name is required" in msg, \
        f"Le message d'erreur attendu n'est pas bon. Reçu: {msg}"

# --- TEST 3 : Vérification Dynamique du Total ---
@pytest.mark.functional
def test_checkout_overview_total_calculation(driver, setup_checkout):
    """Vérifie mathématiquement les totaux (Item Total + Tax = Total)."""
    checkout_page = setup_checkout["checkout"]
    
    # Pré-requis : Passer l'étape 1
    checkout_page.remplir_informations("John", "Doe", "75000")
    checkout_page.cliquer_continuer()
    
    # Récupération des valeurs
    sous_total_calcule = checkout_page.calculer_somme_sous_total()
    sous_total_affiche = checkout_page.obtenir_sous_total_affiche()
    taxe = checkout_page.obtenir_taxe()
    total_final = checkout_page.obtenir_total_final()
    
    # Vérifications Mathématiques
    assert sous_total_calcule == sous_total_affiche, "Le sous-total affiché ne correspond pas à la somme des articles."
    
    total_attendu = round(sous_total_affiche + taxe, 2)
    assert total_attendu == total_final, \
        f"Calcul incorrect : {sous_total_affiche} + {taxe} != {total_final}"

# --- TEST 4 : Succès de la commande ---
@pytest.mark.functional
def test_checkout_complete_success(driver, setup_checkout):
    """Vérifie la confirmation finale et que le panier est vidé."""
    checkout_page = setup_checkout["checkout"]
    inventory_page = setup_checkout["inventory"]
    
    # Pré-requis : Aller jusqu'à la fin
    checkout_page.remplir_informations("John", "Doe", "75000")
    checkout_page.cliquer_continuer()
    checkout_page.cliquer_finish()
    
    # Vérification 1 : Message de succès
    message = checkout_page.obtenir_message_succes()
    assert "Thank you for your order!" in message, \
        f"Message attendu non trouvé. Reçu: {message}"
    
    # Vérification 2 : URL 'checkout-complete'
    assert "checkout-complete" in driver.current_url
    
    # Vérification 3 : Le panier est vide
    # Retourner à l'inventaire et vérifier le badge
    driver.get(driver.current_url.replace("checkout-complete.html", "inventory.html"))
    assert inventory_page.obtenir_nombre_articles_panier() == 0, \
        "Le panier devrait être vide après la commande."
