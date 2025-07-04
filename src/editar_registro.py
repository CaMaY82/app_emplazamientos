from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, 
    QToolButton, QTextEdit, QGroupBox, QDateEdit, QMessageBox, QScrollArea, QCalendarWidget, QDialog

)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QIcon, QPixmap
import darkdetect
import sys
from pathlib import Path
import sqlite3 as sql
from functools import partial

class CalendarioPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.calendario = QCalendarWidget()
        self.calendario.clicked.connect(self.seleccionar_fecha)
        
        layout = QVBoxLayout()
        layout.addWidget(self.calendario)
        self.setLayout(layout)

        self.fecha_seleccionada = None

    def seleccionar_fecha(self, fecha):
        self.fecha_seleccionada = fecha
        self.accept()


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

        self.db_path = str(Path(__file__).resolve().parent.parent / "db" / "EMP.db")

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
        grupo_filtros = QGroupBox("Selecciona")
        layout_principal.addWidget(grupo_filtros, stretch=10)
        grupo_filtros.setFixedHeight(120)
        
        
        filtros_layout = QGridLayout()
        base_dir = Path(__file__).resolve().parent

        if darkdetect.isDark():
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo_dark.png")
        else:
         logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo.png")

        
        grupo_filtros.setLayout(filtros_layout)
        layout_principal.addWidget(grupo_filtros, stretch=5)
       

        # Botones de opción
        self.botonEmp = QRadioButton("Emplazamiento")
        self.botonEmp.setLayoutDirection(Qt.RightToLeft)
       
        self.botonSF = QRadioButton("Solicitud de Fabricación")
        self.botonSF.setLayoutDirection(Qt.RightToLeft)

        filtros_layout.addWidget(self.botonEmp, 1, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)
        filtros_layout.addWidget(self.botonSF, 3, 0, alignment=Qt.AlignLeft)
        filtros_layout.addItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 1)
        

        #self.botonEmp.toggled.connect(self.etiqueta_descripcion)
        #self.botonSF.toggled.connect(self.etiqueta_descripcion)
        
        # Combobox Sector
        self.sector_fl = QComboBox()
        sectores = [" ", "1", "2", "3", "4", "5", "6", "7", "8"]
        self.sector_fl.addItems(sectores)
        filtros_layout.addWidget(QLabel("Sector:"), 0, 2)        
        filtros_layout.addWidget(self.sector_fl, 1, 2)
       
        # Combobox Planta
        self.planta_fl = QComboBox()
               
        layout_principal.addWidget(grupo_filtros)
        filtros_layout.addWidget(QLabel("Planta:"), 2, 2)
        filtros_layout.addWidget(self.planta_fl, 3, 2)

        # ComboBox estado
        self.estado_fl = QComboBox()
        self.estado_fl.addItem("")
        self.estado_fl.addItem("Vigente")
        self.estado_fl.addItem("Vencido")
        self.estado_fl.addItem("Atendido")
        filtros_layout.addWidget(QLabel("Estado:"), 0, 3)
        filtros_layout.addWidget(self.estado_fl, 1, 3)

        # Combobox Status operativo
        self.status_fl = QComboBox()
        self.status_fl.addItem(" ")
        self.status_fl.addItem("Operando")
        self.status_fl.addItem("Fuera de Operación")
        filtros_layout.addWidget(QLabel("Status Operativo:"), 2, 3)
        filtros_layout.addWidget(self.status_fl, 3, 3)

        # Combobox Riesgo
        self.riesgo_fl = QComboBox()
        riesgos = [" ", "A", "B", "C", "D"]
        self.riesgo_fl.addItems(riesgos)
        filtros_layout.addWidget(QLabel("Riesgo:"), 0, 4)        
        filtros_layout.addWidget(self.riesgo_fl, 1, 4)
        self.riesgo_fl.setFixedWidth(200)

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
        filtros_layout.addWidget(self.ID_busqueda, 3, 4)
        self.ID_busqueda.setFixedWidth(200)

        self.resultados_label = QLabel()
        filtros_layout.addWidget(self.resultados_label, 0, 5)
        self.resultados_label.setAlignment(Qt.AlignCenter)

        # Boton buscar
        self.buscar_btn = QPushButton("BUSCAR 🔎")
        self.buscar_btn.setStyleSheet("font-weight: bold; font-size: 16px")
        self.buscar_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        filtros_layout.addWidget(self.buscar_btn, 1, 5, 3, 1)
        self.buscar_btn.clicked.connect(self.buscar_en_db)

        
        #layout del frame intermedio (lista de resultados)
        self.resultados = QFrame()
        resultados_layout = QGridLayout()

        # Lista de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(7)
        self.tabla_resultados.setHorizontalHeaderLabels(["ID", "PLANTA", "CIRCUITO", "UNIDAD DE CONTROL", "FECHA DE ELABORACIÓN", "FECHA DE VENCIMIENTO", "ESTADO ACTUAL"])
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_resultados.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.tabla_resultados.itemSelectionChanged.connect(self.detalle_elemento)
        resultados_layout.addWidget(self.tabla_resultados)
        self.resultados.setLayout(resultados_layout)
        layout_principal.addWidget(self.resultados)

        # Layout de edición
        self.frame_edicion = QFrame()
        edicion_layout = QGridLayout()
        edicion_layout.setAlignment(Qt.AlignCenter)
        self.frame_edicion.setLayout(edicion_layout)
        #layout_principal.addWidget(self.frame_edicion)
        
        # Agregando controles de edición (widgets)

        self.ID = QLineEdit()
        self.ID.setReadOnly(True)
        self.ID.setFixedWidth(80)
        edicion_layout.addWidget(QLabel("ID:"), 0, 0)
        edicion_layout.addWidget(self.ID, 1, 0)
        
        self.sector = QComboBox()
        self.sector.addItems(sectores)
        self.sector.setFixedWidth(50)
        self.sector.model().item(0).setEnabled(False)
        edicion_layout.addWidget(QLabel("Sector:"), 0, 1)  
        edicion_layout.addWidget(self.sector, 1, 1)

        self.planta = QComboBox()
        self.planta.setFixedWidth(90)
        #self.planta.model().item(0).setEnabled(False)
        edicion_layout.addWidget(QLabel("Planta:"), 0, 2)
        edicion_layout.addWidget(self.planta, 1, 2)

        self.circuito = QLineEdit()
        edicion_layout.addWidget(QLabel("Circuito:"), 0, 3)
        edicion_layout.addWidget(self.circuito, 1, 3)

        self.UC = QLineEdit()
        edicion_layout.addWidget(QLabel("UC:"), 0, 4)
        edicion_layout.addWidget(self.UC, 1, 4)



        self.reevaluacion = QLineEdit()
        edicion_layout.addWidget(QLabel("Reevaluación:"),0, 5)
        edicion_layout.addWidget(self.reevaluacion, 1, 5)
        self.reevaluacion.setFixedWidth(100)

        icono_calendario = base_dir.parent / "assets" /"calendar_icon.png"
        self.calendario_reev = QToolButton()
        self.calendario_reev.setIcon(QIcon(str(icono_calendario)))
        self.calendario_reev.setIconSize(QSize(30, 30))
        self.calendario_reev.setFixedSize(30, 30)
        edicion_layout.addWidget(self.calendario_reev, 1, 6)
        self.calendario_reev.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            border: none;
            background-color: transparent;
            padding: 0;
            }
           
            """)

        
        self.vigencia = QLineEdit()
        edicion_layout.addWidget(QLabel("Vigencia:"), 0, 7)
        edicion_layout.addWidget(self.vigencia, 1, 7)
        self.vigencia.setFixedWidth(100)

        self.calendario_vig = QToolButton()
        self.calendario_vig.setIcon(QIcon(str(icono_calendario)))
        self.calendario_vig.setIconSize(QSize(30, 30))
        self.calendario_vig.setFixedSize(30, 30)
        edicion_layout.addWidget(self.calendario_vig, 1, 8)
        self.calendario_vig.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            border: none;
            background-color: transparent;
            padding: 0;
            }
           
            """)

        self.atencion = QLineEdit()
        edicion_layout.addWidget(QLabel("Atención:"), 0, 9)
        edicion_layout.addWidget(self.atencion, 1, 9)
        self.atencion.setFixedWidth(100)

        self.calendario_atn = QToolButton()
        self.calendario_atn.setIcon(QIcon(str(icono_calendario)))
        self.calendario_atn.setIconSize(QSize(30, 30))
        self.calendario_atn.setFixedSize(30, 30)
        edicion_layout.addWidget(self.calendario_atn, 1, 10)
        self.calendario_atn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            border: none;
            background-color: transparent;
            padding: 0;
            }
           
            """)
        
        self.calendario_reev.clicked.connect(lambda: self.abrir_calendario(self.reevaluacion, self.calendario_reev))
        self.calendario_vig.clicked.connect(lambda: self.abrir_calendario(self.vigencia, self.calendario_vig))
        self.calendario_atn.clicked.connect(lambda: self.abrir_calendario(self.atencion, self.calendario_atn))


    


        #edicion_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 2, 0, 1, 5)

        # Layout de edición 2
        self.frame_edicion2 = QFrame()
        edicion2_layout = QGridLayout()
        edicion2_layout.setAlignment(Qt.AlignLeft)
        self.frame_edicion2.setLayout(edicion2_layout)

        self.riesgo = QComboBox()
        self.riesgo.addItems((riesgos))
        self.riesgo.model().item(0).setEnabled(False)
        edicion2_layout.addWidget(QLabel("Riesgo:"), 0, 0)
        edicion2_layout.addWidget(self.riesgo, 1, 0)

        self.estado = QLineEdit()
        self.estado.setReadOnly(True)
        #edicion2_layout.addWidget(QLabel("Estado:"), 0, 1)
        #edicion2_layout.addWidget(self.estado, 1, 1)
        self.estado.setFixedWidth(90)

        SI_NO = (" ", "NO" ,"SI")

        self.paro_planta = QComboBox()
        self.paro_planta.addItems((SI_NO))
        self.paro_planta.model().item(0).setEnabled(False)
        edicion2_layout.addWidget(QLabel("Paro de Planta:"), 0, 2)
        edicion2_layout.addWidget(self.paro_planta, 1, 2)
        #self.paro_planta.setFixedWidth(100)
        
        self.iniciativa = QComboBox()
        self.iniciativa.addItems((SI_NO))
        self.iniciativa.model().item(0).setEnabled(False)
        edicion2_layout.addWidget(QLabel("Iniciativa:"), 0, 3)
        edicion2_layout.addWidget(self.iniciativa, 1, 3)
        #self.iniciativa.setFixedWidth(100)

        self.programa = QComboBox()
        self.programa.addItems(SI_NO)
        self.programa.model().item(0).setEnabled(False)
        edicion2_layout.addWidget(QLabel("Programa:"), 0, 4)
        edicion2_layout.addWidget(self.programa, 1, 4)
        
        self.status = QComboBox()
        self.status.addItems([" ", "OPERANDO", "FUERA DE OPERACIÓN"])
        self.status.model().item(0).setEnabled(False)
        edicion2_layout.addWidget(QLabel("Status Operativo:"), 0, 5)
        edicion2_layout.addWidget(self.status, 1, 5)

        self.sap = QLineEdit()
        edicion2_layout.addWidget(QLabel("Aviso SAP:"), 0, 6)
        edicion2_layout.addWidget(self.sap, 1, 6)
        self.sap.setFixedWidth(150)

        # Layout de edición 3
        self.frame_edicion3 = QFrame()
        edicion3_layout = QGridLayout()
        edicion3_layout.setAlignment(Qt.AlignLeft)
        self.frame_edicion3.setLayout(edicion3_layout)
        #layout_principal.addWidget(self.frame_edicion2)

        self.mecanismo = QComboBox()
        edicion3_layout.addWidget(QLabel("Mecanismo de Daño:"), 0, 0)
        edicion3_layout.addWidget(self.mecanismo, 1, 0,)

        self.material = QLineEdit()
        edicion3_layout.addWidget(QLabel("Material"), 0, 1)
        edicion3_layout.addWidget(self.material, 1, 1)

        self.descripcion = QTextEdit()
        self.descripcion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.descripcion.setFixedHeight(50)
        edicion3_layout.addWidget(QLabel("Descripción:"), 2, 0, 1, 1)
        edicion3_layout.addWidget(self.descripcion, 3, 0, 2, 2)

        self.mitigacion = QTextEdit()
        self.mitigacion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mitigacion.setFixedHeight(50)
        edicion3_layout.addWidget(QLabel("Mitigación:"), 5, 0, 1, 1)
        edicion3_layout.addWidget(self.mitigacion, 6, 0, 2, 1)

        self.comentarios = QTextEdit()
        self.comentarios.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.comentarios.setFixedHeight(50)
        edicion3_layout.addWidget(QLabel("Comentarios:"), 5, 1, 1, 1)
        edicion3_layout.addWidget(self.comentarios, 6, 1, 2, 1)

        grupo_enlaces = QGroupBox("Agregar enlaces a archivo:")
        enlaces_layout = QGridLayout()
        grupo_enlaces.setLayout(enlaces_layout)
        #layout_principal.addWidget(grupo_enlaces)

        self.archivo_link = QLineEdit()
        enlaces_layout.addWidget(QLabel("Enlace a Archivo:"), 0, 1, alignment=Qt.AlignRight)        
        enlaces_layout.addWidget(self.archivo_link, 0, 2)

        self.notificacion_link = QLineEdit()
        enlaces_layout.addWidget(QLabel("Enlace a la Notificación de Ejecución:"), 1, 1)
        enlaces_layout.addWidget(self.notificacion_link, 1, 2)

        icono_archivo = base_dir.parent / "assets" /"new_file.png"
        icono_notificacion = base_dir.parent / "assets" /"notificacion2_icon.png"

        self.archivo_btn = QToolButton()
        self.archivo_btn.setIcon(QIcon(str(icono_archivo)))
        self.archivo_btn.setIconSize(QSize(35, 35))
        self.archivo_btn.setFixedSize(35, 35)
        enlaces_layout.addWidget(self.archivo_btn, 0, 3)
        self.archivo_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            border: none;
            background-color: transparent;
            padding: 0;
            }
           
            """)
        
        self.notificacion_btn = QToolButton()
        self.notificacion_btn.setIcon(QIcon(str(icono_notificacion)))
        self.notificacion_btn.setIconSize(QSize(35, 35))
        self.notificacion_btn.setFixedSize(35, 35)
        enlaces_layout.addWidget(self.notificacion_btn, 1, 3)
        self.notificacion_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            border: none;
            background-color: transparent;
            padding: 0;
            }
           
            """)

        

        botones_frame = QFrame()
        botones_layout = QHBoxLayout()
        botones_layout.setAlignment(Qt.AlignRight)
        botones_frame.setLayout(botones_layout)        
        layout_principal.addWidget(botones_frame)

        self.actualizar = QPushButton("ACTUALIZAR")
        self.actualizar.setFixedSize(150, 40)
        botones_layout.addWidget(self.actualizar)

        self.actualizar.clicked.connect(self.actualizar_registro)


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        contenedor_widget = QWidget()
        self.contenedor = QVBoxLayout(contenedor_widget)
        self.contenedor.addWidget(self.frame_edicion)
        self.contenedor.addWidget(self.frame_edicion2)
        self.contenedor.addWidget(self.frame_edicion3)
        self.contenedor.addWidget(grupo_enlaces)
        self.contenedor.addWidget(botones_frame)

        self.scroll_area.setWidget(contenedor_widget)
        layout_principal.addWidget(self.scroll_area)
        #self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scroll_area.setMaximumHeight(600)

      

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

        # Conexión entre casmbio de comboboxes y funciones 
        self.sector_fl.currentTextChanged.connect(self.actualizar_planta_filtro)
        self.sector.currentTextChanged.connect(self.actualizar_planta_edicion)


    # Funciones para hacer que los comboboxes sector y planta en filtros y edicion cambnien

    def actualizar_planta_filtro(self, sector):
        self.planta_fl.clear()
        plantas = self.sectores_dict.get(sector, [])
        if plantas:
            self.planta_fl.addItems(plantas)

    def actualizar_planta_edicion(self, sector):
        self.planta.clear()
        plantas = self.sectores_dict.get(sector, [])
        if plantas:
            self.planta.addItems(plantas)

    #Función para abrir calendario

    def abrir_calendario(self, line_edit_objetivo, boton):
        calendario = CalendarioPopup(self)
        # Posición del botón
        boton_pos = boton.mapToGlobal(boton.rect().bottomLeft())
        # Tamaño del calendario
        tam_calendario = calendario.sizeHint()
        # Tamaño de la pantalla
        pantalla = QApplication.primaryScreen().geometry()
        nueva_posicion = boton_pos

        # 🔹 Verificar si cabe hacia abajo
        if boton_pos.y() + tam_calendario.height() > pantalla.height():
        # Mostrar arriba del botón
            nueva_posicion = boton.mapToGlobal(boton.rect().topLeft())
            nueva_posicion.setY(nueva_posicion.y() - tam_calendario.height() - 5)
        else:
        # Mostrar debajo del botón con margen
            nueva_posicion.setY(nueva_posicion.y() + 5)

        # 🔹 Verificar si cabe hacia la derecha
        if boton_pos.x() + tam_calendario.width() > pantalla.width():
        # Mover hacia la izquierda para que no se salga
            nueva_posicion.setX(pantalla.width() - tam_calendario.width() - 5)

        # 🔹 Mover calendario
        calendario.move(nueva_posicion)
        calendario.show()

        calendario.finished.connect(lambda: self.actualizar_fecha(calendario, line_edit_objetivo))


    def actualizar_fecha(self, calendario, line_edit_objetivo):
        fecha = calendario.fecha_seleccionada
        if fecha:
         line_edit_objetivo.setText(fecha.toString("yyyy-MM-dd")) 

        
    # Buscar en la base de datos:
    def buscar_en_db(self):
        if self.botonEmp.isChecked():
            tabla = "VISTA_EMP"
            columna_id = "EMPLAZAMIENTO"
            label_result = "Emplazamientos encontrados"
            
        elif self.botonSF.isChecked():
            tabla = "VISTA_SF"
            columna_id = "[SOLICITUD DE FABRICACIÓN]"
            label_result = "Solicitudes de fabricación encontradas"
            
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona lo que deseas buscar")
            return
       
        
        sector = self.sector_fl.currentText().upper()
        if sector in [" "]:
           sector = None # No se aplica filtro
        
        planta = self.planta_fl.currentText().upper()
        if planta in [" "]:
           planta = None

        estado = self.estado_fl.currentText().upper()
        if estado in [""]:
            estado = None
        if estado is None:
           filtro_base = "AND ([ESTADO] = 'VIGENTE' OR [ESTADO] = 'VENCIDO')"
        else:
           filtro_base = ""

        status = self.status_fl.currentText().upper()
        if status in [" "]:
           status = None
        
        riesgo = self.riesgo_fl.currentText().upper()
        if riesgo in [" "]:
           riesgo = None
        
        id_busqueda = self.ID_busqueda.text().strip()
        if id_busqueda == "":
           id_busqueda = None

        # creando la consulta
        if id_busqueda:
         query = f"""
         SELECT {columna_id}, PLANTA, CIRCUITO, [UNIDAD DE CONTROL], [FECHA DE ELABORACIÓN], [FECHA DE VENCIMIENTO], [ESTADO]
         FROM {tabla}
         WHERE {columna_id} = ?
         """
         valores = [id_busqueda]
        else:
            query = f"""
             SELECT {columna_id}, PLANTA, CIRCUITO, [UNIDAD DE CONTROL], [FECHA DE ELABORACIÓN], [FECHA DE VENCIMIENTO],
             [ESTADO] 
               
             FROM {tabla}
             WHERE 1=1
             {filtro_base}
            """
            valores = []

            if sector:
                query += "AND SECTOR = ?"
                valores.append(sector)
            if planta:
                query += "AND PLANTA = ?"
                valores.append(planta)
            if estado:
                query += " AND [ESTADO] = ?"
                valores.append(estado)
            if status:
                query += "AND [STATUS OPERATIVO] = ?"
                valores.append(status)
            if riesgo:
                query += "AND RIESGO = ?"
                valores.append(riesgo)
            if id_busqueda:
                query += f" AND {columna_id} = ?"
                valores.append(id_busqueda)
       
        # conectando a db
        conexion = sql.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute(query, valores)
        resultados = cursor.fetchall()
        conexion.close
        columnas = ["ID", "PLANTA", "CIRCUITO", "UNIDAD DE CONTROL", "ELABORACION", "VENCIMIENTO", "ESTADO ACTUAL"]
        self.tabla_resultados.setColumnCount(len(columnas))
        self.tabla_resultados.setHorizontalHeaderLabels(columnas)
        self.tabla_resultados.setRowCount(0)

        if resultados:
           
            for fila_idx, fila_datos in enumerate(resultados):
             print(f"Fila {fila_idx}: {fila_datos}")
             print(f"Resultados encontrados: {len(resultados)}")
             
             
             
             self.tabla_resultados.insertRow(fila_idx)
             
             for col_idx, dato in enumerate(fila_datos):
                    self.tabla_resultados.setItem(fila_idx, col_idx, QTableWidgetItem(str(dato)))
            self.tabla_resultados.resizeColumnsToContents()
            self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.resultados_label.setText(f"Encontrados {len(resultados)}")
            self.resultados_label.setVisible(True)

            if darkdetect.isDark():
              
              self.resultados_label.setStyleSheet("font-size: 16px; color: lightgreen; font-weight: bold;")
            else:
              self.resultados_label.setStyleSheet("font-size: 16px; color: teal; font-weight: bold;")

        else:
            QMessageBox.information(self, "Sin resultados", "No se encontraron registros.")

        #QMessageBox.information(self, "Resultados", f"  {len(resultados)} {label_result}")

        conexion.close()


     # funcion para actualizar los campos    
    def detalle_elemento(self):
        selected_items = self.tabla_resultados.selectedItems()

        if selected_items:
           
            id_seleccionado = selected_items[0].text()
            if self.botonEmp.isChecked():
                tabla = "VISTA_EMP"
                columna_id = "EMPLAZAMIENTO"
                descripcion = "DESCRIPCIÓN DEL EMPLAZAMIENTO"
                columna_id_tabla = "EMPLAZAMIENTO"
                enlace_archivo = "ENLACE EMP"
            elif self.botonSF.isChecked():
                tabla = "VISTA_SF"
                columna_id = "[SOLICITUD DE FABRICACIÓN]"
                descripcion = "DESCRIPCIÓN DE LA SOLICITUD DE FABRICACIÓN"
                columna_id_tabla = "SOLICITUD DE FABRICACIÓN"
                enlace_archivo = "ENLACE SF"
            else:
                return  
             
            conexion = sql.connect(self.db_path)
            conexion.row_factory = sql.Row
            cursor = conexion.cursor()

            # Consulta SQL para traer toda la información de ese registro
            cursor.execute(f"SELECT * FROM {tabla} WHERE {columna_id} = ?", (id_seleccionado,))
            resultado = cursor.fetchone()

            conexion.close()

        if resultado:
            # con esto se llenan los QlineEdit de resultados
            self.ID.setText(self.limpiar_valor(resultado[columna_id_tabla]))
            self.sector.setCurrentText(self.limpiar_valor(resultado['SECTOR']))
            self.planta.setCurrentText(self.limpiar_valor(resultado['PLANTA']))
            self.reevaluacion.setText(self.limpiar_valor(resultado['FECHA DE REEVALUACIÓN']))
            self.vigencia.setText(self.limpiar_valor(resultado['FECHA DE VENCIMIENTO']))
            self.atencion.setText(self.limpiar_valor(resultado['FECHA DE ATENCIÓN']))
            self.circuito.setText(self.limpiar_valor(resultado['CIRCUITO']))
            self.UC.setText(self.limpiar_valor(resultado['UNIDAD DE CONTROL']))
            self.estado.setText(self.limpiar_valor(resultado["ESTADO"]))
            self.status.setCurrentText(self.limpiar_valor(resultado['STATUS OPERATIVO']))
            self.programa.setCurrentText(self.limpiar_valor(resultado["PROGRAMA DE ATENCIÓN"]))
            self.paro_planta.setCurrentText(self.limpiar_valor(resultado['PARO DE PLANTA']))
            self.iniciativa.setCurrentText(self.limpiar_valor(resultado['INICIATIVA']))            
            self.mecanismo.setCurrentText(self.limpiar_valor(resultado["MECANISMO DE DAÑO"]))
            self.material.setText(self.limpiar_valor(resultado["ESPECIFICACIÓN"]))
            self.sap.setText(self.limpiar_valor(resultado["SAP"]))
            self.riesgo.setCurrentText(self.limpiar_valor(resultado["RIESGO"]))
            self.descripcion.setText(self.limpiar_valor(resultado[descripcion]))
            self.mitigacion.setText(self.limpiar_valor(resultado["MEDIDA DE MITIGACIÓN"]))
            self.comentarios.setText(self.limpiar_valor(resultado["OBSERVACIONES GENERALES"]))
            self.archivo_link.setText(self.limpiar_valor(resultado[enlace_archivo]))
            self.notificacion_link.setText(self.limpiar_valor(resultado["ENLACE NOT"]))



            # Asignar rutas de PDF a los ToolButtons
        if tabla == "EMP":
            ruta_pdf = resultado["ENLACE EMP"] if resultado["ENLACE EMP"] is not None else None
            print(f"Ruta EMP: {ruta_pdf}")

            if ruta_pdf and ruta_pdf.strip():
                try:
                    self.archivo_btn.clicked.disconnect()
                except TypeError:
                    pass

                self.archivo_btn.clicked.connect(partial(self.abrir_pdf, ruta_pdf))
                self.archivo_btn.setVisible(True)
            else:
             self.archivo_btn.setVisible(False)

        elif tabla == "SF":
            ruta_pdf = resultado["ENLACE SF"] if resultado["ENLACE SF"] is not None else None
            if ruta_pdf and ruta_pdf.strip():
               try:
                 self.archivo_btn.clicked.disconnect()
               except TypeError:
                 pass

               self.archivo_btn.clicked.connect(partial(self.abrir_pdf, ruta_pdf))
               self.archivo_btn.setVisible(True)
            else:
                self.archivo_btn.setVisible(False)

        ruta_notificacion = resultado["ENLACE NOT"]
        print(f"Ruta NOT: {ruta_notificacion}")

        if ruta_notificacion and ruta_notificacion.strip():
           try:
              self.notificacion_btn.clicked.disconnect()
           except TypeError:
                pass

           self.notificacion_btn.clicked.connect(partial(self.abrir_pdf, ruta_notificacion))
           self.notificacion_btn.setVisible(True)
            
        else:
            self.notificacion_btn.setVisible(False)
        
        
       

    def abrir_pdf(self, ruta):
        import webbrowser
        webbrowser.open(ruta)

    
    def limpiar_valor(self, resultado):#se usa cuando el campo tiene valor null, se pone un caracter en blanco ""
        return str(resultado) if resultado is not None else ""
    
    #funcion para actualizar
    def actualizar_registro(self):
     if not self.ID.text():
        QMessageBox.warning(self, "Advertencia", "No hay registro seleccionado para guardar.")
        return

     try:
        conexion = sql.connect(self.db_path)
        cursor = conexion.cursor()

        # Prepara los valores a actualizar
        datos_actualizados = {
            'SECTOR': self.sector.currentText(),
            'PLANTA': self.planta.currentText(),
            'FECHA DE REEVALUACIÓN': self.reevaluacion.text(),
            'FECHA DE VENCIMIENTO': self.vigencia.text(),
            'FECHA DE ATENCIÓN': self.atencion.text(),
            'CIRCUITO': self.circuito.text(),
            'UNIDAD DE CONTROL': self.UC.text(),
            'ESTADO ACTUAL': self.estado.text(),
            'STATUS OPERATIVO': self.status.currentText(),
            'PROGRAMA DE ATENCIÓN': self.programa.currentText(),
            'PARO DE PLANTA': self.paro_planta.currentText(),
            'INICIATIVA': self.iniciativa.currentText(),
            'MECANISMO DE DAÑO': self.mecanismo.currentText(),
            'ESPECIFICACIÓN': self.material.text(),
            'SAP': self.sap.text(),
            'RIESGO': self.riesgo.currentText(),
            'OBSERVACIONES GENERALES': self.comentarios.toPlainText(),
            'MEDIDA DE MITIGACIÓN': self.mitigacion.toPlainText(),
            'ENLACE NOT': self.notificacion_link.text(),
        }

        # Nombre correcto para la columna descripción
        if self.botonEmp.isChecked():
            tabla = "EMP"
            columna_id = "EMPLAZAMIENTO"
            datos_actualizados['DESCRIPCIÓN DEL EMPLAZAMIENTO'] = self.descripcion.toPlainText()
            datos_actualizados['ENLACE EMP'] = self.archivo_link.text()
            mensaje = "EMPLAZAMIENTO ACTUALIZADO"
         
            
        elif self.botonSF.isChecked():
            tabla = "SF"
            columna_id = "[SOLICITUD DE FABRICACIÓN]"
            datos_actualizados['DESCRIPCIÓN DE LA SOLICITUD DE FABRICACIÓN'] = self.descripcion.toPlainText()
            datos_actualizados['ENLACE SF'] = self.archivo_link.text()
            mensaje = "SOLICITUD DE FABRICACIÓN ACTUALIZADA"
            
        # Armar el query dinámico
        columnas = ', '.join([f"[{col}] = ?" for col in datos_actualizados.keys()])
        valores = list(datos_actualizados.values())
        valores = [v if v != '' else None for v in valores]

        # Ejecutar actualización
        query = f'UPDATE {tabla} SET {columnas} WHERE "{columna_id}" = ?'
        for i, valor in enumerate(valores, start=1):
            print(f"Parámetro {i}: {valor} ({type(valor)})")
        cursor.execute(query, valores + [self.ID.text])

        conexion.commit()
        conexion.close()

        QMessageBox.information(self, "Éxito", mensaje)

     except Exception as e:
        QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar los cambios:\n{e}")
    
       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_editar()
    #base_dir = Path(__file__).resolve().parent
    #icono_ventana = base_dir.parent / "assets" / "app_icon.ico"
    
    base_dir = Path(__file__).resolve().parent   

    if darkdetect.isDark():
        
        icono_ventana = base_dir.parent / "assets" / "edit_icon_dark.ico"
    else:
        
        icono_ventana = base_dir.parent / "assets" / "edit_icon_light.ico"    
    window.setWindowIcon(QIcon(str(icono_ventana)))

    window.showMaximized()
    sys.exit(app.exec())