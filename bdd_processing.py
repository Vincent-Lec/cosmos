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

    
    url = "http://arasbeam.free.fr/spip.php?page=beam_belist2&lang=fr"

    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver la première table (ou la table cible) sur la page
    tables = soup.find_all('table')
    table = tables[4]

    # Trouver toutes les lignes (tr) dans le tableau
    rows = table.find_all('tr')

    
    id = []
    hd_number = []
    ad = []
    dec = []
    mag = []
    sptype = []
    date = []
    bgcolors = []  

    # Parcourir et récupérer le contenu des balises <td> de chaque ligne
    for row in rows:
        tds = row.find_all('td')  # Trouver toutes les balises <td> dans la ligne
        if len(tds) > 1:  # Vérifier qu'il y a au moins deux <td> dans la ligne
            id.append(tds[0].get_text(strip=True))
            hd_number.append(tds[1].get_text(strip=True))  
            ad.append(tds[2].get_text(strip=True))
            dec.append(tds[3].get_text(strip=True))
            mag.append(tds[4].get_text(strip=True))
            sptype.append(tds[5].get_text(strip=True))
            date.append(tds[9].get_text(strip=True))
            # Récupérer le code couleur de la dernière balise <td>
            bgcolor = tds[9].get('bgcolor', None)  
            bgcolors.append(bgcolor)  

    df = pd.DataFrame({
        'id': id[2:], 
        'hd': hd_number[2:], 
        'ad': ad[2:], 
        'dec': dec[2:], 
        'mag': mag[2:], 
        'sptype': sptype[2:], 
        'date': date[2:], 
        'bgcolor': bgcolors[2:] 
    })

    return df