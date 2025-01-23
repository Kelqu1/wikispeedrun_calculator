import requests
from collections import deque

# Cache pour stocker les liens déjà récupérés
link_cache = {}

# Fonction pour récupérer les liens d'une page Wikipédia
def get_wikipedia_links(page_title):
    # Vérifier si les liens de cette page sont déjà dans le cache
    if page_title in link_cache:
        return link_cache[page_title]
    
    base_url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "links",
        "titles": page_title,
        "pllimit": "500",  # Limite maximale par requête
        "format": "json"
    }
    
    links = []  # Liste pour stocker tous les liens
    try:
        while True:
            response = requests.get(base_url, params=params, timeout=5)
            # Vérification du statut de la réponse
            if response.status_code != 200:
                print(f"Erreur HTTP {response.status_code} pour la page {page_title}")
                break
            
            data = response.json()
            
            # Extraire les liens de la réponse
            pages = data.get('query', {}).get('pages', {})
            for page_id in pages:
                page = pages[page_id]
                # Vérifier si la page contient des liens
                if "links" not in page:
                    print(f"Aucun lien trouvé pour la page {page_title}.")
                    break
                for link in page['links']:
                    links.append(link['title'])
            
            # Vérifier si un token "plcontinue" est présent pour récupérer les liens suivants
            continue_token = data.get('continue', {}).get('plcontinue')
            if continue_token:
                params["plcontinue"] = continue_token  # Ajouter le token pour la requête suivante
            else:
                break  # Arrêter la boucle si tous les liens ont été récupérés
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des liens pour {page_title}: {e}")
    
    # Mettre les liens dans le cache
    link_cache[page_title] = links
    return links

# Fonction pour trouver le chemin le plus court entre deux pages
def shortest_path_bfs(start_page, target_page):
    # File pour BFS
    queue = deque([(start_page, [start_page])])  # Chaque élément : (page_actuelle, chemin)
    visited = set()  # Ensemble des pages déjà explorées
    
    while queue:
        current_page, path = queue.popleft()
        
        # Vérifier si nous avons atteint la page cible
        if current_page == target_page:
            return path  # Retourner le chemin trouvé
        
        # Si déjà visité, ignorer
        if current_page in visited:
            continue
        visited.add(current_page)  # Marquer comme visité
        
        # Récupérer les liens de la page actuelle
        links = get_wikipedia_links(current_page)
        if not links:  # Si aucun lien trouvé, passer à la prochaine page
            continue
        
        # Ajouter les voisins à la file d'attente
        for link in links:
            if link not in visited:
                queue.append((link, path + [link]))  # Ajouter le chemin mis à jour

    return None  # Aucun chemin trouvé

# Point d'entrée principal
if __name__ == "__main__":
    start_page = "France"
    target_page = "Spain"
    
    print(f"Recherche du chemin le plus court entre '{start_page}' et '{target_page}'...")
    path = shortest_path_bfs(start_page, target_page)
    
    if path:
        print(f"Chemin trouvé ({len(path) - 1} étapes) : {' -> '.join(path)}")
    else:
        print("Aucun chemin trouvé.")
