import pandas as pd
from astroquery.simbad import Simbad
from astropy import coordinates
import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style, quantity_support
from astropy.time import Time
from bs4 import BeautifulSoup
import requests


def bess_request():

# URL de la page à analyser
    url = "http://arasbeam.free.fr/spip.php?page=beam_belist2&lang=fr"

    # Récupérer le contenu de la page
    response = requests.get(url)
    response.raise_for_status()  # Vérifie que la requête a réussi

    # Parser le contenu avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver la première table (ou la table cible) sur la page
    tables = soup.find_all('table')
    table = tables[4]

    # Trouver toutes les lignes (tr) dans le tableau
    rows = table.find_all('tr')

    # Liste pour stocker le contenu de la première balise <td> de chaque ligne
    id = []

    # Parcourir et récupérer le contenu de la première balise <td> de chaque ligne
    for row in rows:
        first_td = row.find('td')  # Trouver la première balise <td> dans la ligne
        if first_td:
            id.append(first_td.get_text(strip=True))  # Ajouter le texte à la liste

    hd_number = []
    ad = []
    dec = []
    mag = []
    sptype = []
    date = []

    # Parcourir et récupérer le contenu de la deuxième balise <td> de chaque ligne
    for row in rows:
        tds = row.find_all('td')  # Trouver toutes les balises <td> dans la ligne
        if len(tds) > 1:  # Vérifier qu'il y a au moins deux <td> dans la ligne
            hd_number.append(tds[1].get_text(strip=True))  # Ajouter le texte de la 2ème <td> à la liste
            ad.append(tds[2].get_text(strip=True))
            dec.append(tds[3].get_text(strip=True))
            mag.append(tds[4].get_text(strip=True))
            sptype.append(tds[5].get_text(strip=True))
            date.append(tds[6].get_text(strip=True))

    # Afficher la liste des contenus de la deuxième balise <td>
    df = pd.DataFrame(columns=['id', 'hd', 'ad', 'dec', 'mag', 'sptype', 'date'])

    df['id'] = id[2:]
    df['hd'] = hd_number[2:]
    df['ad'] = ad[2:]
    df['dec'] = dec[2:]
    df['mag'] = mag[2:]
    df['sptype'] = sptype[2:]
    df['date'] = date[2:]

    return df