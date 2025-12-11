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
        "z-ai": "z-ai/glm-4.5-air:free",           # Recommandé
        "mistral": "mistralai/devstral-2512:free",     # Alternative
        "qwen": "qwen/qwen3-coder:free",           # Alternative
        "llama": "meta-llama/llama-3.2-3b-instruct" ,   # Alternative
        "openai": "openai/gpt-oss-120b:free"    # Alternative
    }
    
    data = {
        "model": models["mistral"],  # Changer ici pour tester d'autres modèles
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
    Ajout d'un produit au panier
    Titre : Ajouter un article au panier
    En tant qu' utilisateur connecté,
    Je veux pouvoir ajouter un produit spécifique depuis la page des produits à mon panier,
    Afin d' pouvoir l'acheter plus tard.
    Critères d'acceptation :
    Sur la page /inventory.html, chaque produit doit avoir un bouton "Add to cart".
    Cliquer sur le bouton "Add to cart" pour un produit change le bouton en "Remove" et incrémente le compteur du panier (l'icône du panier en haut à droite).
    Le compteur du panier doit afficher "1" après avoir ajouté le premier article.
    Le produit ajouté doit être visible dans le panier lorsque l'utilisateur navigue vers la page du panier.
    """
    
    result = generate_test_cases_with_OpenRouter(my_user_story)
    save_output(result)