import numpy as np
from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                               QFileDialog, QMessageBox, QLabel, QStackedWidget, 
                               QTableWidget, QTableWidgetItem, QSplitter,QCheckBox, QHeaderView,QColorDialog, QInputDialog,QMenuBar,QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
import pyqtgraph as pg
from data_processing import DataProcessor
from image_analysis import ImageProcessor


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

        # # Ajouter une image ou un logo (facultatif)
        # logo = QLabel()
        # logo.setPixmap(QPixmap("images/logo.png").scaled(200, 200, Qt.KeepAspectRatio))
        # logo.setAlignment(Qt.AlignCenter)
        # home_layout.addWidget(logo)

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

        self.show_home()

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_graph_page(self):
        self.stacked_widget.setCurrentWidget(self.graph_page)

    def show_image_page(self):
        self.stacked_widget.setCurrentWidget(self.image_page)

    def show_comparaison_page(self):
        self.stacked_widget.setCurrentWidget(self.comparaison_page)



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


from PySide6.QtWidgets import QMenuBar, QMenu

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

        # self.hd_spectrum_hr_action = options_menu.addAction("Superposer le spectre Melchiors HR")
        # self.hd_spectrum_hr_action.setCheckable(True)
        # self.hd_spectrum_hr_action.triggered.connect(self.toggle_hd_spectrum_hr)

        # self.hd_spectrum_br_action = options_menu.addAction("Superposer le spectre Melchiors BR")
        # self.hd_spectrum_br_action.setCheckable(True)
        # self.hd_spectrum_br_action.triggered.connect(self.toggle_hd_spectrum_br)

        self.melchiors_spectrum_action = options_menu.addAction("Superposer le spectre Melchiors")
        self.melchiors_spectrum_action.setCheckable(True)
        self.melchiors_spectrum_action.triggered.connect(self.toggle_melchiors_spectrum)

        self.remove_atmo_action = options_menu.addAction("Retirer les raies atmosphériques")
        self.remove_atmo_action.setCheckable(True)
        self.remove_atmo_action.triggered.connect(self.toggle_remove_atmo)

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

    # def toggle_hd_spectrum_hr(self):
    #     if not self.hd_number:
    #         QMessageBox.critical(self, "Erreur", "Numéro HD non trouvé dans le fichier FITS.")
    #         return

    #     if self.hd_spectrum_hr_action.isChecked():
    #         wavelengths, intensities = self.data_processor.plot_melchiors_HR(self.hd_number)
    #         self.hd_spectrum_item = self.graphWidget.plot(wavelengths, intensities, pen=pg.mkPen('r', style=Qt.DashLine))
    #     else:
    #         if self.hd_spectrum_item:
    #             self.graphWidget.removeItem(self.hd_spectrum_item)
    #             self.hd_spectrum_item = None

    # def toggle_hd_spectrum_br(self):
    #     if not self.hd_number:
    #         QMessageBox.critical(self, "Erreur", "Numéro HD non trouvé dans le fichier FITS.")
    #         return

    #     if self.hd_spectrum_br_action.isChecked():
    #         wavelengths, intensities = self.data_processor.plot_melchiors_BR(self.hd_number)
    #         self.hd_spectrum_item = self.graphWidget.plot(wavelengths, intensities, pen=pg.mkPen('r', style=Qt.DashLine))
    #     else:
    #         if self.hd_spectrum_item:
    #             self.graphWidget.removeItem(self.hd_spectrum_item)
    #             self.hd_spectrum_item = None

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
            # Logic for removing atmospheric lines goes here
            pass
    
class ComparaisonPage(QWidget):
    def __init__(self):
        super(ComparaisonPage, self).__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.openFilesButton = QPushButton("Ouvrir un/des fichiers FITS 1D")
        self.openFilesButton.setIcon(QIcon("icons/open_file.png"))
        self.openFilesButton.clicked.connect(self.open_files)
        main_layout.addWidget(self.openFilesButton)

        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter, 1)

        self.graph_comp_Widget = pg.PlotWidget()
        self.splitter.addWidget(self.graph_comp_Widget)

        side_widget = QWidget()
        side_layout = QVBoxLayout()
        side_widget.setLayout(side_layout)
        self.splitter.addWidget(side_widget)

        self.bg_color_button = QPushButton("Choisir couleur de fond")
        side_layout.addWidget(self.bg_color_button)
        self.bg_color_button.clicked.connect(self.choose_background_color)

        self.axis_color_button = QPushButton("Choisir couleur des axes")
        side_layout.addWidget(self.axis_color_button)
        self.axis_color_button.clicked.connect(self.choose_axis_color)

        self.line_thickness_button = QPushButton("Choisir épaisseur des traits")
        side_layout.addWidget(self.line_thickness_button)
        self.line_thickness_button.clicked.connect(self.choose_line_thickness)

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
                    wavelength, spectrum, title, hd_number,obj_name, date_obs = self.data_processor.process_file(file_name)
                    color = self.colors[i % len(self.colors)]
                    self.plot_spectrum(wavelength, spectrum, color, obj_name, date_obs)
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Erreur avec le fichier {file_name}: {str(e)}")

    def plot_spectrum(self, wavelength, spectrum, color, obj_name, date_obs):
        wavelength = np.asarray(wavelength)
        spectrum = np.asarray(spectrum)
        spectrum = self.data_processor.remove_atmospheric_lines(wavelength, spectrum)
        plot_item = self.graph_comp_Widget.plot(wavelength, spectrum, pen=pg.mkPen(color, width=self.line_thickness), name=obj_name + "_" + date_obs)

        self.plots.append((plot_item, color))
        self.graph_comp_Widget.setLabel("left", "Intensité")
        self.graph_comp_Widget.setLabel("bottom", 'Longueur d\'onde [Å]')
