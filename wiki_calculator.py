import asyncio
import aiohttp
from functools import lru_cache
from typing import List, Optional, Tuple
from collections import deque

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

async def shortest_path_bfs(start_page: str, target_page: str, max_depth: int = 3) -> Optional[List[str]]:
    # Vérifier le lien direct
    start_links = await get_wikipedia_links(start_page)
    if target_page in start_links:
        return [start_page, target_page]

    # ... (le reste du code reste inchangé)

# ... (le reste des fonctions restent inchangées)

async def main():
    start_page = "France"
    target_page = "Espagne"
    
    print(f"Recherche du chemin le plus court entre '{start_page}' et '{target_page}'...")
    path = await shortest_path_bfs(start_page, target_page)
    
    if path:
        print(f"Chemin trouvé ({len(path) - 1} étapes) : {' -> '.join(path)}")
    else:
        print("Aucun chemin trouvé.")

if __name__ == "__main__":
    asyncio.run(main())