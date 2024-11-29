import requests
import networkx as nx
import matplotlib.pyplot as plt

def get_wikipedia_links(page_title):
    url = f'https://fr.wikipedia.org/w/api.php?action=query&prop=links&titles={page_title}&pllimit=10&format=json'  # Limite les liens
    response = requests.get(url)
    data = response.json()
    
    links = []
    pages = data.get('query', {}).get('pages', {})
    
    for page_id in pages:
        page = pages[page_id]
        for link in page.get('links', []):
            links.append(link['title'])
    
    print(f"Liens récupérés pour {page_title}: {links}")  # Affiche les liens récupérés
    return links

def build_graph(start_page):
    G = nx.Graph()
    G.add_node(start_page)
    
    links = get_wikipedia_links(start_page)
    
    for link in links:
        G.add_edge(start_page, link)
        
        sub_links = get_wikipedia_links(link)
        for sub_link in sub_links:
            G.add_edge(link, sub_link)
    
    return G

def plot_graph(G):
    plt.figure(figsize=(12, 12))
    nx.draw(G, with_labels=True, node_size=50, font_size=10, font_weight='bold', node_color='skyblue')
    plt.title('Graphe des liens Wikipédia')
    plt.show()

if __name__ == "__main__":
    start_page = "Python_(langage)"  # Titre de la page Wikipédia de départ
    graph = build_graph(start_page)
    plot_graph(graph)
