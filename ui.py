import numpy as np
from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                               QFileDialog, QMessageBox, QLabel, QStackedWidget, 
                               QTableWidget, QTableWidgetItem, QSplitter,QCheckBox, QHeaderView,QColorDialog, 
                               QInputDialog,QMenuBar,QMenu, QDialog, QCalendarWidget,QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import pyqtgraph as pg
from data_processing import DataProcessor
from image_analysis import ImageProcessor
from bdd_processing import bess_request
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cosmos")

        # Créer le widget central et le layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)

        # Créer le menu à gauche
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(self.menu_layout)

        self.homeButton = QPushButton("Accueil")
        self.homeButton.clicked.connect(self.show_home)
        self.menu_layout.addWidget(self.homeButton)

        self.graphButton = QPushButton("FITS 1D")
        self.graphButton.clicked.connect(self.show_graph_page)
        self.menu_layout.addWidget(self.graphButton)

        self.imageButton = QPushButton("FITS 2D")
        self.imageButton.clicked.connect(self.show_image_page)
        self.menu_layout.addWidget(self.imageButton)

        self.comparaisonButton = QPushButton("Comparaison")
        self.comparaisonButton.clicked.connect(self.show_comparaison_page)
        self.menu_layout.addWidget(self.comparaisonButton)

        self.bddButton = QPushButton("Base de Données")
        self.bddButton.clicked.connect(self.show_bdd_page)
        self.menu_layout.addWidget(self.bddButton)


        # Créer le QStackedWidget pour changer de pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Page d'accueil
        self.home_page = QWidget()
        home_layout = QVBoxLayout(self.home_page)
        
        # Ajouter un titre principal
        home_title = QLabel("Cosmos")
        home_title.setAlignment(Qt.AlignCenter)
        home_title.setStyleSheet("font-size: 48px; font-weight: bold;")
        home_layout.addWidget(home_title)

        # Ajouter un sous-titre
        home_subtitle = QLabel("Analyse des données astronomiques")
        home_subtitle.setAlignment(Qt.AlignCenter)
        home_subtitle.setStyleSheet("font-size: 24px; color: gray;")
        home_layout.addWidget(home_subtitle)

        # Ajouter un texte descriptif
        description = QLabel(
            "Bienvenue dans Cosmos, une application pour l'analyse et la visualisation des données FITS. "
            "Utilisez les boutons à gauche pour explorer les différentes fonctionnalités, "
            "y compris l'analyse spectrale et l'affichage de spectres 2D."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("font-size: 24px; color: gray;")
        home_layout.addWidget(description)

        # Ajouter des boutons de navigation rapide (ronds)
        btn_layout = QHBoxLayout()
        quick_graph_btn = QPushButton("FITS 1D")
        quick_graph_btn.setFixedSize(120, 120)
        quick_graph_btn.setStyleSheet("border-radius: 50px; background-color: #4CAF50; color: white; font-size: 14px;")
        quick_graph_btn.clicked.connect(self.show_graph_page)
        btn_layout.addWidget(quick_graph_btn)

        quick_image_btn = QPushButton("FITS 2D")
        quick_image_btn.setFixedSize(120, 120)
        quick_image_btn.setStyleSheet("border-radius: 50px; background-color: #4CAF50; color: white; font-size: 14px;")
        quick_image_btn.clicked.connect(self.show_image_page)
        btn_layout.addWidget(quick_image_btn)

        quick_compare_btn = QPushButton("Comparaison")
        quick_compare_btn.setFixedSize(120, 120)
        quick_compare_btn.setStyleSheet("border-radius: 50px; background-color: #4CAF50; color: white; font-size: 14px;")
        quick_compare_btn.clicked.connect(self.show_comparaison_page)
        btn_layout.addWidget(quick_compare_btn)
        home_layout.addLayout(btn_layout)


        quick_bdd_btn = QPushButton("Base de Données")
        quick_bdd_btn.setFixedSize(120, 120)
        quick_bdd_btn.setStyleSheet("border-radius: 50px; background-color: #4CAF50; color: white; font-size: 14px;")
        quick_bdd_btn.clicked.connect(self.show_bdd_page)
        btn_layout.addWidget(quick_bdd_btn)
        home_layout.addLayout(btn_layout)


        # Ajouter des informations sur la version et l'auteur
        footer = QLabel("Version 0.1 - Développé par V. Lecocq")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 12px; color: gray;")
        home_layout.addWidget(footer)

        self.stacked_widget.addWidget(self.home_page)

        # Page de graphes
        self.graph_page = GraphPage()
        self.stacked_widget.addWidget(self.graph_page)

        # Page d'images
        self.image_page = ImagePage()
        self.stacked_widget.addWidget(self.image_page)

        # Page de comparaison
        self.comparaison_page = ComparaisonPage()
        self.stacked_widget.addWidget(self.comparaison_page)

        # Page de comparaison
        self.bdd_page = BDDPage()
        self.stacked_widget.addWidget(self.bdd_page)



        self.show_home()

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_graph_page(self):
        self.stacked_widget.setCurrentWidget(self.graph_page)

    def show_image_page(self):
        self.stacked_widget.setCurrentWidget(self.image_page)

    def show_comparaison_page(self):
        self.stacked_widget.setCurrentWidget(self.comparaison_page)

    def show_bdd_page(self):
        self.stacked_widget.setCurrentWidget(self.bdd_page)


class ImagePage(QWidget):
    def __init__(self):
        super(ImagePage, self).__init__()

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Créer un bouton pour ouvrir un fichier image
        self.openImageButton = QPushButton("Ouvrir un fichier FITS 2D")
        self.openImageButton.clicked.connect(self.open_image)
        layout.addWidget(self.openImageButton)

        # Créer le widget de pyqtgraph pour l'analyse d'image
        self.win = pg.GraphicsLayoutWidget()
        layout.addWidget(self.win)

        # Setup image analysis components
        self.image_processor = ImageProcessor(self.win)
        self.image_processor.setup_image_analysis()

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier FITS 2D", "", "Fichiers FITS 2D (*.fits *.fit);;Tous les fichiers (*)")

        if file_name:
            try:
                self.image_processor.process_image(file_name)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))



class GraphPage(QWidget):
    def __init__(self):
        super(GraphPage, self).__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.hd_number = None
        self.resolution = None

        # barre de menu
        self.menu_bar = QMenuBar(self)

        # menu "File"
        file_menu = QMenu("Fichier", self)
        self.menu_bar.addMenu(file_menu)


        # menu "Options"
        options_menu = QMenu("Options", self)
        self.menu_bar.addMenu(options_menu)

        # actionsd du menu "File"
        self.open_file_action = file_menu.addAction("Ouvrir un FITS 1D")
        #self.open_file_action.setCheckable(True)
        self.open_file_action.triggered.connect(self.open_file)


        # actionsd du menu "Options"
        self.balmer_lines_action = options_menu.addAction("Afficher les raies de Balmer")
        self.balmer_lines_action.setCheckable(True)
        self.balmer_lines_action.triggered.connect(self.toggle_balmer_lines)

        self.melchiors_spectrum_action = options_menu.addAction("Superposer le spectre Melchiors")
        self.melchiors_spectrum_action.setCheckable(True)
        self.melchiors_spectrum_action.triggered.connect(self.toggle_melchiors_spectrum)

        # Sous-menu pour les raies atmosphériques
        atmo_menu = QMenu("Raies atmosphériques", self)
        options_menu.addMenu(atmo_menu)

        self.remove_atmo_action = atmo_menu.addAction("Afficher sans les raies")
        self.remove_atmo_action.setCheckable(True)
        self.remove_atmo_action.triggered.connect(self.toggle_remove_atmo)

        self.show_both_spectra_action = atmo_menu.addAction("Afficher les deux spectres")
        self.show_both_spectra_action.setCheckable(True)
        self.show_both_spectra_action.triggered.connect(self.toggle_show_both_spectra)

        self.show_baseline_action = atmo_menu.addAction("Afficher la ligne de base")
        self.show_baseline_action.setCheckable(True)
        self.show_baseline_action.triggered.connect(self.toggle_show_baseline)

        self.show_telluric_lines_action = atmo_menu.addAction("Afficher les raies telluriques")
        self.show_telluric_lines_action.setCheckable(True)
        self.show_telluric_lines_action.triggered.connect(self.toggle_show_telluric_lines)


        # Ajouter la barre de menu au layout principal
        main_layout.setMenuBar(self.menu_bar)

        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter, 1)

        self.graphWidget = pg.PlotWidget()
        self.splitter.addWidget(self.graphWidget)

        side_widget = QWidget()
        side_layout = QVBoxLayout()
        side_widget.setLayout(side_layout)
        self.splitter.addWidget(side_widget)

        self.table = QTableWidget()
        side_layout.addWidget(self.table)

        self.hd_number_label = QLabel("")
        side_layout.addWidget(self.hd_number_label)

        self.balmer_lines = [4101, 4340, 4861, 6563]
        self.balmer_lines_items = []
        self.hd_spectrum_item = None

        self.telluric_lines = [
            6508.603, 6511.999, 6512.242, 6514.727, 6516.437, 6516.543, 6516.625, 6519.467, 
            6523.850, 6532.459, 6534.000, 6534.014, 6536.726, 6542.317, 6543.912, 6547.705,
            6548.627, 6552.632, 6557.181, 6558.149, 6560.501, 6564.208, 6568.806, 6572.087, 
            6574.860, 6580.794, 6586.559, 6594.375, 6599.365, 6605.566, 6612.550
        ]

        # Configurer le style du graphe
        self.graphWidget.setBackground('w')
        self.graphWidget.getAxis('left').setPen('k')
        self.graphWidget.getAxis('bottom').setPen('k')
        self.graphWidget.getAxis('left').setTextPen('k')
        self.graphWidget.getAxis('bottom').setTextPen('k')

        self.data_processor = DataProcessor()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier FITS 1D", "", "Fichiers FITS 1D (*.fits *.fit);;Tous les fichiers (*)")

        if file_name:
            try:
                wavelength, spectrum, title, hd_number, obj_name, date_obs, resolution = self.data_processor.process_file(file_name)
                self.wavelength = wavelength
                self.spectrum = spectrum
                self.hd_number = hd_number
                self.resolution = resolution
                self.plot_spectrum(wavelength, spectrum, title)
                self.display_header(self.data_processor.header)
                self.hd_number_label.setText(f"Numéro HD: {hd_number}" if hd_number else "")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))

    def plot_spectrum(self, wavelength, spectrum, title):
        self.graphWidget.clear()
        self.graphWidget.plot(wavelength, spectrum, pen='k')
        self.graphWidget.setLabel('left', 'Intensité')
        self.graphWidget.setLabel('bottom', 'Longueur d\'onde [Å]')
        self.graphWidget.setTitle(title)
        self.toggle_balmer_lines()

    def display_header(self, header):
        self.table.setRowCount(len(header))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Clé', 'Valeur'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, (key, value) in enumerate(header.items()):
            self.table.setItem(i, 0, QTableWidgetItem(str(key)))
            self.table.setItem(i, 1, QTableWidgetItem(str(value)))

    def toggle_balmer_lines(self):
        if self.balmer_lines_action.isChecked():
            self.balmer_lines_items = []
            for line in self.balmer_lines:
                infinite_line = pg.InfiniteLine(pos=line, angle=90, pen=pg.mkPen('g', style=Qt.DashLine))
                self.graphWidget.addItem(infinite_line)
                self.balmer_lines_items.append(infinite_line)
        else:
            for item in self.balmer_lines_items:
                self.graphWidget.removeItem(item)
            self.balmer_lines_items = []


    def toggle_melchiors_spectrum(self):
        if not self.hd_number:
            QMessageBox.critical(self, "Erreur", "Numéro HD non trouvé dans le fichier FITS.")
            return

        if self.melchiors_spectrum_action.isChecked():
            
            print('resolution= ', self.resolution)
            if self.resolution > 5000:
                wavelengths, intensities = self.data_processor.plot_melchiors_HR(self.hd_number)
                self.hd_spectrum_item = self.graphWidget.plot(wavelengths, intensities, pen=pg.mkPen('r', style=Qt.DashLine))
            elif self.resolution < 5000:
                wavelengths, intensities = self.data_processor.plot_melchiors_BR(self.hd_number)
                self.hd_spectrum_item = self.graphWidget.plot(wavelengths, intensities, pen=pg.mkPen('r', style=Qt.DashLine))
        else:
            if self.hd_spectrum_item:
                self.graphWidget.removeItem(self.hd_spectrum_item)
                self.hd_spectrum_item = None


    def toggle_remove_atmo(self):
        if self.remove_atmo_action.isChecked():
            if not hasattr(self, 'wavelength') or not hasattr(self, 'spectrum'):
                QMessageBox.critical(self, "Erreur", "Veuillez d'abord ouvrir un fichier FITS.")
                self.remove_atmo_action.setChecked(False)
                return
            x = np.array(self.wavelength)
            y = np.array(self.spectrum)
            cleaned_wavelength, cleaned_spectrum,bkg = self.data_processor.remove_atmospheric_lines(x,y)

            # Plot the cleaned spectrum
            self.plot_spectrum(cleaned_wavelength, cleaned_spectrum, "Spectre sans raies atmosphériques")

            self.cleaned_wavelength = cleaned_wavelength
            self.cleaned_spectrum = cleaned_spectrum
            self.bkg = bkg

        else:
            if hasattr(self, 'wavelength') and hasattr(self, 'spectrum'):
                self.plot_spectrum(self.wavelength, self.spectrum, "Spectre original")

    def toggle_show_both_spectra(self):
            if self.show_both_spectra_action.isChecked():
                if hasattr(self, 'cleaned_wavelength') and hasattr(self, 'cleaned_spectrum'):
                    self.graphWidget.clear()
                    self.graphWidget.plot(self.cleaned_wavelength, self.cleaned_spectrum, pen='k', name="Spectre sans raies atmosphériques")
                    self.graphWidget.plot(self.wavelength, self.spectrum, pen=pg.mkPen('b', style=Qt.DashLine),name="Spectre original")
            else:
                if hasattr(self, 'wavelength') and hasattr(self, 'spectrum'):
                    self.plot_spectrum(self.wavelength, self.spectrum, "Spectre original")

    def toggle_show_baseline(self):
        if self.show_baseline_action.isChecked():
            self.graphWidget.plot(self.wavelength, self.bkg, pen=pg.mkPen('g', style=Qt.DashLine), name="Ligne de base")
        else:
            self.plot_spectrum(self.wavelength, self.spectrum, "Spectre original")

    def toggle_show_telluric_lines(self):
        if self.show_telluric_lines_action.isChecked():
            self.telluric_lines_items = []
            for line in self.telluric_lines:
                infinite_line = pg.InfiniteLine(pos=line, angle=90, pen=pg.mkPen('b', style=Qt.DashLine))
                self.graphWidget.addItem(infinite_line)
                self.telluric_lines_items.append(infinite_line)
        else:
            for item in self.telluric_lines_items:
                self.graphWidget.removeItem(item)
            self.telluric_lines_items = []


    
class ComparaisonPage(QWidget):
    def __init__(self):
        super(ComparaisonPage, self).__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # barre de menu
        self.menu_bar = QMenuBar(self)

        # menu "File"
        file_menu = QMenu("Fichier", self)
        self.menu_bar.addMenu(file_menu)

        # menu "Options"
        options_menu = QMenu("Options", self)
        self.menu_bar.addMenu(options_menu)


        # actions du menu "File"
        self.open_file_action = file_menu.addAction("Ouvrir des FITS 1D")
        #self.open_file_action.setCheckable(True)
        self.open_file_action.triggered.connect(self.open_files)


        # actionsd du menu "Options"
        self.choix_couleur_fond_action = options_menu.addAction("Couleur du background")
        self.choix_couleur_fond_action.setCheckable(True)
        self.choix_couleur_fond_action.triggered.connect(self.choose_background_color)

        self.choix_couleur_axe_action = options_menu.addAction("Couleur des axes")
        self.choix_couleur_axe_action.setCheckable(True)
        self.choix_couleur_axe_action.triggered.connect(self.choose_axis_color)

        self.choix_width_action = options_menu.addAction("Epaisseur des traits")
        self.choix_width_action.setCheckable(True)
        self.choix_width_action.triggered.connect(self.choose_line_thickness)

        self.remove_atmo_action = options_menu.addAction("Retirer les raies atmos")
        self.remove_atmo_action.setCheckable(True)
        self.remove_atmo_action.triggered.connect(self.toggle_remove_atmo)



        # Ajouter la barre de menu au layout principal
        main_layout.setMenuBar(self.menu_bar)


        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter, 1)

        self.graph_comp_Widget = pg.PlotWidget()
        self.splitter.addWidget(self.graph_comp_Widget)

        side_widget = QWidget()
        side_layout = QVBoxLayout()
        side_widget.setLayout(side_layout)
        self.splitter.addWidget(side_widget)

        self.graph_comp_Widget.setBackground("w")
        self.axis_pen_color = "k"
        self.line_thickness = 1

        self.update_axis_colors()
        self.legend = self.graph_comp_Widget.addLegend()

        self.colors = ["r", "g", "b", "c", "m", "y", "k"]
        self.plots = []

        self.data_processor = DataProcessor()

    def choose_background_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.graph_comp_Widget.setBackground(color.name())

    def choose_axis_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.axis_pen_color = color.name()
            self.update_axis_colors()

    def choose_line_thickness(self):
        thickness, ok = QInputDialog.getInt(self, "Choisir épaisseur", "Épaisseur des traits:", self.line_thickness, 1, 10)
        if ok:
            self.line_thickness = thickness
            self.update_existing_plots()

    def update_axis_colors(self):
        self.graph_comp_Widget.getAxis("left").setPen(self.axis_pen_color)
        self.graph_comp_Widget.getAxis("bottom").setPen(self.axis_pen_color)
        self.graph_comp_Widget.getAxis("left").setTextPen(self.axis_pen_color)
        self.graph_comp_Widget.getAxis("bottom").setTextPen(self.axis_pen_color)

    def update_existing_plots(self):
        for plot, color in self.plots:
            plot.setPen(pg.mkPen(color, width=self.line_thickness))

    def open_files(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Ouvrir des fichiers FITS 1D", "", "Fichiers FITS 1D (*.fits *.fit);;Tous les fichiers (*)")

        if file_names:
            self.graph_comp_Widget.clear()
            self.plots.clear()

            for i, file_name in enumerate(file_names):
                try:
                    wavelength, spectrum, title, hd_number,obj_name, date_obs, resolution = self.data_processor.process_file(file_name)
                    self.wavelength = wavelength
                    self.spectrum = spectrum
                    color = self.colors[i % len(self.colors)]
                    self.plot_spectrum(wavelength, spectrum, color, obj_name, date_obs)
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Erreur avec le fichier {file_name}: {str(e)}")

    def plot_spectrum(self, wavelength, spectrum, color, obj_name, date_obs):
        wavelength = np.asarray(wavelength)
        spectrum = np.asarray(spectrum)
        plot_item = self.graph_comp_Widget.plot(wavelength, spectrum, pen=pg.mkPen(color, width=self.line_thickness), name=obj_name + "_" + date_obs)
        self.plots.append((plot_item, color))
        self.graph_comp_Widget.setLabel("left", "Intensité")
        self.graph_comp_Widget.setLabel("bottom", 'Longueur d\'onde [Å]')

    def toggle_remove_atmo(self):
        if self.remove_atmo_action.isChecked():
            if not self.plots:
                QMessageBox.critical(self, "Erreur", "Veuillez d'abord ouvrir un ou plusieurs fichiers FITS.")
                self.remove_atmo_action.setChecked(False)
                return

            # Conserver une copie des spectres originaux
            self.original_plots = list(self.plots)
            
            self.graph_comp_Widget.clear()
            self.plots.clear()

            for plot_item, color in self.original_plots:
                try:
                    x = plot_item.getData()[0]  # Extraction des longueurs d'onde
                    y = plot_item.getData()[1]  # Extraction des spectres
                    
                    # Suppression des raies atmosphériques
                    cleaned_wavelength, cleaned_spectrum, bkg = self.data_processor.remove_atmospheric_lines(x, y)

                    # Affichage du spectre nettoyé
                    cleaned_plot = self.graph_comp_Widget.plot(cleaned_wavelength, cleaned_spectrum, pen=pg.mkPen(color, width=self.line_thickness), name="Spectre sans raies atmosphériques")
                    self.plots.append((cleaned_plot, color))

                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Erreur lors du traitement des raies atmosphériques: {str(e)}")
                    self.remove_atmo_action.setChecked(False)
                    return

        else:
            if not hasattr(self, 'original_plots'):
                QMessageBox.critical(self, "Erreur", "Aucune donnée d'origine n'est disponible.")
                self.remove_atmo_action.setChecked(False)
                return

            self.graph_comp_Widget.clear()
            self.plots.clear()

            # Réafficher les spectres originaux
            for plot_item, color in self.original_plots:
                x = plot_item.getData()[0]
                y = plot_item.getData()[1]
                original_plot = self.graph_comp_Widget.plot(x, y, pen=pg.mkPen(color, width=self.line_thickness), name="Spectre original")
                self.plots.append((original_plot, color))
            
            del self.original_plots  # Nettoyer les spectres originaux pour éviter des incohérences futures


class BDDPage(QWidget):
    def __init__(self):
        super().__init__()

        # Créer le layout principal
        main_layout = QHBoxLayout(self)

        # Créer le QSplitter avec un trait vertical
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: lightgray; width: 2px; }")
        main_layout.addWidget(splitter)

        # Créer la section gauche avec les boutons et le label
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Bouton pour choisir un lieu
        self.location_button = QPushButton("Choisir un lieu")
        self.location_button.clicked.connect(self.choose_location)
        left_layout.addWidget(self.location_button)

        # Bouton pour choisir une date avec un calendrier
        self.calendar_button = QPushButton("Choisir une date")
        self.calendar_button.clicked.connect(self.choose_date)
        left_layout.addWidget(self.calendar_button)

        # Bouton pour ouvrir la sélection des constellations
        self.constellation_button = QPushButton("Choisir les constellations")
        self.constellation_button.clicked.connect(self.choose_constellations)
        left_layout.addWidget(self.constellation_button)

        # Label pour afficher les constellations sélectionnées
        self.selected_constellations_label = QLabel("Constellations sélectionnées: Aucun")
        left_layout.addWidget(self.selected_constellations_label)

        left_layout.addStretch()

        # Ajouter le widget gauche au splitter
        splitter.addWidget(left_widget)

        # Créer la section droite avec le tableau
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.table = QTableWidget()
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Toujours afficher la barre de défilement verticale
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Afficher la barre de défilement horizontale si nécessaire

        right_layout.addWidget(self.table)

        # Ajouter le widget droit au splitter
        splitter.addWidget(right_widget)

        splitter.setSizes([150, 400])  # Taille initiale des panneaux

        # Charger les données dans le tableau
        self.load_data_to_table()

    def load_data_to_table(self):
        
        df = bess_request()

        # Configurer le tableau
        self.table.setRowCount(len(df))  # Définir le nombre de lignes total en fonction du DataFrame
        self.table.setColumnCount(len(df.columns) - 1)  # Ne pas inclure la colonne "bgcolor"
        self.table.setHorizontalHeaderLabels(df.columns.drop('bgcolor'))

        # Remplir le tableau avec les données du DataFrame
        for i in range(len(df)):
            for j, col in enumerate(df.columns.drop('bgcolor')):  # Exclure la colonne "bgcolor"
                item = QTableWidgetItem(str(df.iloc[i][col]))
                if col == 'date':
                    # Appliquer le code couleur à la cellule de la colonne "date"
                    color = df.iloc[i]['bgcolor']
                    if color:
                        item.setBackground(QColor(color))
                self.table.setItem(i, j, item)

        # Limiter la hauteur du tableau pour n'afficher que 20 lignes à la fois
        row_height = self.table.rowHeight(0)
        header_height = self.table.horizontalHeader().height()
        self.table.setFixedHeight(row_height * 20 + header_height)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def choose_location(self):
        print("Choisir un lieu via Google Maps")

    def choose_date(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Choisir une date")

        calendar = QCalendarWidget(dialog)
        calendar.setGridVisible(True)
        calendar.clicked.connect(lambda date: self.on_date_selected(dialog, date))

        layout = QVBoxLayout(dialog)
        layout.addWidget(calendar)
        dialog.exec_()

    def on_date_selected(self, dialog, date):
        print(f"Date choisie: {date.toString(Qt.ISODate)}")
        dialog.accept()

    def get_constellation_list(self):
        constellations =  [
            "Andromeda", "Antlia", "Apus", "Aquarius", "Aquila", "Ara", "Aries", "Auriga",
            "Bootes", "Caelum", "Camelopardalis", "Cancer", "Canes Venatici", "Canis Major",
            "Canis Minor", "Capricornus", "Carina", "Cassiopeia", "Centaurus", "Cepheus",
            "Cetus", "Chamaeleon", "Circinus", "Columba", "Coma Berenices", "Corona Australis",
            "Corona Borealis", "Corvus", "Crater", "Crux", "Cygnus", "Delphinus", "Dorado",
            "Draco", "Equuleus", "Eridanus", "Fornax", "Gemini", "Grus", "Hercules", "Horologium",
            "Hydra", "Hydrus", "Indus", "Lacerta", "Leo", "Leo Minor", "Lepus", "Libra",
            "Lupus", "Lynx", "Lyra", "Mensa", "Microscopium", "Monoceros", "Musca", "Norma",
            "Octans", "Ophiuchus", "Orion", "Pavo", "Pegasus", "Perseus", "Phoenix", "Pictor",
            "Pisces", "Piscis Austrinus", "Puppis", "Pyxis", "Reticulum", "Sagitta", "Sagittarius",
            "Scorpius", "Sculptor", "Scutum", "Serpens", "Sextans", "Taurus", "Telescopium",
            "Triangulum", "Triangulum Australe", "Tucana", "Ursa Major", "Ursa Minor", "Vela",
            "Virgo", "Volans", "Vulpecula"
        ]
        return constellations

    def choose_constellations(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Choisir les constellations")

        layout = QVBoxLayout(dialog)

        scroll_area = QScrollArea(dialog)
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        constellations = self.get_constellation_list()
        self.checkboxes = []

        for constellation in constellations:
            checkbox = QCheckBox(constellation)
            scroll_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        layout.addWidget(scroll_area)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.on_constellations_selected(dialog))
        layout.addWidget(ok_button)

        dialog.exec_()

    def on_constellations_selected(self, dialog):
        selected_constellations = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        if selected_constellations:
            self.selected_constellations_label.setText("Constellations sélectionnées: " + ", ".join(selected_constellations))
        else:
            self.selected_constellations_label.setText("Constellations sélectionnées: Aucun")
        dialog.accept()
