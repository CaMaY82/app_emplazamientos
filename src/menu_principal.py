from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, QToolButton, QTextEdit
)
from PySide6.QtCore import Qt, QSize

from PySide6.QtGui import QIcon, QPixmap

import darkdetect

import sys

from pathlib import Path

class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.resize(1800, 900)
        layout_principal = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)
        frame_sup = QFrame()
        layout_sup = QHBoxLayout()
        frame_sup.setLayout(layout_sup)        
        layout_principal.addWidget(frame_sup, 0, 0, Qt.AlignTop)
        base_dir = Path(__file__).resolve().parent
        logoPMX = base_dir.parent / "assets" / "pemex_logo.png"
        pemex = QPixmap(str(logoPMX))
        logo_pemex = QLabel()
        logo_pemex.setFixedSize(400, 150)
        logo_pemex.setPixmap(pemex)
        logo_pemex.setScaledContents(True)
        layout_sup.addWidget(logo_pemex)

        titulo = QLabel("Bienvenidos al Sistema de Administración de Emplazamientos y Solicitudes de Fabricación de La Refinería Madero")
        titulo.setWordWrap(True)
        titulo.setAlignment(Qt.AlignCenter)
        layout_sup.addWidget(titulo, alignment=Qt.AlignCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 30px")

        if darkdetect.isDark():
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo_dark.png")
         logoIT = base_dir.parent / "assets" / "inspeccion_logo_dark.png"
        else:
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo.png")
         logoIT = base_dir.parent / "assets" / "inspeccion_logo.png"
         
        logo_inspeccion = QLabel()
        logo_inspeccion.setFixedSize(350, 150)
        logo_inspeccion.setScaledContents(True)        
        pixmap = QPixmap(str(logoIT))
        logo_inspeccion.setPixmap(pixmap)
        layout_sup.addWidget(logo_inspeccion)

        #botones e iconos centrales

        

        





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = MenuPrincipal()
    ventana.showMaximized()
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon_2.ico"
    ventana.setWindowIcon(QIcon(str(icono_ventana)))
    sys.exit(app.exec())