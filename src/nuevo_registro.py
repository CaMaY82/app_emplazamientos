from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, QToolButton, QGroupBox, QDateEdit
)
from PySide6.QtCore import Qt, QSize, QDate

from PySide6.QtGui import QIcon, QPixmap

import sys

from pathlib import Path

class UI_Nuevo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registrar Nuevo")
        self.setMinimumSize(1100, 930)

        #Layoput de la ventana
        layout_principal = QVBoxLayout(self)
        seleccion_box = QGroupBox("SELECCIONA")
        seleccion_box.setFixedHeight(100)
        seleccion_layout = QHBoxLayout()
        base_dir = Path(__file__).resolve().parent
        

        self.boton_emp = QRadioButton("EMPLAZAMIENTO")
        self.boton_sf = QRadioButton("SOLICITUD DE FABRICACIÓN")
        self.logo = QLabel()
        self.logo.setFixedSize(100, 50)
        logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo_dark.png")
        self.logo.setPixmap(logoIT)
        self.logo.setScaledContents(True)

        seleccion_box.setLayout(seleccion_layout)
        layout_principal.addWidget(seleccion_box, alignment=Qt.AlignTop)
        
        seleccion_layout.addWidget(self.boton_emp)
        seleccion_layout.addWidget(self.boton_sf)
        seleccion_layout.addSpacerItem(QSpacerItem(50, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        seleccion_layout.addWidget(self.logo)

        self.frame_inferior = QFrame()
        self.layout_inferior = QGridLayout()

        self.ID = QLineEdit()
        self.sector = QComboBox()
        self.planta = QComboBox()
        self.circuito = QLineEdit()
        self.fecha_elab = QDateEdit()
        self.fecha_ven = QDateEdit()
        self.SAP = QLineEdit
        self.programa = QComboBox()
        self.iniciativa = QComboBox()
        self.paro_planta = QComboBox()
        self.status = QComboBox()
        self.riesgo = QComboBox()
        self.mitigacion = QLineEdit()
        self.comentarios = QLineEdit()
        self.descripcion = QLineEdit()
        self.material = QLineEdit()
        self.mecanismo = QComboBox()
        self.enlace = QLineEdit()
        



        


        

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_Nuevo()
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon.ico"
    window.setWindowIcon(QIcon(str(icono_ventana)))

    window.show()
    sys.exit(app.exec_())
