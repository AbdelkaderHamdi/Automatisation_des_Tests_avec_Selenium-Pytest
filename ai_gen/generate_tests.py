import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_prompt_template(filename="prompt_templates.txt"):
    """Lit le template de prompt depuis le fichier"""
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_test_cases(user_story):
    """Envoie la User Story à Gemini et récupère les cas de test"""
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    # Charger le template et injecter la user story
    template = load_prompt_template()
    full_prompt = template.replace("{USER_STORY}", user_story)
    
    print("🤖 Génération en cours avec Gemini...")
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Erreur lors de la génération : {e}"

def save_output(content, filename="generated_cases.md"):
    """Sauvegarde le résultat dans le dossier ai_gen"""
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Cas de tests sauvegardés dans : {file_path}")

if __name__ == "__main__":
    # Exemple d'entrée (User Story)
    my_user_story = """
    Titre: Connexion utilisateur
    En tant qu'utilisateur enregistré,
    Je veux me connecter à l'application avec mon email et mot de passe,
    Afin d'accéder à mon tableau de bord.
    
    Critères d'acceptation:
    1. Si l'email et le mot de passe sont valides, rediriger vers le dashboard.
    2. Si l'email est invalide, afficher "Utilisateur inconnu".
    3. Si le mot de passe est vide, le bouton de connexion doit être désactivé.
    """
    
    result = generate_test_cases(my_user_story)
    save_output(result)