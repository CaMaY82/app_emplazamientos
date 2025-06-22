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

class UI_Busqueda(QWidget):
    def __init__(self):
        super().__init__()

        # Con el uso de DarkDetect se hace la condicional y se da el estilo a los widgets para una mejor UI
        
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
                    padding-left: 2px;
                    padding-top: 2px;
                    border: 1px inset gray;
                    }
                     """)
             
        else:
            app.setStyleSheet("""
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QPushButton, QTableWidget  {
            background-color: #eceff1;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 5px;
                }
                 QPushButton:pressed {
                    padding-left: 2px;
                    padding-top: 2px;
                    border: 1px inset gray;
        }
            """)

        self.setWindowTitle("Buscar")
        self.setMinimumSize(1100, 800)

        #Layoput de la ventana
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(3)  

        #Título
        titulo = QLabel("¿Qué Deseas Buscar?")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 16px")
        layout_principal.addWidget(titulo)
        layout_principal.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        #layout del frame superior (filtros)
        self.filtros_frame = QFrame()        
        filtros_layout = QGridLayout()
        filtros_layout.setSpacing(5)
        filtros_layout.setContentsMargins(0, 0, 0, 0)
      

        # Botones de opción
        self.botonEmp = QRadioButton("Emplazamientos")
        self.botonEmp.setLayoutDirection(Qt.RightToLeft)
       
        self.botonSF = QRadioButton("Solicitudes de Fabricación")
        self.botonSF.setLayoutDirection(Qt.RightToLeft)

        filtros_layout.addWidget(self.botonEmp, 0, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)
        filtros_layout.addWidget(self.botonSF, 1, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 1)

        self.botonEmp.toggled.connect(self.etiqueta_descripcion)
        self.botonSF.toggled.connect(self.etiqueta_descripcion)
        
        # Combo boxes

        # Combobox Sector
        self.sector_cb = QComboBox()
        self.sector_cb.addItem("Sector")
        self.sector_cb.model().item(0).setEnabled(False)
        sectores = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.sector_cb.addItems(sectores)
        
        filtros_layout.addWidget(self.sector_cb, 0, 2)
       
        # Combobox Planta
        self.planta_cb = QComboBox()
        self.planta_cb.addItem("Planta")
        self.planta_cb.model().item(0).setEnabled(False)

        self.filtros_frame.setLayout(filtros_layout)
        layout_principal.addWidget(self.filtros_frame)
        filtros_layout.addWidget(self.planta_cb, 1, 2)

        # ComboBox estado
        self.estado_cb = QComboBox()
        self.estado_cb.addItem("Estado Actual")
        self.estado_cb.addItem("")
        self.estado_cb.addItem("Vigente")
        self.estado_cb.addItem("Vencido")
        self.estado_cb.addItem("Atendido")
        self.estado_cb.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.estado_cb, 0, 3)

        # Combobox Status operativo
        self.status_cb = QComboBox()
        self.status_cb.addItem("Status Operativo")
        self.status_cb.addItem("Operando")
        self.status_cb.addItem("Fuera de Operación")
        self.status_cb.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.status_cb, 1, 3)

        # Combobox Riesgo
        self.riesgo_cb = QComboBox()
        self.riesgo_cb.addItem("Riesgo")
        riesgos = ["A", "B", "C", "D"]
        self.riesgo_cb.addItems(riesgos)
        self.riesgo_cb.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.riesgo_cb, 0, 4)
        self.riesgo_cb.setFixedWidth(200)

        # caja de texto para buscar emp o sf
        self.ID_busqueda = QLineEdit()
        self.ID_busqueda.setPlaceholderText("Ingresa el ID")
        self.ID_busqueda.setToolTip("Ingresa el número del EMP o SF que quieres buscar")
        self.ID_busqueda.setStyleSheet("""
         QToolTip {
        background-color: #FFFFFF;
        color: black;
        font-size: 16px;
        border: 1px solid black;
        }
        """)
        filtros_layout.addWidget(self.ID_busqueda, 1, 4)
        self.ID_busqueda.setFixedWidth(200)


        # botón buscar
        self.buscar_btn = QPushButton("BUSCAR 🔎")
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


        #layout del frame inferior (Datos de resultado)
        self.datos_item = QFrame()
        self.datos_layout = QGridLayout()
        self.datos_layout.setAlignment(Qt.AlignLeft)
        self.datos_item.setLayout(self.datos_layout)
        layout_principal.addWidget(self.datos_item)

        #cajas de texto de los resultados
        self.ID_resultado = QLineEdit()
        self.ID_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("ID:"), 0, 0)
        self.datos_layout.addWidget(self.ID_resultado, 1, 0)
        self.ID_resultado.setFixedWidth(75)

        self.sector_resultado = QLineEdit()
        self.sector_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Sector:"), 0, 1)
        self.datos_layout.addWidget(self.sector_resultado, 1, 1)
        self.sector_resultado.setFixedWidth(70)
        
        
        self.planta_resultado = QLineEdit()
        self.planta_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Planta:"), 0, 2)
        self.datos_layout.addWidget(self.planta_resultado, 1, 2)
        self.planta_resultado.setFixedWidth(127)                                            

        self.circuito_resultado = QLineEdit()
        self.circuito_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Circuito:"), 0, 3,)
        self.datos_layout.addWidget(self.circuito_resultado, 1, 3, 1, 2)
        

        self.UC_resultado = QLineEdit()
        self.UC_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Unidad de Control:"), 0, 5)
        self.datos_layout.addWidget(self.UC_resultado, 1, 5)
        

        self.status_resultado = QLineEdit()
        self.status_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Status Operativo:"), 0, 6)
        self.datos_layout.addWidget(self.status_resultado, 1, 6)
        
        self.vigencia_resultado = QLineEdit()
        self.vigencia_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Vigencia:"), 2, 0)
        self.datos_layout.addWidget(self.vigencia_resultado, 3, 0)
        self.vigencia_resultado.setFixedWidth(75)

        self.estado_resultado = QLineEdit()
        self.estado_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Estado:"), 2, 1)
        self.datos_layout.addWidget(self.estado_resultado, 3, 1)
        self.estado_resultado.setFixedWidth(70)

        self.mecanismo_resultado = QLineEdit()
        self.mecanismo_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Mecanismo de daño"), 2, 2)
        self.datos_layout.addWidget(self.mecanismo_resultado, 3, 2, 1, 2)
        
        
        self.material_resultado = QLineEdit()
        self.material_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Material:"), 2, 4)
        self.datos_layout.addWidget(self.material_resultado, 3, 4, 1, 1)
        
        
        self.SAP_resultado = QLineEdit()
        self.SAP_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Aviso SAP:"), 2, 5)
        self.datos_layout.addWidget(self.SAP_resultado, 3, 5)
       
        
        self.riesgo_resultado = QLineEdit()
        self.riesgo_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Clase de Riesgo:"), 2, 6)
        self.datos_layout.addWidget(self.riesgo_resultado, 3, 6)

        self.descripcion_resultado = QTextEdit()
        self.descripcion_resultado.setReadOnly(True)
        self.etiqueta_item = QLabel("Descripción:")
        self.datos_layout.addWidget(self.etiqueta_item, 4, 0, 1, 6)
        self.datos_layout.addWidget(self.descripcion_resultado, 5, 0, 1, 7)
        self.descripcion_resultado.setFixedHeight(80)

        self.mitigacion_resultado = QLineEdit()
        self.mitigacion_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Mitigación:"), 6, 0)
        self.datos_layout.addWidget(self.mitigacion_resultado, 7, 0, 1, 7)
        self.mitigacion_resultado.setFixedHeight(30)

        self.comentarios_resultado = QLineEdit()
        self.comentarios_resultado.setReadOnly(True)
        self.datos_layout.addWidget(QLabel("Comentarios:"), 8, 0)
        self.datos_layout.addWidget(self.comentarios_resultado, 9, 0, 1, 7)

        self.frame_inferior = QFrame()
        self.layout_inferior = QHBoxLayout()
        
        layout_principal.addWidget(self.frame_inferior)

        # Cuando el usuario cambie el tema de Windows, se detecta y se cambia el logo de IT adecuado con lo siguiente:


        if darkdetect.isDark():
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo_dark.png")
         logoIT = base_dir.parent / "assets" / "inspeccion_logo_dark.png"
        else:
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo.png")
         logoIT = base_dir.parent / "assets" / "inspeccion_logo.png"
         
        logo_inspeccion = QLabel()
        logo_inspeccion.setFixedSize(150, 75)
        logo_inspeccion.setScaledContents(True)
        
        pixmap = QPixmap(str(logoIT))
        logo_inspeccion.setPixmap(pixmap)

        self.frame_inferior.setLayout(self.layout_inferior)
        self.layout_inferior.addWidget(logo_inspeccion)
        self.layout_inferior.addStretch()
       
        # Agreganbdo botones con icono para ver el archivo del emplazamiento y las notificaciones de ejecución:

        icono_reporte = base_dir.parent / "assets" /"pdf_icon.png"
        self.reporte_btn = QToolButton()
        self.reporte_btn.setText("Ver Reporte")
        self.reporte_btn.setIcon(QIcon(str(icono_reporte)))
        self.reporte_btn.setIconSize(QSize(64, 64))
        self.reporte_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.reporte_btn.setFixedSize(100, 100)        
        self.reporte_btn.setFixedSize(100, 100)
        self.reporte_btn.setIconSize(QSize(64, 64))
        self.frame_inferior.setLayout(self.layout_inferior)
        self.layout_inferior.addWidget(self.reporte_btn)
        self.reporte_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            background-color: transparent;
            padding: 0;
            }
            
            """)
       
        icono_notificacion = base_dir.parent / "assets" /"notificacion_icon.png"
        self.notificacion_btn = QToolButton()
        self.notificacion_btn.setText("Ver Notificación")
        self.notificacion_btn.setIcon(QIcon(str(icono_notificacion)))
        self.notificacion_btn.setIconSize(QSize(64, 64))
        self.notificacion_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.notificacion_btn.setFixedSize(100, 100)
        self.frame_inferior.setLayout(self.layout_inferior)
        self.layout_inferior.addWidget(self.notificacion_btn)
        self.notificacion_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            background-color: transparent;
            padding: 0;
            }
           
            """)

        # Diccionario de sectores
        self.sectores_dict = {
            "1": ["", "BA", "MC", "FCC1", "MT2"],
            "2": ["", "U-502", "U-801", "U-901"],
            "3": ["", "U-300","U-500", "U-501", "U-600", "U-900"],
            "4": ["", "ALQUILACION", "TAME A", "TAME B", "MTBE A", "MTBE B", "ULSG A", "ULSG B", "CH", "U-100", "U-200"],
            "5": ["", "MD/MDJ", "PRETRATAMIENTO", "CL", "CT-1000N", "CT-1001N", "CT-1002N", "CT-1003N", "CT-1004N",
                  "DE-100", "DE-101", "DE-102", "DE-103", "MP", "CB2N", "CB3", "CB5", "CB6", "CB7", "CB8",
                  "ACUEDUCTO 3", "CHAIREL", "PATOS"],
            "6": ["", "MJA", "MJW", "MJN", "MFA", "MZ"],
            "7": ["", "MAYA", "FCC2"],
            "8": ["", "COQUER", "AMINA", "MT3", "AZUFRE", "AZUFRE 100", "AZUFRE 200", "AZUFRE 300", "AZUFRE 400"]
        }
        

       # Para conectar combo boxes, SECTOR y PLANTA se define la función:

        self.sector_cb.currentTextChanged.connect(self.actualizar_planta_Cbox)

        layout_principal.addStretch()

    def actualizar_planta_Cbox(self, sector):
        self.planta_cb.clear()
        planta = self.sectores_dict.get(sector)
        if planta:
            self.planta_cb.addItems(planta)

    

    def etiqueta_descripcion(self):
        if self.botonEmp.isChecked():
            tipo_item = "Descripción del Emplazamiento:"
            
        elif self.botonSF.isChecked():
            tipo_item = "Descripción de la Solicitud de Fabricación:"
            
        else:
            tipo_item = "Descripción:"
           

        self.etiqueta_item.setText(tipo_item)
       
           

    
if __name__ == "__main__":
   app = QApplication(sys.argv)
   ventana = QMainWindow()
   ventana.setWindowTitle("BUSCAR")
   base_dir = Path(__file__).resolve().parent
   icono_ventana = base_dir.parent / "assets" / "search_icon.ico"
   ui = UI_Busqueda()
   ventana.setCentralWidget(ui)
   ventana.setWindowIcon(QIcon(str(icono_ventana)))
   ventana.show()
   sys.exit(app.exec())