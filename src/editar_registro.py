from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, QToolButton, QTextEdit, QGroupBox, QDateEdit

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
            QLineEdit, QTextEdit, QComboBox, QTableWidget {
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
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QPushButton, QTableWidget {
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
        self.setMinimumSize(1150, 800)

         #Layoput de la ventana
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(3)  

        #Título
        #titulo = QLabel("¿QUÉ DESEAS EDITAR?")
        #titulo.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        #titulo.setStyleSheet("font-weight: bold; font-size: 16px")
        #layout_principal.addWidget(titulo)
        #layout_principal.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))


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
        self.botonEmp = QRadioButton("EMPLAZAMIENTO")
        self.botonEmp.setLayoutDirection(Qt.RightToLeft)
       
        self.botonSF = QRadioButton("SOLICITUD DE FABRICACIÓN")
        self.botonSF.setLayoutDirection(Qt.RightToLeft)

        filtros_layout.addWidget(self.botonEmp, 0, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)
        filtros_layout.addWidget(self.botonSF, 1, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 1)
        

        #self.botonEmp.toggled.connect(self.etiqueta_descripcion)
        #self.botonSF.toggled.connect(self.etiqueta_descripcion)
        
        # Combobox Sector
        self.sector_fl = QComboBox()
        self.sector_fl.addItem("SECTOR")
        self.sector_fl.model().item(0).setEnabled(False)
        sectores = [" ", "1", "2", "3", "4", "5", "6", "7", "8"]
        self.sector_fl.addItems(sectores)
        
        filtros_layout.addWidget(self.sector_fl, 0, 2)
       
        # Combobox Planta
        self.planta_fl = QComboBox()
        self.planta_fl.addItem("PLANTA")
        self.planta_fl.model().item(0).setEnabled(False)

        
        layout_principal.addWidget(grupo_filtros)
        filtros_layout.addWidget(self.planta_fl, 1, 2)

        # ComboBox estado
        self.estado_fl = QComboBox()
        self.estado_fl.addItem("ESTADO ACTUAL")
        self.estado_fl.addItem("")
        self.estado_fl.addItem("VIGENTE")
        self.estado_fl.addItem("VENCIDO")
        self.estado_fl.addItem("ATENDIDO")
        self.estado_fl.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.estado_fl, 0, 3)

        # Combobox Status operativo
        self.status_fl = QComboBox()
        self.status_fl.addItem("STATUS OPERATIVO")
        self.status_fl.addItem("OPERANDO")
        self.status_fl.addItem("FUERA DE OPERACIÓN")
        self.status_fl.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.status_fl, 1, 3)

        # Combobox Riesgo
        self.riesgo_fl = QComboBox()
        self.riesgo_fl.addItem("RIESGO")
        riesgos = ["A", "B", "C", "D"]
        self.riesgo_fl.addItems(riesgos)
        self.riesgo_fl.model().item(0).setEnabled(False)
        filtros_layout.addWidget(self.riesgo_fl, 0, 4)
        self.riesgo_fl.setFixedWidth(200)

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

        # Layout de edición
        self.frame_edicion = QFrame()
        edicion_layout = QGridLayout()
        edicion_layout.setAlignment(Qt.AlignCenter)
        self.frame_edicion.setLayout(edicion_layout)
        layout_principal.addWidget(self.frame_edicion)
        
        # Agregando controles de edición (widgets)

        self.ID = QLineEdit()
        self.ID.setReadOnly(True)
        self.ID.setFixedWidth(90)
        edicion_layout.addWidget(QLabel("ID:"), 0, 0)
        edicion_layout.addWidget(self.ID, 1, 0)
        
        self.sector = QComboBox()
        self.sector.addItems(sectores)
        self.sector.setFixedWidth(100)
        self.sector.model().item(0).setEnabled(False)
        edicion_layout.addWidget(QLabel("SECTOR:"), 0, 1)  
        edicion_layout.addWidget(self.sector, 1, 1)

        self.planta = QComboBox()
        self.planta.setFixedWidth(200)
        #self.planta.model().item(0).setEnabled(False)
        edicion_layout.addWidget(QLabel("PLANTA:"), 0, 2)
        edicion_layout.addWidget(self.planta, 1, 2)

        self.reevaluacion = QDateEdit()
        self.reevaluacion.setCalendarPopup(True)
        edicion_layout.addWidget(QLabel("REEVALUACION:"),0, 3)
        edicion_layout.addWidget(self.reevaluacion, 1, 3)
        self.reevaluacion.setFixedWidth(150)

        self.vigencia = QDateEdit()
        self.vigencia.setCalendarPopup(True)
        edicion_layout.addWidget(QLabel("VIGENCIA:"), 0, 4)
        edicion_layout.addWidget(self.vigencia, 1, 4)
        #self.vigencia.setFixedWidth(90)

        self.atencion = QDateEdit()
        self.atencion.setCalendarPopup(True)
        edicion_layout.addWidget(QLabel("ATENCION:"), 0, 5)
        edicion_layout.addWidget(self.atencion, 1, 5)
        #self.atencion.setFixedWidth(90)

        edicion_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 2, 0, 1, 5)

        self.estado = QLineEdit()
        self.estado.setReadOnly(True)
        edicion_layout.addWidget(QLabel("ESTADO:"), 3, 0)
        edicion_layout.addWidget(self.estado, 4, 0)
        self.estado.setFixedWidth(90)

        SI_NO = ("NO" ,"SI")

        self.paro_planta = QComboBox()
        self.paro_planta.addItems((SI_NO))
        edicion_layout.addWidget(QLabel("PARO DE PLANTA:"), 3, 1)
        edicion_layout.addWidget(self.paro_planta, 4, 1)
        #self.paro_planta.setFixedWidth(100)
        
        self.iniciativa = QComboBox()
        self.iniciativa.addItems((SI_NO))
        edicion_layout.addWidget(QLabel("INICIATIVA:"), 3, 2)
        edicion_layout.addWidget(self.iniciativa, 4, 2)
        #self.iniciativa.setFixedWidth(100)

        self.programa = QComboBox()
        self.programa.addItems(SI_NO)
        edicion_layout.addWidget(QLabel("PROGRAMA:"), 3, 3)
        edicion_layout.addWidget(self.programa, 4, 3)
        
        self.status = QComboBox()
        self.status.addItems(["OPERANDO", "FUERA DE OPERACIÓN"])
        edicion_layout.addWidget(QLabel("STATUS OPERATIVO:"), 3, 4)
        edicion_layout.addWidget(self.status, 4, 4)

        self.sap = QLineEdit()
        edicion_layout.addWidget(QLabel("AVISO SAP:"), 3, 5)
        edicion_layout.addWidget(self.sap, 4, 5)
        #self.sap.setFixedWidth(100)

        # Layout de edición 2
        self.frame_edicion2 = QFrame()
        edicion2_layout = QGridLayout()
        edicion2_layout.setAlignment(Qt.AlignLeft)
        self.frame_edicion2.setLayout(edicion2_layout)
        layout_principal.addWidget(self.frame_edicion2)

        self.mecanismo = QComboBox()
        edicion2_layout.addWidget(QLabel("MECANISMO DE DAÑO:"), 0, 0)
        edicion2_layout.addWidget(self.mecanismo, 1, 0,)

        self.material = QLineEdit()
        edicion2_layout.addWidget(QLabel("MATERIAL"), 0, 1)
        edicion2_layout.addWidget(self.material, 1, 1)

        self.mitigacion = QTextEdit()
        self.mitigacion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mitigacion.setFixedHeight(50)
        edicion2_layout.addWidget(QLabel("MEDIDA DE MITIGACIÓN:"), 2, 0, 1, 1)
        edicion2_layout.addWidget(self.mitigacion, 3, 0, 2, 2)

        self.descripcion = QTextEdit()
        self.descripcion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.descripcion.setFixedHeight(50)
        edicion2_layout.addWidget(QLabel("DESCRIPCION:"), 5, 0, 1, 1)
        edicion2_layout.addWidget(self.descripcion, 6, 0, 2, 1)

        self.comentarios = QTextEdit()
        self.comentarios.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.comentarios.setFixedHeight(50)
        edicion2_layout.addWidget(QLabel("COMENTARIOS:"), 5, 1, 1, 1)
        edicion2_layout.addWidget(self.comentarios, 6, 1, 2, 1)

        grupo_enlaces = QGroupBox("AGREGAR ENLACES DE LOS ARCHIVOS")
        enlaces_layout = QGridLayout()
        grupo_enlaces.setLayout(enlaces_layout)
        layout_principal.addWidget(grupo_enlaces)

        archivo_link = QLineEdit()
        enlaces_layout.addWidget(QLabel("ENLACE AL ARCHIVO:"), 0, 1, alignment=Qt.AlignRight)        
        enlaces_layout.addWidget(archivo_link, 0, 2)

        notificacion_link = QLineEdit()
        enlaces_layout.addWidget(QLabel("ENLACE A NOTIFICACION DE EJECUCION:"), 1, 1)
        enlaces_layout.addWidget(notificacion_link, 1, 2)

        botones_frame = QFrame()
        botones_layout = QHBoxLayout()
        botones_layout.setAlignment(Qt.AlignRight)
        botones_frame.setLayout(botones_layout)        
        layout_principal.addWidget(botones_frame)

        self.actualizar = QPushButton("ACTUALIZAR")
        self.actualizar.setFixedSize(200, 30)
        botones_layout.addWidget(self.actualizar)
        


        

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

        
        


        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_editar()
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon.ico"
    window.setWindowIcon(QIcon(str(icono_ventana)))

    window.show()
    sys.exit(app.exec())