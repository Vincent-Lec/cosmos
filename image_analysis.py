import pyqtgraph as pg
import numpy as np
from astropy.io import fits
import cv2  # Si vous utilisez OpenCV pour traiter les images

class ImageProcessor:
    def __init__(self, win):
        self.win = win
        self.p1 = None
        self.img = None
        self.roi = None
        self.iso = None
        self.hist = None
        self.isoLine = None
        self.p2 = None

    def setup_image_analysis(self):
        """Configurer les composants pour l'analyse d'image"""
        # A plot area (ViewBox + axes) for displaying the image
        self.p1 = self.win.addPlot(title="")

        # Item for displaying image data
        self.img = pg.ImageItem()
        self.p1.addItem(self.img)

        # Custom ROI for selecting an image region
        self.roi = pg.ROI([0, 0], [1000, 1000])
        self.roi.addScaleHandle([0.5, 0], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.p1.addItem(self.roi)
        self.roi.setZValue(10000)  # make sure ROI is drawn above image

        # Isocurve drawing
        self.iso = pg.IsocurveItem(level=0.8, pen='g')
        self.iso.setParentItem(self.img)
        self.iso.setZValue(5)

        # Contrast/color control
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.win.addItem(self.hist)

        # Draggable line for setting isocurve level
        self.isoLine = pg.InfiniteLine(angle=0, movable=True, pen='g')
        self.hist.vb.addItem(self.isoLine)
        self.hist.vb.setMouseEnabled(y=False)  # makes user interaction a little easier
        self.isoLine.setValue(0.8)
        self.isoLine.setZValue(1000)  # bring iso line above contrast controls

        # Another plot area for displaying ROI data
        self.win.nextRow()
        self.p2 = self.win.addPlot(colspan=2)
        self.p2.setMaximumHeight(250)
        self.win.resize(800, 800)
        self.win.show()

    def process_image(self, file_name):
        """Traitement de l'image à partir d'un fichier FITS"""
        image_data, header = self.read_fits_image(file_name)
        self.display_image(self.img, self.hist, self.iso, image_data)
        self.roi.sigRegionChanged.connect(self.update_plot)
        self.isoLine.sigDragged.connect(self.update_isocurve)

    def update_plot(self):
        """Mise à jour du tracé basé sur la région d'intérêt"""
        roi_data = self.roi.getArrayRegion(self.img.image, self.img)
        if roi_data is not None and roi_data.size > 0:
            profile = roi_data.mean(axis=1)  # Calculer le profil spectral en prenant la moyenne sur l'axe y
            self.p2.plot(profile, clear=True)  # Afficher le profil dans le deuxième graphique

    def update_isocurve(self):
        """Mise à jour de la courbe d'isocourbes"""
        self.iso.setLevel(self.isoLine.value())

    def read_fits_image(self, file_name):
        """Lire les données d'une image FITS"""
        with fits.open(file_name) as hdul:
            data = hdul[0].data
            header = hdul[0].header
        return data, header

    def display_image(self, img_item, hist_item, iso_item, image_data):
        """Afficher l'image dans le widget pyqtgraph"""
        rotated_data = np.rot90(image_data, 3)
        img_item.setImage(rotated_data)
        hist_item.setLevels(rotated_data.min(), rotated_data.max())
        iso_item.setData(pg.gaussianFilter(rotated_data, (2, 2)))

    def adjust_image(self, image_data, brightness, contrast):
        """Ajuster la luminosité et le contraste d'une image"""
        # Ajuster les niveaux de luminosité et de contraste
        adjusted_image = cv2.convertScaleAbs(image_data, alpha=1 + contrast / 100, beta=brightness)
        return adjusted_image
