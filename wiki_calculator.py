import asyncio
import aiohttp
from functools import lru_cache
from typing import List, Optional, Tuple
from collections import deque

# Utilisation de lru_cache pour une gestion efficace du cache
@lru_cache(maxsize=1000)
async def get_wikipedia_links(page_title: str) -> List[str]:
    base_url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "links",
        "titles": page_title,
        "pllimit": "500",
        "format": "json"
    }
    
    links = []
    async with aiohttp.ClientSession() as session:
        try:
            while True:
                async with session.get(base_url, params=params, timeout=5) as response:
                    if response.status != 200:
                        print(f"Erreur HTTP {response.status} pour la page {page_title}")
                        break
                    
                    data = await response.json()
                    
                    pages = data.get('query', {}).get('pages', {})
                    for page_id in pages:
                        page = pages[page_id]
                        if "links" not in page:
                            print(f"Aucun lien trouvé pour la page {page_title}.")
                            break
                        links.extend([link['title'] for link in page['links']])
                    
                    continue_token = data.get('continue', {}).get('plcontinue')
                    if continue_token:
                        params["plcontinue"] = continue_token
                    else:
                        break
        except asyncio.TimeoutError:
            print(f"Timeout lors de la récupération des liens pour {page_title}")
        except Exception as e:
            print(f"Erreur lors de la récupération des liens pour {page_title}: {e}")
    
    return links

async def shortest_path_bfs(start_page: str, target_page: str) -> Optional[List[str]]:
    queue = deque([(start_page, [start_page])])
    visited = set()
    
    while queue:
        current_page, path = queue.popleft()
        
        if current_page == target_page:
            return path
        
        if current_page in visited:
            continue
        visited.add(current_page)
        
        links = await get_wikipedia_links(current_page)
        for link in links:
            if link not in visited:
                queue.append((link, path + [link]))

    return None

async def main():
    start_page = "France"
    target_page = "Spain"
    
    print(f"Recherche du chemin le plus court entre '{start_page}' et '{target_page}'...")
    path = await shortest_path_bfs(start_page, target_page)
    
    if path:
        print(f"Chemin trouvé ({len(path) - 1} étapes) : {' -> '.join(path)}")
    else:
        print("Aucun chemin trouvé.")

if __name__ == "__main__":
    asyncio.run(main())