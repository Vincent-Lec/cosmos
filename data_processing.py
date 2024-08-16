import numpy as np
import cv2
from astropy.io import fits
from astroquery.simbad import Simbad
from astropy.table import Table
import pandas as pd
from astropy.convolution import convolve, Gaussian1DKernel
from lmfit.models import VoigtModel
from pybaselines import Baseline


class DataProcessor:
    def __init__(self):
        self.header = None

    def read_fits_file(self, file_name):
        """Lire les données d'un fichier FITS 1D"""
        with fits.open(file_name) as hdul:
            data = hdul[0].data
            header = hdul[0].header
        return data, header

    def extract_spectrum(self, header, data):
        """Extraire le spectre d'un fichier FITS 1D"""
        value1 = header['CRVAL1']
        pas = header['CDELT1']
        wavelength = [value1 + i * pas for i in range(len(data))]
        spectrum = data
        title = header['OBJNAME'] + ', ' + header['DATE-OBS'] + ', ' + header['BSS_INST'] + ', ' + header['OBSERVER']
        obj_name = header['OBJNAME']
        result_table = Simbad.query_objectids(obj_name)
        date_obs = header['DATE-OBS']
        print(type(header['BSS_ITRP']))
        if isinstance(header['BSS_ITRP'], int):
            resolution = header['BSS_ITRP']
        else:
            resolution = None
        hd_number = None  # Initialisation en dehors de la boucle

        for i in range(len(result_table)):
            if 'HD' in result_table['ID'][i]:    
                hd_number = result_table['ID'][i]
            else:
                pass

        print('hd_number_extract', hd_number)
        return wavelength, spectrum, title, hd_number, obj_name, date_obs,  resolution


    def process_file(self, file_name):
        data, self.header = self.read_fits_file(file_name)
        wavelength, spectrum, title, hd_number, obj_name, date_obs, resolution = self.extract_spectrum(self.header, data)
        return wavelength, spectrum, title, hd_number, obj_name, date_obs, resolution


    def plot_melchiors_BR(self, hd_number):
        df = pd.read_excel("melchiors_lib.xlsx")
        ref_number = df.loc[df['Name1'] == hd_number, 'ID'].values[0]

        file = f"https://royer.se/melchiors/spectra/00{ref_number}_melchiors_spectrum.fits.gz"

        table = Table.read(file, format='fits')

        gauss_kernel = Gaussian1DKernel(80)  # basse résolution
        smoothed_data_gauss = convolve(table['flux_tac'], gauss_kernel)

        wave = table['wave']
        mask = (wave >= 6620) & (wave <= 6640)
        
        mean_value = smoothed_data_gauss[mask].mean()
        smoothed_data_gauss /= mean_value

        return table['wave'], smoothed_data_gauss

    def plot_melchiors_HR(self, hd_number):
        df = pd.read_excel("melchiors_lib.xlsx")
        ref_number = df.loc[df['Name1'] == hd_number, 'ID'].values[0]

        file = f"https://royer.se/melchiors/spectra/00{ref_number}_melchiors_spectrum.fits.gz"

        table = Table.read(file, format='fits')

        gauss_kernel = Gaussian1DKernel(1)  # haute résolution
        smoothed_data_gauss = convolve(table['flux_tac'], gauss_kernel)

        wave = table['wave']
        mask = (wave >= 6620) & (wave <= 6640)
        
        mean_value = smoothed_data_gauss[mask].mean()
        smoothed_data_gauss /= mean_value

        return table['wave'], smoothed_data_gauss

    def fit_voigt(self,x, y, center):
        model = VoigtModel()
        params = model.make_params(center=center, amplitude=max(y), sigma=1.0, fraction=0.5)
        result = model.fit(y, params, x=x)
        return result

    
    def remove_atmospheric_lines(self, x, y):

        line_positions = [
            6508.603, 6511.999, 6512.242, 6514.727, 6516.437, 6516.543, 6516.625, 6519.467, 
            6523.850, 6532.459, 6534.000, 6534.014, 6536.726, 6542.317, 6543.912, 6547.705,
            6548.627, 6552.632, 6557.181, 6558.149, 6560.501, 6564.208, 6568.806, 6572.087, 
            6574.860, 6580.794, 6586.559, 6594.375, 6599.365, 6605.566, 6612.550
        ]

        # estimation de la ldb
        baseline_fitter = Baseline(x_data=x)
        bkg, params = baseline_fitter.asls(y, lam=1e5, p=0.95)  # pouvoir modifier ces parametres , p en particulier ?

        # Correction du spectre de la ldb
        y_corrected = y - bkg

        # Fit  avec profil de Voigt
        for pos in line_positions:
            window = 2  # pouvoir modifier ce parametre ?
            mask = (x > pos - window) & (x < pos + window)
            
            try:
                result = self.fit_voigt(x[mask], y_corrected[mask], center=pos)
                y_corrected[mask] -= result.best_fit
                
            except Exception as e:
                print(f"Could not fit Pseudo-Voigt to line at {pos}: {e}")

        return x,y_corrected + bkg, bkg
