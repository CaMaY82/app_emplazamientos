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

        central_frame = QFrame()
        central_layout = QGridLayout()
        central_frame.setLayout(central_layout)
                
        
        buscar_icon = QPixmap(base_dir.parent / "assets" / "buscar_icon.png")
                
        self.buscar_img = QLabel()
        self.buscar_img.setFixedSize(150, 150)
        self.buscar_img.setScaledContents(True)
        self.buscar_img.setPixmap(buscar_icon)

        self.buscar = QPushButton("Buscar")
        self.buscar.setFixedSize(120, 50)
        layout_principal.addWidget(central_frame)
        central_layout.addWidget(self.buscar_img, 0, 0)
        central_layout.addWidget(self.buscar, 1, 0)

        editar_icon = QPixmap(base_dir.parent / "assets" / "editar_icon.png")

        self.editar_img = QLabel()
        self.editar_img.setFixedSize(150, 150)
        self.editar_img.setScaledContents(True)
        self.editar_img.setPixmap(editar_icon)
        
        
        self.editar = QPushButton("Editar")
        self.editar.setFixedSize(120, 50)
        central_layout.addWidget(self.editar_img, 0, 1)
        central_layout.addWidget(self.editar, 1, 1)

        nuevo_icon = QPixmap(base_dir.parent / "assets" / "nuevo_icon.png")

        self.nuevo_img = QLabel()
        self.nuevo_img.setFixedSize(150, 150)
        self.nuevo_img.setScaledContents(True)
        self.nuevo_img.setPixmap(nuevo_icon)

        self.nuevo_registro = QPushButton("Nuevo Registro")
        self.nuevo_registro.setFixedSize(120, 50)
        central_layout.addWidget(self.nuevo_img, 0, 2)
        central_layout.addWidget(self.nuevo_registro, 1, 2)

        dash_icon = QPixmap(base_dir.parent / "assets" / "dashboard_icon.png")

        self.dash_img = QLabel()
        self.dash_img.setFixedSize(150, 150)
        self.dash_img.setScaledContents(True)
        self.dash_img.setPixmap(dash_icon)



        self.dashboard = QPushButton("Dashboard")
        self.dashboard.setFixedSize(120, 50)
        central_layout.addWidget(self.dash_img, 0, 3)
        central_layout.addWidget(self.dashboard, 1, 3)

        salir_icon = QPixmap(base_dir.parent / "assets" / "salir_icon.png")

        self.salir_img = QLabel()
        self.salir_img.setFixedSize(150, 150)
        self.salir_img.setScaledContents(True)
        self.salir_img.setPixmap(salir_icon)

        self.salir = QPushButton("Salir")
        self.salir.setFixedSize(120, 50)
        central_layout.addWidget(self.salir_img, 0, 4)
        central_layout.addWidget(self.salir, 1, 4)


        

        





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = MenuPrincipal()
    ventana.show()
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon_2.ico"
    ventana.setWindowIcon(QIcon(str(icono_ventana)))
    sys.exit(app.exec())