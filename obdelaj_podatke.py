import os
import re
import csv


class Clanek:
    '''
    Razred Clanek predstavlja clanek z naslovom, vsebino in avtorjem
    '''
    def __init__(self, naslov, vsebina, avtor):
        self.naslov = naslov
        self.vsebina = vsebina
        self.avtor = avtor


def save_data_to_csv(data):
    '''
    Funkcija save_data_to_csv shrani podatke v csv datoteko z uporabo knjiznice csv
    '''
    os.makedirs("obdelani_podatki", exist_ok=True)

    with open("obdelani_podatki/clanki.csv", "w", encoding='utf-8') as csv_file:
        # objekt za pisanje v csv datoteko
        writer = csv.DictWriter(csv_file, fieldnames=["naslov", "avtor", "vsebina" ])
        writer.writeheader()
        # zapisemo vsak clanek
        for clanek in data:
            writer.writerow({"naslov": clanek.naslov, "avtor": clanek.avtor, "vsebina": clanek.vsebina})


def extract_data():
    '''
    Funkcija extract_data iz html niza izloci podatke o clankih - avtorju, naslovu in vsebini
    '''
    print("Pregledujem podatke za temo spanje")
    clanki = []

    # listdir vrne seznam vseh datotek v mapi
    for filename in os.listdir("clanki"):
        print("pregledujem", filename)
        with open("clanki/" + filename, "r", encoding='utf-8') as file:
            text = file.read()
            naslov = filename.strip(".html").replace("!", "").replace("?", "").replace(".", "").replace(",", "").lower()
            besede = ''
            
            # vzorec za avtorja
            vzorec_avtor = r'class="single__meta-author"[^>]*>([^<]+)<\/a>'
            avtor = re.search(vzorec_avtor, text, flags=re.DOTALL).group(1)
            
            # vzorec za odstavke
            vzorec_odstavek = r'<p>.*?</p>'
            odstavki = re.findall(vzorec_odstavek, text, flags=re.DOTALL)
            
            # iz vsakega odstavka odstranimo html znacke in dodamo vsebino v besede
            for odstavek in odstavki:
                odstavek = odstavek.lower()
                odstavek = odstavek.strip('<p>').strip('</p>').replace('\n', '').replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '').replace('.', '').replace(',', '').replace('?', '').replace('!', '')
                besede += odstavek

            clanki.append(Clanek(naslov, besede, avtor))
    
    # shranimo podatke v csv datoteko
    save_data_to_csv(clanki)


def najpogostejsa_beseda(clanki):
    # slovar najpogostejsih besed
    najpogostejse_besede = {}

    # uporabimo .unique() da dobimo vse avtorje samo enkrat
    for avtor in clanki['avtor'].unique():
        # slovar frekvenc besed
        besede = {}
        
        for index, row in clanki[clanki['avtor'] == avtor].iterrows():
            # .split() razdeli besedilo na posamezne besede
            besede_v_clanku = row['vsebina'].split()
            
            # za vsako besedo preverimo, če je beseda dolga vsaj 7 znakov
            for b in besede_v_clanku:
                if len(b) < 7:
                    continue
                
                # povečamo število pojavitev za 1
                if b in besede:
                    besede[b] += 1
                else:
                    besede[b] = 1
        
        # Najdemo najpogosteje uporabljeno besedo za vsakega avtorja
        max_beseda = ''
        max_count = 0
        for b, count in besede.items():
            if count > max_count:
                max_beseda = b
                max_count = count
        
        # shranimo najpogostejsi besedi za vsakega avtorja
        najpogostejse_besede[avtor] = max_beseda

    return najpogostejse_besede
