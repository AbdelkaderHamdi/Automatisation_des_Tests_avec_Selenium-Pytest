import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage

def test_verify_detail_price_consistency(driver):
    """Vérifie que le prix de la liste == prix du détail."""
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    detail_page = ProductDetailPage(driver)
    
    login_page.charger()
    login_page.se_connecter("standard_user", "secret_sauce")
    
    # Prix liste
    prix_liste = inventory_page.obtenir_prix_depuis_liste(0)
    
    # Entrer dans le détail
    inventory_page.cliquer_titre_produit(0)
    
    # Prix détail
    prix_detail = detail_page.obtenir_prix_produit()
    
    assert prix_liste == prix_detail
    detail_page.cliquer_retour_aux_produits()

@pytest.mark.functional
def test_check_specific_product_price_format(driver):
    """
    Vérifie le format du prix pour UN SEUL produit donné sur la page de détails.
    """
    # --- CONFIGURATION ---
  
    
    # --- 1. Initialisation ---
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    detail_page = ProductDetailPage(driver)
    
    # Connexion
    login_page.charger()
    # Note : Si vous mettez "problem_user", le test échouera peut-être 
    # si le produit ciblé est celui qui est buggé.
    login_page.se_connecter("problem_user", "secret_sauce")

    # On utilise la nouvelle méthode qui cherche par index
    inventory_page.cliquer_titre_produit(3)
    
    # --- 3. Vérification sur la page de détail ---
    prix_affiche = detail_page.obtenir_prix_produit()
    nom_produit = detail_page.obtenir_nom_produit()
    print(f"Prix récupéré pour {nom_produit} : {prix_affiche}")
    
    # Validation stricte via Regex (rejette les bugs type $√-1)
    est_valide = detail_page.est_un_prix_valide(prix_affiche)
    
    assert est_valide, \
        f"ALERTE : Le prix du produit '{nom_produit}' est invalide ! Trouvé : '{prix_affiche}'"

    print("Succès : Le format du prix est correct.")