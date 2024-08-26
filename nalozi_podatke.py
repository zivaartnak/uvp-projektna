import requests
import re
import os


def download_link(url):
    '''
    Funkcija download_url_to_string nalozi spletno stran in vrne njen html niz
    '''
    # v primeru, da je url neveljaven, vrni None
    try:
        text = requests.get(url).text

    except requests.exceptions.RequestException:
        print('Spletne strani ni bilo mogoce prenesti')
        return None
    return text


def save_to_file(text, mapa, filename):
    '''
    Funkcija save_text_to_file shrani niz v datoteko
    '''
    # ustvari mapo, ce ta ne obstaja
    os.makedirs(mapa, exist_ok=True)
    # ustvari pot do datoteke
    path = os.path.join(mapa, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        # shrani niz v datoteko
        file_out.write(text)
    return None

def download_article(naslov, link):
    '''
    Funkcija download_article shrani clanek v html obliki
    '''
    text = download_link(link)
    save_to_file(text, "clanki", naslov + ".html")


def extract_data(text):
    '''
    Funkcija extract_data iz html niza izloci podatke o clankih
    '''

    # regex vzorec za clanek
    clanek_vzorec = r'<article class="card-d">.*?</article>'
    clanki = re.findall(clanek_vzorec, text, flags=re.DOTALL)
    # iteriramo cez vse najdene clanke
    for clanek in clanki:
        naslov_vzorec = r'<h3 class="title">.*?</h3>'
        naslov = re.search(naslov_vzorec, clanek, flags=re.DOTALL).group()
        naslov = naslov.strip('<h3 class="title">').strip('</h3>')

        link_vzorec = r'<a href=".*?"'
        link = re.search(link_vzorec, clanek, flags=re.DOTALL).group()
        link = link.strip('<a href=').strip('"')

        download_article(naslov, link)
        print("Shranil sem clanek " + naslov)


def get_pages(zacetni_url, tema):
    '''
    Funkcija get_pages iz dane teme shrani vse strani
    '''

    # generiramo ustrezni url
    url = zacetni_url + "/" + tema
    
    # nalozimo prvih 5 strani - range(1, 6) pomeni, da gremo od 1 do 5
    for i in range(1, 6):
        text = download_link(url + "/page/" + str(i))

        extract_data(text)
        print("Shranil sem stran " + str(i) + " za temo " + tema)


def save_web_data():
    '''
    Funkcija save_web_data shrani vse podatke iz spletne strani
    '''

    link = "https://med.over.net/rubrika/teme-meseca/spanje/pages"
    get_pages(link, "spanje")
