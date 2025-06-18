from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, QToolButton, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt, QSize, QDate

from PySide6.QtGui import QIcon, QPixmap

import darkdetect

import sys

from pathlib import Path

class UI_editar(QWidget):
    def __init__(self):
        super().__init__()

        if darkdetect.isDark():
         modo = "oscuro"
       
        else:
         modo = "claro"

        if darkdetect.isDark():
         app.setStyleSheet("""
            QLineEdit, QTextEdit, QComboBox {
            background-color: #2e2e2e;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 5px;
              }
                QPushButton:pressed {
                 padding-right: 2px;
                 padding-bottom: 2px;
                 border: 1px inset gray;
                  }
                
             """)
        else:
            app.setStyleSheet("""
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QPushButton {
            background-color: #eceff1;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 5px;
                }
                  QPushButton:pressed {
                    padding-right: 2px;
                    padding-bottom: 2px;
                    border: 1px inset gray;
        }
            """)
            
        self.setWindowTitle("Editar Registro")
        self.setMinimumSize(800, 850)

         #Layoput de la ventana
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(3)  

        #Título
        titulo = QLabel("¿QUÉ DESEAS EDITAR?")
        titulo.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 16px")
        layout_principal.addWidget(titulo)
        layout_principal.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))


        # Layout de los filtros
        grupo_filtros = QGroupBox("SELECCIONA")
        grupo_filtros.setFixedHeight(100)
        
        
        filtros_layout = QGridLayout()
        base_dir = Path(__file__).resolve().parent

        if darkdetect.isDark():
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo_dark.png")
        else:
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo.png")

        
        grupo_filtros.setLayout(filtros_layout)
        layout_principal.addWidget(grupo_filtros, alignment=Qt.AlignTop)
       

        # Botones de opción
        self.botonEmp = QRadioButton("Emplazamientos")
        self.botonEmp.setLayoutDirection(Qt.RightToLeft)
       
        self.botonSF = QRadioButton("Solicitudes de Fabricaión")
        self.botonSF.setLayoutDirection(Qt.RightToLeft)

        filtros_layout.addWidget(self.botonEmp, 0, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)
        filtros_layout.addWidget(self.botonSF, 1, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 1)
        

        #self.botonEmp.toggled.connect(self.etiqueta_descripcion)
        #self.botonSF.toggled.connect(self.etiqueta_descripcion)
        
        # Combobox Sector
        self.sector_cb = QComboBox()
        self.sector_cb.addItem("SECTOR")
        self.sector_cb.model().item(0).setEnabled(False)
        sectores = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.sector_cb.addItems(sectores)
        
        filtros_layout.addWidget(self.sector_cb, 0, 2)
       
        # Combobox Planta
        self.planta_cb = QComboBox()
        self.planta_cb.addItem("PLANTA")
        self.planta_cb.model().item(0).setEnabled(False)

        
        layout_principal.addWidget(grupo_filtros)
        filtros_layout.addWidget(self.planta_cb, 1, 2)

        # ComboBox estado
        self.estado_cb = QComboBox()
        self.estado_cb.addItem("ESTADO ACTUAL")
        self.estado_cb.addItem("")
        self.estado_cb.addItem("VIGENTE")
        self.estado_cb.addItem("VENCIDO")
        self.estado_cb.addItem("ATENDIDO")
        self.estado_cb.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.estado_cb, 0, 3)

        # Combobox Status operativo
        self.status_cb = QComboBox()
        self.status_cb.addItem("STATUS OPERATIVO")
        self.status_cb.addItem("OPERANDO")
        self.status_cb.addItem("FUERA DE OPERACIÓN")
        self.status_cb.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.status_cb, 1, 3)

        # Combobox Riesgo
        self.riesgo_cb = QComboBox()
        self.riesgo_cb.addItem("RIESGO")
        riesgos = ["A", "B", "C", "D"]
        self.riesgo_cb.addItems(riesgos)
        self.riesgo_cb.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.riesgo_cb, 0, 4)
        self.riesgo_cb.setFixedWidth(200)

        # Boton buscar
        self.buscar_btn = QPushButton("Buscar 🔎")
        self.buscar_btn.setStyleSheet("font-weight: bold; font-size: 16px")
        self.buscar_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        filtros_layout.addWidget(self.buscar_btn, 0, 5, 2, 1)

        #layout del frame intermedio (lista de resultados)
        self.resultados = QFrame()
        resultados_layout = QGridLayout()

        # Lista de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(7)
        self.tabla_resultados.setHorizontalHeaderLabels(["ID", "PLANTA", "CIRCUITO", "UNIDAD DE CONTROL", "FECHA DE ELABORACIÓN", "FECHA DE VENCIMIENTO", "ESTADO ACTUAL"])
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        resultados_layout.addWidget(self.tabla_resultados)
        self.resultados.setLayout(resultados_layout)
        layout_principal.addWidget(self.resultados)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_editar()
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon.ico"
    window.setWindowIcon(QIcon(str(icono_ventana)))

    window.show()
    sys.exit(app.exec())