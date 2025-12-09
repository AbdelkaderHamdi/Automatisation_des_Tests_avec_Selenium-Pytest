import pytest
from pages.login_page import LoginPage

# La page Login sera le point de départ pour ces tests.
TARGET_URL = "https://www.saucedemo.com/"
VALID_PASSWORD = "secret_sauce"

# Données pour les tests valides (Success) et les tests problématiques (Failure)

# (1) Test de succès: L'utilisateur est connecté et le site change d'URL.
@pytest.mark.parametrize("username", [
    "standard_user", 
    "locked_out_user"
])
@pytest.mark.functional
def test_successful_login(driver, username):
    """
    Vérifie la connexion pour les utilisateurs valides.
    (Utilise la paramétrisation pour réutiliser le même test pour 4 utilisateurs)
    """
    login_page = LoginPage(driver)
    
    # 1. Action
    login_page.charger()
    login_page.se_connecter(username, VALID_PASSWORD)
    
    # 2. Vérification (Assertion)
    # Après une connexion réussie, l'URL doit changer pour la page d'inventaire
    current_url = driver.current_url
    print(f"Connexion réussie pour {username}. Nouvelle URL: {current_url}")
    assert "inventory.html" in current_url, \
        f"L'URL n'a pas redirigé vers l'inventaire après la connexion de {username}."


# (2) Test d'échec: L'utilisateur est bloqué ou les identifiants sont faux.
@pytest.mark.parametrize("username, expected_error", [
    ("wrong_user", "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "Epic sadface: Username and password do not match any user in this service"), # Mauvais mot de passe
    ("", "Epic sadface: Username is required"), 
])
@pytest.mark.functional
@pytest.mark.boundary # Marqueur pour les tests basés sur les limites 
def test_unsuccessful_login(driver, username, expected_error):
    """
    Vérifie l'échec de connexion pour les utilisateurs bloqués, 
    les mauvais identifiants, et les champs vides.
    """
    login_page = LoginPage(driver)
    
    # On utilise un mot de passe incorrect pour le test "Mauvais mot de passe"
    password = VALID_PASSWORD if username != "standard_user" else "wrong_password" 

    # 1. Action
    login_page.charger()
    login_page.se_connecter(username, password)
       # 2. Vérification (Assertion)
       # 2. Vérification (Assertion)
    error_message = login_page.obtenir_message_erreur()
    print(f"Test d'échec pour {username}. Message d'erreur reçu: {error_message}")
    
    current_url = driver.current_url
    assert error_message == expected_error, \
        f"Le message d'erreur attendu '{expected_error}' n'a pas été trouvé."