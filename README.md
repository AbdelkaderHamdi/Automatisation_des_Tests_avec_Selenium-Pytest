# Projet de Test Automatisé - Sauce Demo (Selenium + Python)

Ce projet implémente une **suite de tests automatisés complète** pour le site [SauceDemo](https://www.saucedemo.com/) en utilisant **Selenium**, **pytest** et le **Page Object Model (POM)**.

---

## 📋 Table des Matières

- [Aperçu du Projet](#aperçu-du-projet)
- [Architecture](#architecture)
- [Installation](#installation)
- [Structure du Projet](#structure-du-projet)
- [Exécution des Tests](#exécution-des-tests)
- [Composants Principaux](#composants-principaux)
- [Fonctionnalités](#fonctionnalités)

---

## 🎯 Aperçu du Projet

Ce projet automatise les tests fonctionnels, de performance et de responsivité pour une application web e-commerce (SauceDemo). Il utilise :

- **Selenium WebDriver** : Automatisation des navigateurs
- **pytest** : Framework de test puissant et flexible
- **Page Object Model (POM)** : Maintenance du code et réutilisabilité
- **Google Generative AI (Gemini)** : Génération assistée par IA de cas de test
- **pytest-html** : Rapports de test HTML détaillés

### Cas de Test Couverts

- ✅ **Authentification** : Connexion valide/invalide, champs vides, utilisateurs spéciaux
- ✅ **Gestion du Panier** : Ajout, suppression, navigation
- ✅ **Processus de Paiement** : Validation des informations, calcul des totaux, confirmation
- ✅ **Détails des Produits** : Validation des prix, navigation, format des données
- ✅ **Performance** : Temps de chargement des pages
- ✅ **Responsivité Mobile** : Test sur appareils mobiles (émulation iPhone X)

---

## 🏗️ Architecture

Le projet suit le **Page Object Model (POM)**, un pattern de conception qui :

1. **Encapsule les sélecteurs** : Chaque page a sa propre classe avec des locators
2. **Réutilise les méthodes communes** : La classe `BasePage` fournit les helpers
3. **Facilite la maintenance** : Les changements d'IU sont localisés dans les page objects
4. **Améliore la lisibilité** : Les tests décrivent des actions métier, pas du code Selenium

### Diagramme des Dépendances

```
conftest.py (fixture driver)
    ↓
tests/
    ├── functional/
    │   ├── test_login.py        → LoginPage
    │   ├── test_inventory.py    → InventoryPage
    │   ├── test_cart.py         → CartPage
    │   ├── test_checkout.py     → CheckoutPage
    │   └── test_products.py     → ProductDetailPage
    ├── performance/
    │   └── test_load_times.py
    └── responsive/
        └── test_mobile_view.py

pages/
    ├── base_page.py             (méthodes communes)
    ├── login_page.py
    ├── inventory_page.py
    ├── cart_page.py
    ├── checkout_page.py
    └── product_detail_page.py

utils/
    ├── driver_factory.py        (création du WebDriver)
    └── excel_reader.py          (lecture de données Excel)

ai_gen/
    ├── generate_tests.py        (génération IA)
    └── prompt_templates.txt
```

---

## 💻 Installation

### Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **Navigateurs** : Chrome, Firefox ou Edge installés localement

### Étapes

1. **Clonez le projet** :
   ```bash
   git clone <repository-url>
   cd Projet_Test_Logiciel
   ```

2. **Créez un environnement virtuel** :
   ```bash
   python -m venv venv
   # Sur Windows
   venv\Scripts\activate
   # Sur macOS/Linux
   source venv/bin/activate
   ```

3. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Téléchargez les WebDrivers** (optionnel si déjà dans PATH) :
   - [ChromeDriver](https://chromedriver.chromium.org/)
   - [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
   - [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

   Placez-les dans le `PATH` système ou à la racine du projet.

5. **Configurez les variables d'environnement** (pour IA) :
   ```bash
   # Créez un fichier .env à la racine
   GEMINI_API_KEY=votre_clé_api_google
   OPENROUTER_API_KEY=votre_clé_api_openrouter
   ```

---

## 📁 Structure du Projet

```
Projet_Test_Logiciel/
├── conftest.py                      # Configuration pytest et fixture driver
├── pytest.ini                       # Marqueurs pytest
├── requirements.txt                 # Dépendances Python
├── README.md                        # Ce fichier
│
├── pages/                           # Page Object Model
│   ├── __init__.py
│   ├── base_page.py                # Classe de base avec méthodes communes
│   ├── login_page.py               # Sélecteurs et actions de login
│   ├── inventory_page.py           # Sélecteurs et actions de la liste produits
│   ├── cart_page.py                # Sélecteurs et actions du panier
│   ├── checkout_page.py            # Sélecteurs et actions du paiement
│   └── product_detail_page.py      # Sélecteurs et actions détail produit
│
├── tests/                           # Suite de tests
│   ├── functional/                 # Tests fonctionnels
│   │   ├── __init__.py
│   │   ├── test_login.py           # Tests authentification (7 cas)
│   │   ├── test_inventory.py       # Tests liste produits (2 cas)
│   │   ├── test_cart.py            # Tests panier (4 cas)
│   │   ├── test_checkout.py        # Tests paiement (4 cas)
│   │   └── test_products.py        # Tests détails produit (2 cas)
│   ├── performance/
│   │   └── test_load_times.py      # Tests performance (1 cas)
│   └── responsive/
│       └── test_mobile_view.py     # Tests mobile (1 cas)
│
├── utils/                           # Utilitaires
│   ├── driver_factory.py           # Factory pour créer les drivers
│   └── excel_reader.py             # Lecteur de données Excel
│
└── ai_gen/                          # Génération IA de cas de test
    ├── generate_tests.py           # Script principal IA
    ├── prompt_templates.txt        # Templates de prompts
    └── generated_cases.md          # Cas générés par IA
```

---

## 🧪 Exécution des Tests

### Configuration Pytest

Le fichier `pytest.ini` définit les marqueurs disponibles :
- `@pytest.mark.functional` : Tests des fonctionnalités principales
- `@pytest.mark.boundary` : Tests des cas limites et erreurs
- `@pytest.mark.performance` : Tests de performance
- `@pytest.mark.responsive` : Tests de responsivité

### Exécuter Tous les Tests

```bash
# Avec navigateur Chrome (défaut)
pytest

# Avec Firefox
pytest --browser=firefox

# Avec Edge
pytest --browser=edge
```

### Exécuter par Type de Test

```bash
# Uniquement les tests fonctionnels
pytest -m functional

# Uniquement les tests des limites
pytest -m boundary

# Uniquement les tests de performance
pytest -m performance

# Uniquement les tests responsivité
pytest -m responsive
```

### Exécuter un Fichier Spécifique

```bash
# Tests de login uniquement
pytest tests/functional/test_login.py

# Tests du panier uniquement
pytest tests/functional/test_cart.py -v
```

### Options Avancées

```bash
# Mode verbeux (affiche plus de détails)
pytest -v

# Arrêter au premier échec
pytest -x

# Afficher les print() pendant l'exécution
pytest -s

# Générer un rapport HTML
pytest --html=report.html --self-contained-html

# Exécution parallèle (rapide)
pytest -n auto
```

### Exemple Complet

```bash
pytest tests/functional/test_login.py -m functional --browser=chrome -v --html=report.html -s
```

---

## 🔧 Composants Principaux

### 1. **Base Page** (`pages/base_page.py`)

Classe mère contenant les méthodes communes à toutes les pages :

```python
- ouvrir_url(url)              # Ouvre une URL
- attendre_element(by_locator) # Attend qu'un élément soit visible
- cliquer(by_locator)          # Clique sur un élément cliquable
- ecrire_texte(by_locator, texte) # Écrit du texte dans un input
```

### 2. **Login Page** (`pages/login_page.py`)

Gère l'authentification :
- Sélecteurs : Username, Password, Login Button, Error Message
- Méthodes : `charger()`, `se_connecter(username, password)`, `obtenir_message_erreur()`

**Tests associés** :
- ✅ Connexion réussie pour utilisateurs valides
- ❌ Connexion échouée pour identifiants invalides
- ⚠️ Champs requis vides

### 3. **Inventory Page** (`pages/inventory_page.py`)

Gère la liste des produits :
- Sélecteurs : Items, Buttons Add/Remove, Cart Icon, Prices
- Méthodes : `ajouter_produit_au_panier()`, `retirer_produit_du_panier()`, `obtenir_nombre_articles_panier()`, `obtenir_tous_les_prix()`

**Tests associés** :
- ✅ Ajout de produit au panier
- ✅ Suppression de produit du panier
- 📊 Récupération des prix

### 4. **Cart Page** (`pages/cart_page.py`)

Gère le panier d'achat :
- Sélecteurs : Items du panier, Boutons Remove/Checkout/Continue
- Méthodes : `obtenir_nombre_articles_panier()`, `supprimer_premier_article()`, `cliquer_checkout()`

**Tests associés** :
- ✅ Suppression d'article
- ✅ Navigation vers checkout
- ✅ Retour au catalogue

### 5. **Checkout Page** (`pages/checkout_page.py`)

Gère le processus de paiement en trois étapes :
- **Étape 1** : Remplissage informations (Nom, Prénom, Code Postal)
- **Étape 2** : Aperçu et calcul automatique des totaux
- **Étape 3** : Confirmation et message de succès

Méthodes :
- `remplir_informations(first_name, last_name, postal_code)`
- `calculer_somme_sous_total()` (validation mathématique)
- `obtenir_sous_total_affiche()`, `obtenir_taxe()`, `obtenir_total_final()`
- `cliquer_finish()`

**Tests associés** :
- ✅ Paiement avec infos valides
- ❌ Paiement avec infos manquantes
- 🔢 Validation des calculs de totaux
- ✅ Succès de la commande

### 6. **Product Detail Page** (`pages/product_detail_page.py`)

Gère les détails d'un produit :
- Sélecteurs : Product Name, Price, Back Button
- Méthodes : `obtenir_nom_produit()`, `obtenir_prix_produit()`, `est_un_prix_valide(texte)`

**Tests associés** :
- 💰 Cohérence des prix (liste vs détail)
- 🔍 Validation du format des prix (ex: éviter les bugs "$√-1")

### 7. **Driver Factory** (`utils/driver_factory.py`)

Factory pattern pour initialiser les WebDrivers :
- Support Chrome (headless), Firefox, Edge
- Configuration commune : timeouts implicites (10s), timeouts page (30s)

### 8. **Excel Reader** (`utils/excel_reader.py`)

Lecteur de fichiers Excel pour tests paramétrés (future utilisation avec openpyxl)

### 9. **Générateur IA** (`ai_gen/generate_tests.py`)

Génère des cas de test à partir d'une User Story :
- Intégration Gemini (Google Generative AI)
- Fallback OpenRouter (modèles gratuits)
- Sortie en format Markdown tabulaire

---

## 📊 Cas de Test Détaillés

### Tests de Login (7 cas) - `test_login.py`

| ID | Scénario | Résultat |
|----|----------|----------|
| T1 | Connexion réussie (standard_user) | Redirection inventory.html ✅ |
| T2 | Connexion réussie (locked_out_user) | Redirection inventory.html ✅ |
| T3 | Utilisateur incorrect | Message "Username and password do not match" ❌ |
| T4 | Mauvais mot de passe | Message "Username and password do not match" ❌ |
| T5 | Champ username vide | Message "Username is required" ❌ |

### Tests d'Inventaire (2 cas) - `test_inventory.py`

| ID | Scénario | Résultat |
|----|----------|----------|
| I1 | Ajout de produit | Panier = 1 ✅ |
| I2 | Suppression de produit | Panier = 0 ✅ |

### Tests de Panier (4 cas) - `test_cart.py`

| ID | Scénario | Résultat |
|----|----------|----------|
| C1 | Suppression d'article | Panier vidé ✅ |
| C2 | Accès au checkout | Redirection checkout-step-one ✅ |
| C3 | Retour au catalogue | Redirection inventory ✅ |
| C4 | Accès détail produit | Navigation correcte ✅ |

### Tests de Paiement (4 cas) - `test_checkout.py`

| ID | Scénario | Résultat |
|----|----------|----------|
| P1 | Infos valides | Redirection checkout-step-two ✅ |
| P2 | Champ Last Name vide | Erreur et blocage ❌ |
| P3 | Calcul des totaux | Math correcte (Item + Tax = Total) ✅ |
| P4 | Commande complète | Message "Thank you for your order!" ✅ |

### Tests de Produits (2 cas) - `test_products.py`

| ID | Scénario | Résultat |
|----|----------|----------|
| Prod1 | Cohérence prix | Liste == Détail ✅ |
| Prod2 | Format de prix | Regex $XX.XX valide ✅ |

### Tests de Performance (1 cas) - `test_load_times.py`

| ID | Scénario | Seuil |
|----|----------|--------|
| Perf1 | Temps de chargement login | < 2.0s ✅ |

### Tests de Responsivité (1 cas) - `test_mobile_view.py`

| ID | Scénario | Résultat |
|----|----------|----------|
| Mob1 | Layout mobile (iPhone X) | Titre visible ✅ |

---

## 🚀 Fonctionnalités Avancées

### 1. Paramétrisation des Tests

Tests réutilisables avec différentes données :

```python
@pytest.mark.parametrize("username", ["standard_user", "locked_out_user"])
def test_successful_login(driver, username):
    # Test exécuté 2 fois avec chaque username
```

### 2. Fixtures Pytest

Setup/Teardown automatique :

```python
@pytest.fixture
def setup_checkout(driver):
    # Préparation commune pour tous les tests de paiement
    # Retourne les pages nécessaires
```

### 3. Validations Avancées

- ✅ Validation regex (format des prix)
- ✅ Calcul mathématique (sous-total + taxe = total)
- ✅ Comparaison cross-page (prix liste vs détail)
- ✅ Assertions sur les URLs

### 4. Tests de Performance

Mesure du temps de chargement :

```python
assert load_time < 2.0  # Page doit charger en moins de 2s
```

### 5. Tests de Responsivité Mobile

Émulation d'appareils mobiles (iPhone X) :

```python
mobile_emulation = { "deviceName": "iPhone X" }
```

---

## 📈 Rapports et Logs

### Générer un Rapport HTML

```bash
pytest --html=report.html --self-contained-html
```

Cela crée un fichier `report.html` avec :
- ✅ Résumé pass/fail
- 📊 Graphiques et statistiques
- 🕐 Durée d'exécution
- 📋 Logs détaillés
- 🖼️ Screenshots (si configuré)

### Voir les Logs en Direct

```bash
pytest -s  # Affiche tous les print()
pytest -v  # Mode verbeux
```

---

## 🛠️ Dépannage

### Problèmes Courants

| Problème | Solution |
|----------|----------|
| `NoSuchElementException` | Vérifier le sélecteur, augmenter timeout `wait.until()` |
| WebDriver non trouvé | Ajouter le chemin du driver au `PATH` |
| Test timeout | Vérifier la connexion réseau, augmenter `implicitly_wait()` |
| Erreur `GEMINI_API_KEY` | Créer un fichier `.env` avec la clé API |

### Mode Headless vs Headful

```python
# conftest.py : Comment/décommenter
options.add_argument("--headless")  # Sans fenêtre (rapide)
# Pas de --headless = avec fenêtre visuelle (debug)
```

---

## 📚 Documentation Supplémentaire

- [Selenium Python Documentation](https://selenium.dev/selenium/docs/apis/py/)
- [pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Best Practices](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Google Generative AI API](https://ai.google.dev/)

---

## 📝 Notes sur le Projet

- **Langage** : Python 3.8+
- **Framework Test** : pytest
- **Modèle d'Automatisation** : Page Object Model (POM)
- **Site Testé** : SauceDemo (https://www.saucedemo.com/)
- **Couverture** : Fonctionnel, Performance, Responsivité
- **Total des Tests** : 25 cas de test

---

## 🤝 Contributions

Pour ajouter de nouveaux tests :

1. Créez une nouvelle page dans `pages/` si nécessaire
2. Écrivez le test dans `tests/functional/` ou autre catégorie
3. Lancez les tests : `pytest -v`
4. Générez un rapport HTML

---

**Dernière mise à jour** : Décembre 2025
