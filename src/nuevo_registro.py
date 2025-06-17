from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, QToolButton, QGroupBox, QDateEdit, QTextEdit
)
from PySide6.QtCore import Qt, QSize, QDate

from PySide6.QtGui import QIcon, QPixmap

import sys

from pathlib import Path

class UI_Nuevo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registrar Nuevo")
        self.setMinimumSize(800, 850)

        #Layoput de la ventana
        layout_principal = QVBoxLayout(self)
        seleccion_box = QGroupBox("SELECCIONA")
        seleccion_box.setFixedHeight(100)
        seleccion_layout = QHBoxLayout()
        base_dir = Path(__file__).resolve().parent
        
        # Agregando botones de seleccion emp y sf
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
        self.layout_inferior.setHorizontalSpacing(100)
        self.frame_inferior.setLayout(self.layout_inferior)
        layout_principal.addWidget(self.frame_inferior)
        self.layout_inferior.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.frame2_inferior = QFrame()
        self.layout_inferior2 = QVBoxLayout()
        self.frame2_inferior.setLayout(self.layout_inferior2)
        layout_principal.addWidget(self.frame2_inferior)

       

        
        
        # Agregando campos para captura de datos

        

        self.ID = QLineEdit()
        self.layout_inferior.addWidget(QLabel("ID:"), 0, 0)
        self.layout_inferior.addWidget(self.ID, 1, 0)
        #self.ID.setFixedWidth(150)
        self.ID.setFixedHeight(25)

        sectores = (" ", "1", "2", "3", "4", "5", "6", "7", "8")

        self.sector = QComboBox()
        self.sector.addItems(sectores)
        self.layout_inferior.addWidget(QLabel("SECTOR:"), 2, 0)
        self.sector.setFixedHeight(25)
        self.layout_inferior.addWidget(self.sector, 3, 0)

        self.planta = QComboBox()
        self.layout_inferior.addWidget(QLabel("PLANTA:"), 4, 0)
        self.layout_inferior.addWidget(self.planta, 5, 0)
        self.planta.setFixedHeight(25)

        self.circuito = QLineEdit()
        self.layout_inferior.addWidget(QLabel("CIRCUITO:"), 6, 0)
        self.layout_inferior.addWidget(self.circuito,7, 0,)
        self.circuito.setFixedHeight(25)

        self.UC = QLineEdit()
        self.layout_inferior.addWidget(QLabel("UNIDAD DE CONTROL:"),8 ,0)
        self.layout_inferior.addWidget(self.UC, 9, 0)
        self.UC.setFixedHeight(25)

        self.material = QLineEdit()
        self.layout_inferior.addWidget(QLabel("MATERIAL:"), 0, 1)
        self.layout_inferior.addWidget(self.material, 1, 1)
        self.material.setFixedHeight(25)

        self.fecha_elab = QDateEdit()
        self.etiqueta_elab = QLabel("FECHA DE ELABORACIÓN:")
        self.etiqueta_elab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.etiqueta_elab.setFixedWidth(150)
        self.layout_inferior.addWidget(self.etiqueta_elab, 2, 1)
        self.layout_inferior.addWidget(self.fecha_elab, 3, 1)
        self.fecha_elab.setFixedHeight(25)
        self.fecha_elab.setCalendarPopup(True)
        self.fecha_elab.setDate(QDate.currentDate())
        self.fecha_elab.setDisplayFormat("dd/MM/yyyy")

        self.fecha_ven = QDateEdit()
        self.layout_inferior.addWidget(QLabel("FECHA DE VENCIMIENTO:"), 4, 1)
        self.layout_inferior.addWidget(self.fecha_ven, 5, 1)
        self.fecha_ven.setFixedHeight(25)
        self.fecha_ven.setCalendarPopup(True)
        self.fecha_ven.setDate(QDate.currentDate())
        self.fecha_ven.setDisplayFormat("dd/MM/yyyy")
        
        self.SAP = QLineEdit()
        self.layout_inferior.addWidget(QLabel("AVISO SAP:"), 6, 1)
        self.layout_inferior.addWidget(self.SAP, 7, 1)
        self.SAP.setFixedHeight(25)
              
        self.programa = QComboBox()
        self.programa.addItems(("NO", "SI"))
        self.layout_inferior.addWidget(QLabel("PROGRAMA DE ATENCIÓN:"), 8, 1)
        self.layout_inferior.addWidget(self.programa, 9, 1)
        self.programa.setFixedHeight(25)

        self.iniciativa = QComboBox()
        self.iniciativa.addItems(("No", "SI"))
        self.layout_inferior.addWidget(QLabel("INICIATIVA:"), 0, 2)
        self.layout_inferior.addWidget(self.iniciativa, 1, 2)
        self.iniciativa.setFixedHeight(25)

        self.paro_planta = QComboBox()
        self.paro_planta.addItems((" ", "SI", "NO"))
        self.layout_inferior.addWidget(QLabel("PARO DE PLANTA:"), 2, 2)
        self.layout_inferior.addWidget(self.paro_planta, 3, 2)
        self.paro_planta.setFixedHeight(25)

        self.status = QComboBox()
        self.status.addItems((" ", "OPERANDO", "FUERA DE OPERACIÓN"))
        self.layout_inferior.addWidget(QLabel("ESTADO OPERATIVO:"), 4, 2)
        self.layout_inferior.addWidget(self.status, 5, 2)
        self.status.setFixedHeight(25)
        
        self.riesgo = QComboBox()
        self.riesgo.addItems((" ","A", "B", "C", "D"))
        self.layout_inferior.addWidget(QLabel("CLASE DE RIESGO:"), 6, 2)
        self.layout_inferior.addWidget(self.riesgo, 7, 2)
        self.riesgo.setFixedHeight(25)

        self.mecanismo = QComboBox()
        self.layout_inferior2.addWidget(QLabel("MECANISMO DE DAÑO:"))
        self.layout_inferior2.addWidget(self.mecanismo)
        self.mecanismo.setFixedHeight(25)        

        self.descripcion = QTextEdit()
        self.descripcion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout_inferior2.addWidget(QLabel("DESCRIPCIÓN:"))
        self.layout_inferior2.addWidget(self.descripcion)
        self.descripcion.setFixedHeight(45)
        
        self.mitigacion = QTextEdit()
        self.mitigacion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout_inferior2.addWidget(QLabel("MEDIDA DE MITIGACION:"))
        self.layout_inferior2.addWidget(self.mitigacion)
        self.mitigacion.setFixedHeight(45)

        self.comentarios = QTextEdit()
        self.comentarios.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout_inferior2.addWidget(QLabel("COMENTARIOS:"))
        self.layout_inferior2.addWidget(self.comentarios)
        self.comentarios.setFixedHeight(45)
        
        
        self.enlace = QLineEdit()
        self.layout_inferior2.addWidget(QLabel("ENLACE AL ARCHIVO:"))
        self.layout_inferior2.addWidget(self.enlace)
        self.layout_inferior2.addSpacing(30)

        icono_guardar = base_dir.parent /"assets"/"save_icon.png"

        self.guardar_btn = QToolButton()
        self.guardar_btn.setFixedSize(64, 64)
        self.layout_inferior2.addStretch()
        self.layout_inferior2.addWidget(self.guardar_btn, alignment=Qt.AlignRight)
        self.guardar_btn.setIcon(QIcon(str(icono_guardar)))
        self.guardar_btn.setIconSize(QSize(64, 64))
        self.guardar_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.guardar_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            border: none;
            background-color: transparent;
            padding: 0;
            }
            QToolButton:hover {
            background-color: #333;
            }
            """)
        
        self.guardar2 = QPushButton("GUARDAR")
        self.layout_inferior2.addWidget(self.guardar2)
        self.guardar2.setFixedSize(50, 50)
        
        
        # Lista Mecanismos de Daño

        mecanismos = [" ",
         "FRAGILIZACIÓN A 885 °F (475 °C)",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN CÁUSTICA",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR ÁCIDO FLUORHÍDRICO EN ALEACIONES DE NÍQUEL",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR ÁCIDO POLITIONICO",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR AMINA",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR AMONÍACO",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR CARBONATOS",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR CLORUROS",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR ETANOL",
         "AGRIETAMIENTO POR CORROSIÓN BAJO TENSIÓN POR HIDRÓGENO EN ÁCIDO FLUORHÍDRICO",
         "AGRIETAMIENTO POR RELAJACIÓN DE ESFUERZOS (AGRIETAMIENTO POR RECALENTAMIENTO)",
         "AGRIETAMIENTO POR SOLDADURA DE METALES DISÍMILES",
         "ATAQUE POR HIDRÓGENO A ALTA TEMPERATURA",
         "CARBURIZACIÓN",
         "CAVITACIÓN",
         "CHOQUE TÉRMICO",
         "CORROSIÓN ATMOSFÉRICA",
         "CORROSIÓN BAJO AISLAMIENTO",
         "CORROSIÓN CÁUSTICA",
         "CORROSIÓN EN SUELO",
         "CORROSIÓN GALVÁNICA",
         "CORROSIÓN GRÁFICA DE HIERROS FUNDIDOS",
         "CORROSIÓN H2/H2S A ALTA TEMPERATURA",
         "CORROSIÓN INFLUENCIADA MICROBIOLÓGICAMENTE",
         "CORROSIÓN POR ÁCIDO CLORHÍDRICO",
         "CORROSIÓN POR ÁCIDO FLUORHÍDRICO",
         "CORROSIÓN POR ÁCIDO FOSFÓRICO",
         "CORROSIÓN POR ÁCIDO NAFTÉNICO",
         "CORROSIÓN POR ÁCIDO ORGÁNICO ACUOSO",
         "CORROSIÓN POR ÁCIDO SULFÚRICO",
         "CORROSIÓN POR AGUA AMARGA (ÁCIDA)",
         "CORROSIÓN POR AGUA DE CALDERA Y CONDENSADO DE VAPOR",
         "CORROSIÓN POR AGUA DE ENFRIAMIENTO",
         "CORROSIÓN POR AGUA DE PROCESO OXIGENADA",
         "CORROSIÓN POR AMINA",
         "CORROSIÓN POR BISULFURO DE AMONIO (AGUA AMARGA)",
         "CORROSIÓN POR CELDAS DE CONCENTRACIÓN",
         "CORROSIÓN POR CENIZAS DE COMBUSTIÓN",
         "CORROSIÓN POR CLORURO DE AMONIO Y CLORHIDRATO DE AMINA",
         "CORROSIÓN POR CO2",
         "CORROSIÓN POR FENOL (ÁCIDO CARBÓLICO)",
         "CORROSIÓN POR PUNTO DE ROCÍO DE GASES COMBUSTÓN",
         "CORROSIÓN POR SALMUERA",
         "DAÑO POR H2S HÚMEDO",
         "DEGRADACIÓN DE REFRACTARIO",
         "DESALEACIÓN",
         "DESCARBURIZACIÓN",
         "ENVEJECIMIENTO POR DEFORMACIÓN",
         "EROSIÓN/EROSIÓN-CORROSIÓN",
         "ESFEROIDIZACIÓN (ABLANDAMIENTO)",
         "FATIGA MECÁNICA (INCLUYENDO FATIGA INDUCIDA POR VIBRACIÓN)",
         "FATIGA POR CORROSIÓN",
         "FATIGA TÉRMICA",
         "FLUENCIA Y RUPTURA POR ESFUERZO",
         "FRACTURA FRÁGIL",
         "FRAGILIZACIÓN POR FASE SIGMA",
         "FRAGILIZACIÓN POR HIDRÓGENO",
         "FRAGILIZACIÓN POR LÍQUIDOS METÁLICOS",
         "FRAGILIZACIÓN POR TEMPLE",
         "GRAFITIZACIÓN",
         "HIDRURACIÓN DE TITANIO",
         "IGNICIÓN Y COMBUSTIÓN MEJORADAS POR OXÍGENO GASEOSO",
         "NITROCARBURACIÓN",
         "OXIDACIÓN",
         "PULVERIZACIÓN DE METALES",
         "RUPTURA POR SOBRECALENTAMIENTO A CORTO PLAZO",
         "SULFURACIÓN",
        "OTROS"]  

        self.mecanismo.addItems(mecanismos) 


        # Diccionario de sectores

        self.sectores_dict = {
            "1": ["BA", "MC", "FCC1", "MT2"],
            "2": ["U-502", "U-801", "U-901"],
            "3": ["U-300","U-500", "U-501", "U-600", "U-900"],
            "4": ["ALQUILACION", "TAME A", "TAME B", "MTBE A", "MTBE B", "ULSG A", "ULSG B", "CH", "U-100", "U-200"],
            "5": ["MD/MDJ", "PRETRATAMIENTO", "CL", "CT-1000N", "CT-1001N", "CT-1002N", "CT-1003N", "CT-1004N",
                  "DE-100", "DE-101", "DE-102", "DE-103", "MP", "CB2N", "CB3", "CB5", "CB6", "CB7", "CB8",
                  "ACUEDUCTO 3", "CHAIREL", "PATOS"],
            "6": ["MJA", "MJW", "MJN", "MFA", "MZ"],
            "7": ["MAYA", "FCC2"],
            "8": ["COQUER", "AMINA", "MT3", "AZUFRE", "AZUFRE 100", "AZUFRE 200", "AZUFRE 300", "AZUFRE 400"]
        }
        

       # Para conectar combo boxes, SECTOR y PLANTA se define la función:

        self.sector.currentTextChanged.connect(self.actualizar_planta_Cbox)

        layout_principal.addStretch()

    def actualizar_planta_Cbox(self, sector):
        self.planta.clear()
        planta = self.sectores_dict.get(sector)
        if planta:
            self.planta.addItems(planta)
        


        

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_Nuevo()
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon.ico"
    window.setWindowIcon(QIcon(str(icono_ventana)))

    window.show()
    sys.exit(app.exec())
