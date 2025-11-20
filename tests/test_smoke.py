import pytest
from pages.base_page import BasePage

# Site cible pour le test
TARGET_URL = "https://www.saucedemo.com/"

@pytest.mark.smoke
def test_smoke_page_title(driver):
    """
    Vérifie que le site se charge et que le titre est correct.
    Le paramètre 'driver' vient automatiquement du fichier conftest.py
    """
    # 1. Préparation
    base_page = BasePage(driver)
    
    # 2. Action
    base_page.ouvrir_url(TARGET_URL)
    titre_actuel = base_page.obtenir_titre_page()
    
    # 3. Vérification (Assertion)
    assert titre_actuel == "Swag Labs", "Le titre de la page n'est pas correct."