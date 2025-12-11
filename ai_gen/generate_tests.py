import os
import google.generativeai as genai
import requests
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



def generate_test_cases_with_OpenRouter(user_story):
    """
    Génère un test avec l'API OpenRouter (modèles gratuits).
    """
    # Clé API OpenRouter (gratuite)
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found.")
        return

    # Charger le template de prompt
    try:
        with open("ai_gen/prompt_templates.txt", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print("Error: ai_gen/prompt_templates.txt not found.")
        return

    prompt = template.format(
        USER_STORY=user_story
    )

    # Configuration de l'API OpenRouter
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",  # Optionnel
        "X-Title": "Selenium Test Generator"      # Optionnel
    }
    
    # Modèles gratuits disponibles
    models = {
        "deepseek": "deepseek/deepseek-chat",           # Recommandé
        "mistral": "mistralai/mistral-7b-instruct",     # Alternative
        "qwen": "qwen/qwen-2.5-7b-instruct",           # Alternative
        "llama": "meta-llama/llama-3.2-3b-instruct"    # Alternative
    }
    
    data = {
        "model": models["deepseek"],  # Changer ici pour tester d'autres modèles
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        print("🔄 Génération du test en cours...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result['choices'][0]['message']['content']
        
        print("\n✅ Test généré avec succès!")
        print(generated_text)
        
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling OpenRouter API: {e}")
        return None



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
    
    result = generate_test_cases_with_OpenRouter(my_user_story)
    save_output(result)