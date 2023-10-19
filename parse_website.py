import requests
from bs4 import BeautifulSoup

URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
BASE_URL = "https://bulbapedia.bulbagarden.net"


def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        print("Failed")
        return None


soup = fetch_page(URL)


def extract_pokemon(page: BeautifulSoup):
    generations = []
    pokemons = []
    for h3 in page.find_all('h3'):
        if len(h3.findChildren("span")) != 0:
            generations.append(h3)
    for index, gen in enumerate(generations):
        table = gen.find_next_sibling()
        rows = table.findAll('tr')[1:]
        prev_ndex = None
        for row in rows:
            cols = row.findAll('td')
            if cols[0].text.strip():
                ndex = cols[0].text.strip()
                prev_ndex = ndex
                name_col = 2
                type_start_col = -2 if len(cols) == 5 else -1
            else:
                ndex = prev_ndex
                name_col = 1
                type_start_col = -2 if len(cols) == 4 else -1
            name_data = cols[name_col].find('a', href=True)
            name = name_data.text.strip()
            form_tag = cols[name_col].find('small')
            if form_tag:
                form_name = form_tag.text.strip()
                name = f"{form_name.split(' ')[0]} {name}"
            types = [a.text for col in cols[type_start_col:] for a in col.findAll('a')]
            pokemon_data = {
                'Generation': index + 1,
                'Ndex': ndex,
                'Name': name,
                'Type 1': types[0],
                'Type 2': types[1] if len(types) > 1 else None,
                'URL': BASE_URL + name_data['href']
            }
            pokemon_soup = fetch_page(pokemon_data['URL'])
            span_tag = pokemon_soup.find('span', {'id': 'Base_stats'})
            h4_tag = span_tag.parent
            table = h4_tag.find_next_sibling('table')
            if not table:
                h5_tag = h4_tag.find_next_sibling('h5', string=lambda s: pokemon_data['Name'] in s)
                if h5_tag:
                    table = h5_tag.find_next_sibling('table')
            print(ndex)
            if ndex == "#0026":
                print(table)
                break
            # pokemons.append(pokemon_data)
        break
    # print(pokemons)


extract_pokemon(soup)
