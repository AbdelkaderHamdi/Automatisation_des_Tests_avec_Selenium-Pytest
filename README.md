# Projet de Test Automatisé (Selenium + Python)

Ce projet utilise **pytest** et le **Page Object Model (POM)** pour tester un site web.

---

## 1. Installation 

1. Clonez ce projet.

2. Créez un environnement virtuel (recommandé) :

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Téléchargez les WebDrivers :
   - **ChromeDriver** (pour Chrome)
   - **GeckoDriver** (pour Firefox)
   - **EdgeDriver** (pour Edge)


   > Assurez-vous que ces fichiers `.exe` sont dans votre `PATH` système **ou** placez-les à la racine du projet.

---

## 2. Exécution des Tests

Le framework `pytest` détecte automatiquement les fichiers `test_*.py`.

### Exécuter le *Smoke Test*

Ouvrez un terminal à la racine du projet et lancez :

```bash
pytest
```

> Par défaut, cela utilise **Chrome** (défini dans `conftest.py`).

---

### Exécuter sur un navigateur spécifique

Utilisez l’option `--browser` ajoutée :

```bash
pytest --browser=firefox
```

ou

```bash
pytest --browser=edge
```

---

### Générer un Rapport HTML 

Grâce à `pytest-html`, générez un rapport visuel :

```bash
pytest --browser=chrome --html=report.html
```

> Ouvrez ensuite le fichier `report.html` dans votre navigateur pour consulter les résultats détaillés.
