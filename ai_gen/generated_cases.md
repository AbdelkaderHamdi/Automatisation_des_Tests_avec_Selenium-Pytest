Voici les cas de test générés en boîte noire basés sur la User Story de connexion utilisateur :

| ID | Description | Pré-conditions | Étapes de test | Résultat Attendu |
|----|-------------|----------------|----------------|------------------|
| TC-01 | Connexion réussie avec identifiants valides (Happy Path) | 1. L'utilisateur est enregistré dans le système<br>2. L'application est accessible | 1. Accéder à la page de connexion<br>2. Saisir un email valide enregistré<br>3. Saisir le mot de passe correct associé<br>4. Cliquer sur le bouton "Se connecter" | L'utilisateur est redirigé vers son tableau de bord |
| TC-02 | Tentative de connexion avec email invalide (Negative testing) | 1. L'application est accessible<br>2. L'email testé n'est pas enregistré | 1. Accéder à la page de connexion<br>2. Saisir un email non enregistré<br>3. Saisir un mot de passe quelconque<br>4. Cliquer sur le bouton "Se connecter" | Le message "Utilisateur inconnu" s'affiche |
| TC-03 | Tentative de connexion avec mot de passe vide (Edge case) | 1. L'application est accessible<br>2. Un email valide est saisi | 1. Accéder à la page de connexion<br>2. Saisir un email valide<br>3. Laisser le champ mot de passe vide<br>4. Essayer de cliquer sur le bouton "Se connecter" | Le bouton "Se connecter" reste désactivé et l'utilisateur n'est pas connecté |

Cas supplémentaires suggérés (non inclus dans le tableau) :
- Connexion avec mot de passe incorrect (devrait afficher un message d'erreur spécifique)
- Test de sensibilité à la casse pour l'email/mot de passe
- Test avec des champs contenant des caractères spéciaux
- Test de performance avec réponse attendue sous X secondes