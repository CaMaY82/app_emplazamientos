from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox,
    QSizePolicy, QGridLayout, QLineEdit, QSpacerItem, QGroupBox, QDateEdit, QTextEdit, QMessageBox, QCalendarWidget, QScrollArea,  QToolButton
)
from PySide6.QtCore import Qt, QSize, QDate, Signal
from PySide6.QtGui import QIcon, QPixmap, QIntValidator
import darkdetect
import sys
from pathlib import Path
from datetime import datetime
from conexiondb import globalconn

class UI_Nuevo(QWidget):
    volver_home = Signal()

    def __init__(self, app):
        super().__init__()
        self.app = app


        

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
            
        self.setWindowTitle("REGISTRAR NUEVO")
        #self.setMinimumSize(800, 850)

        #Layoput de la ventana
        layout_principal = QVBoxLayout(self)
        seleccion_box = QGroupBox("Selecciona")
        seleccion_box.setFixedHeight(100)
        seleccion_layout = QHBoxLayout()
        #base_dir = Path(__file__).resolve().parent

        if darkdetect.isDark():
         logoIT = QPixmap("assets/inspeccion_logo_dark.png")
        else:
         logoIT = QPixmap("assets/inspeccion_logo.png")

        
        # Agregando botones de seleccion emp y sf
        self.boton_emp = QRadioButton("Emplazamiento")
        self.boton_sf = QRadioButton("Solicitud de Fabricación")
        self.logo = QLabel()
        self.logo.setFixedSize(170, 70)
        self.boton_emp.toggled.connect(self.generar_id)
        self.boton_sf.toggled.connect(self.generar_id)
        
        self.logo.setPixmap(logoIT)
        self.logo.setScaledContents(True)

        seleccion_box.setLayout(seleccion_layout)
        layout_principal.addWidget(seleccion_box, alignment=Qt.AlignTop)
        
        seleccion_layout.addWidget(self.boton_emp)
        seleccion_layout.addWidget(self.boton_sf)
        seleccion_layout.addSpacerItem(QSpacerItem(50, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        #seleccion_layout.addWidget(self.logo, alignment=Qt.AlignTop)

        
        #Sustitucion de logo IT por el icono de regresar
        icono_regresar = "assets/regresar_icon.png"       
        self.regresar = QToolButton()
        #self.regresar.setText("Regresar")
        self.regresar.setIcon(QIcon(str(icono_regresar)))
        self.regresar.setIconSize(QSize(50, 50))
        self.regresar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #self.regresar.setFixedSize(70, 30)
        self.regresar.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 12px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        
        seleccion_layout.addWidget(self.regresar, alignment=Qt.AlignTop)
        self.regresar.clicked.connect(self.volver_home.emit)

        self.frame_inferior = QFrame()
        self.layout_inferior = QGridLayout()
        self.layout_inferior.setHorizontalSpacing(100)
        self.frame_inferior.setLayout(self.layout_inferior)
        #layout_principal.addWidget(self.frame_inferior)
        #self.layout_inferior.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.frame2_inferior = QFrame()
        self.layout_inferior2 = QVBoxLayout()
        self.frame2_inferior.setLayout(self.layout_inferior2)
        #layout_principal.addWidget(self.frame2_inferior)

       

        
        
        # Agregando campos para captura de datos       

        self.ID = QLineEdit()
        self.layout_inferior.addWidget(QLabel("ID:"), 0, 0)
        self.layout_inferior.addWidget(self.ID, 1, 0)
        #self.ID.setFixedWidth(150)
        self.ID.setFixedHeight(25)
        self.ID.setReadOnly(True)
        self.ID.setStyleSheet("color: #5a7b8f;")

        sectores = (" ", "1", "2", "3", "4", "5", "6", "7", "8")

        self.sector = QComboBox()
        self.sector.addItems(sectores)
        self.sector.model().item(0).setEnabled(False)
        self.layout_inferior.addWidget(QLabel("Sector:"), 2, 0)
        self.sector.setFixedHeight(25)
        self.layout_inferior.addWidget(self.sector, 3, 0)

        self.planta = QComboBox()
        self.layout_inferior.addWidget(QLabel("Planta:"), 4, 0)
        self.layout_inferior.addWidget(self.planta, 5, 0)
        self.planta.setFixedHeight(25)

        self.circuito = QLineEdit()
        self.layout_inferior.addWidget(QLabel("Circuito:"), 6, 0)
        self.layout_inferior.addWidget(self.circuito,7, 0,)
        self.circuito.textChanged.connect(lambda text: self.circuito.setText(text.upper()))
        self.circuito.setFixedHeight(25)

        self.UC = QLineEdit()
        self.layout_inferior.addWidget(QLabel("Unidad de Control:"),8 ,0)
        self.layout_inferior.addWidget(self.UC, 9, 0)
        self.UC.textChanged.connect(lambda text: self.UC.setText(text.upper()))
        self.UC.setFixedHeight(25)

        self.material = QLineEdit()
        self.layout_inferior.addWidget(QLabel("Material:"), 0, 1)
        self.layout_inferior.addWidget(self.material, 1, 1)
        self.material.textChanged.connect(lambda text: self.material.setText(text.upper()))
        self.material.setFixedHeight(25)

        self.fecha_elab = QDateEdit()
        self.etiqueta_elab = QLabel("Fecha de Elaboración:")
        self.etiqueta_elab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.etiqueta_elab.setFixedWidth(150)
        self.layout_inferior.addWidget(self.etiqueta_elab, 2, 1)
        self.layout_inferior.addWidget(self.fecha_elab, 3, 1)
        self.fecha_elab.setFixedHeight(25)
        self.fecha_elab.setCalendarPopup(True)
        self.fecha_elab.setDate(QDate.currentDate())
        self.fecha_elab.setDisplayFormat("dd/MM/yyyy")
       
        self.fecha_ven = QDateEdit()
        self.layout_inferior.addWidget(QLabel("Fecha de Vencimiento:"), 4, 1)
        self.layout_inferior.addWidget(self.fecha_ven, 5, 1)
        self.fecha_ven.setFixedHeight(25)
        self.fecha_ven.setCalendarPopup(True)
        self.fecha_ven.setDate(QDate.currentDate())
        self.fecha_ven.setDisplayFormat("dd/MM/yyyy")
        
        self.SAP = QLineEdit()
        self.layout_inferior.addWidget(QLabel("Aviso SAP:"), 6, 1)
        self.layout_inferior.addWidget(self.SAP, 7, 1)
        self.SAP.setValidator(QIntValidator(0, 999999999))
        self.SAP.setFixedHeight(25)
              
        self.programa = QComboBox()
        self.programa.addItems((" ", "NO", "SÍ"))
        self.programa.model().item(0).setEnabled(False)
        self.layout_inferior.addWidget(QLabel("Programa de atención:"), 8, 1)
        self.layout_inferior.addWidget(self.programa, 9, 1)
        self.programa.setFixedHeight(25)

        self.iniciativa = QComboBox()
        self.iniciativa.addItems((" ", "NO", "SÍ"))
        self.iniciativa.model().item(0).setEnabled(False)
        self.layout_inferior.addWidget(QLabel("Iniciativa:"), 0, 2)
        self.layout_inferior.addWidget(self.iniciativa, 1, 2)
        self.iniciativa.setFixedHeight(25)

        self.paro_planta = QComboBox()
        self.paro_planta.addItems((" ", "SÍ", "NO"))
        self.paro_planta.model().item(0).setEnabled(False)
        self.layout_inferior.addWidget(QLabel("Paro de Planta:"), 2, 2)
        self.layout_inferior.addWidget(self.paro_planta, 3, 2)
        self.paro_planta.setFixedHeight(25)

        self.status = QComboBox()
        self.status.addItems((" ", "OPERANDO", "FUERA DE OPERACIÓN"))
        self.status.model().item(0).setEnabled(False)
        self.layout_inferior.addWidget(QLabel("Estado Operativo:"), 4, 2)
        self.layout_inferior.addWidget(self.status, 5, 2)
        self.status.setFixedHeight(25)
        
        self.riesgo = QComboBox()
        self.riesgo.addItems((" ","A", "B", "C", "D"))
        self.riesgo.model().item(0).setEnabled(False)
        self.layout_inferior.addWidget(QLabel("Clase de Riesgo:"), 6, 2)
        self.layout_inferior.addWidget(self.riesgo, 7, 2)
        self.riesgo.setFixedHeight(25)

        self.mecanismo = QComboBox()
        self.layout_inferior2.addWidget(QLabel("Mecanismo de Daño:"))
        self.layout_inferior2.addWidget(self.mecanismo)
        self.mecanismo.setFixedHeight(25)        

        self.descripcion = QTextEdit()
        self.descripcion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout_inferior2.addWidget(QLabel("Descripción:"))
        self.layout_inferior2.addWidget(self.descripcion)
        self.descripcion.textChanged.connect(self.convertir_descripcion_a_mayusculas)
        self.descripcion.setFixedHeight(45)

        self.mitigacion = QTextEdit()
        self.mitigacion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout_inferior2.addWidget(QLabel("Medida de Mitigación:"))
        self.layout_inferior2.addWidget(self.mitigacion)
        self.mitigacion.textChanged.connect(self.convertir_mitigacion_a_mayusculas)
        self.mitigacion.setFixedHeight(45)

        self.comentarios = QTextEdit()
        self.comentarios.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout_inferior2.addWidget(QLabel("Comentarios:"))
        self.layout_inferior2.addWidget(self.comentarios)
        self.comentarios.textChanged.connect(self.convertir_comentarios_a_mayusculas)
        self.comentarios.setFixedHeight(45)
        
        
        self.enlace = QLineEdit()
        self.layout_inferior2.addWidget(QLabel("Enlace al Archivo:"))
        self.layout_inferior2.addWidget(self.enlace)
        self.layout_inferior2.addSpacing(30)

        
       
        
        self.guardar_btn = QPushButton("GUARDAR")
        self.layout_inferior2.addStretch()
        self.layout_inferior2.addWidget(self.guardar_btn, alignment=Qt.AlignRight)
        self.guardar_btn.setFixedSize(150, 50)
        self.guardar_btn.clicked.connect(self.guardar_registro)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        contenedor_widget = QWidget()
        self.contenedor = QVBoxLayout(contenedor_widget)
        self.contenedor.addWidget(self.frame_inferior)
        self.contenedor.addWidget(self.frame2_inferior)
        self.scroll_area.setWidget(contenedor_widget)
        layout_principal.addWidget(self.scroll_area, stretch=1)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        

        
        
       
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
        

    

    def guardar_registro (self):

     try:
        if self.boton_emp.isChecked():
            tabla = "EMP"
            columna_id = "EMPLAZAMIENTO"
            descripcion_columna = '"DESCRIPCIÓN DEL EMPLAZAMIENTO"'
            enlace_columna = '"ENLACE EMP"'
        elif self.boton_sf.isChecked():
            tabla = "SF"
            columna_id = '"SOLICITUD DE FABRICACIÓN"'
            descripcion_columna = '"DESCRIPCIÓN DE LA SOLICITUD DE FABRICACIÓN"'
            enlace_columna = '"ENLACE SF"'
        else:
            return
        
        # Obtener valores del formulario
        id_value = self.ID.text().strip().replace("'", "''")
        sector_value = self.sector.currentText().strip().replace("'", "''")
        planta_value = self.planta.currentText().strip().replace("'", "''")
        circuito_value = self.circuito.text().strip().replace("'", "''")
        uc_value = self.UC.text().strip().replace("'", "''")
        descripcion_value = self.descripcion.toPlainText().strip().replace("'", "''")
        mecanismo_value = self.mecanismo.currentText().strip().replace("'", "''")
        material_value = self.material.text().strip().replace("'", "''")
        fecha_elab_value = self.fecha_elab.date().toString('yyyy-MM-dd')
        sap_value = self.SAP.text().strip().replace("'", "''")
        fecha_ven_value = self.fecha_ven.date().toString('yyyy-MM-dd')
        programa_value = self.programa.currentText().strip().replace("'", "''")
        iniciativa_value = self.iniciativa.currentText().strip().replace("'", "''")
        paro_value = self.paro_planta.currentText().strip().replace("'", "''")
        estado_actual = "VIGENTE"
        status_operativo = self.status.currentText().strip().replace("'", "''")
        riesgo_value = self.riesgo.currentText().strip().replace("'", "''")
        mitigacion_value = self.mitigacion.toPlainText().strip().replace("'", "''")
        observaciones_value = self.comentarios.toPlainText().strip().replace("'", "''")
        enlace_value = self.enlace.text().strip().replace("'", "''")

        # Validar campos obligatorios
        campos_obligatorios = [
            id_value, sector_value, planta_value, circuito_value, uc_value,
            descripcion_value, mecanismo_value, material_value, fecha_elab_value,
            sap_value, fecha_ven_value, programa_value, iniciativa_value, paro_value,
            estado_actual, status_operativo, riesgo_value, mitigacion_value
        ]

        if "" in campos_obligatorios or sector_value == " " or planta_value == " " or programa_value == " " or iniciativa_value == " " or paro_value == " " or estado_actual == " " or riesgo_value == " " or mecanismo_value == " ":
            QMessageBox.warning(self, "Campos Vacíos", "Por favor completa todos los campos obligatorios.")
            return

        # contruit el Query SQLite cloud
        

        query = f"""
            INSERT INTO {tabla} (
                {columna_id}, SECTOR, PLANTA, CIRCUITO, [UNIDAD DE CONTROL],
                {descripcion_columna}, [MECANISMO DE DAÑO], ESPECIFICACIÓN,
                [FECHA DE ELABORACIÓN], SAP, [FECHA DE VENCIMIENTO], [PROGRAMA DE ATENCIÓN],
                INICIATIVA, [PARO DE PLANTA], [FECHA DE ATENCIÓN], [ESTADO ACTUAL],
                [FECHA DE REEVALUACIÓN], [STATUS OPERATIVO], RIESGO, [MEDIDA DE MITIGACIÓN],
                [OBSERVACIONES GENERALES], {enlace_columna}
            )
           VALUES (
                    '{id_value}', '{sector_value}', '{planta_value}', '{circuito_value}', '{uc_value}',
                    '{descripcion_value}', '{mecanismo_value}', '{material_value}', '{fecha_elab_value}',
                    '{sap_value}', '{fecha_ven_value}', '{programa_value}', '{iniciativa_value}',
                    '{paro_value}', NULL, '{estado_actual}', NULL, '{status_operativo}',
                    '{riesgo_value}', '{mitigacion_value}', '{observaciones_value}', '{enlace_value}'
                )
            """

        globalconn.execute(query)

        if tabla == "EMP":
            mensaje = f"Emplazamiento {self.ID.text()} registrado correctamente"
        elif tabla == "SF":
            mensaje = f"Solicitud de Fabricación {self.ID.text()} registrada correctamente"

        QMessageBox.information(self,"Exito", mensaje)

        self.limpiar_formulario()
        self.limpiar_radio_buttons()

     except Exception as e:
        QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def generar_id(self):
        # Verifica cuál botón está activo
        if self.boton_emp.isChecked():
            tabla = "EMP"
            columna_id = "EMPLAZAMIENTO"
        elif self.boton_sf.isChecked():
            tabla = "SF"
            columna_id = "[SOLICITUD DE FABRICACIÓN]"
        else:
           return  # No hace nada si no hay botón seleccionado
        try:
            # Año actual
            anio_actual = datetime.now().year

            # Consulta los registros que ya existen de este año
            query = f"""
                SELECT {columna_id} FROM {tabla} 
                WHERE {columna_id} LIKE '%/{anio_actual}'
            """
            cursor = globalconn.execute(query)
            registros = cursor.fetchall()

            numeros_existentes = []
            for registro in registros:
                id_registrado = registro[0]
                numero = id_registrado.split('/')[0]  # Extrae el consecutivo
                if numero.isdigit():
                    numeros_existentes.append(int(numero))

            if numeros_existentes:
                nuevo_consecutivo = max(numeros_existentes) + 1
            else:
                nuevo_consecutivo = 1  # Primer registro del año

            # Formatear con ceros a la izquierda
            nuevo_id = f"{str(nuevo_consecutivo).zfill(3)}/{anio_actual}"

            # Mostrar el ID sugerido
            self.ID.setText(nuevo_id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el ID: {str(e)}")

    def convertir_descripcion_a_mayusculas(self):
            cursor = self.descripcion.textCursor()  # Guardar posición del cursor
            texto = self.descripcion.toPlainText()
            self.descripcion.blockSignals(True)  # Para evitar recursión infinita
            self.descripcion.setPlainText(texto.upper())
            self.descripcion.blockSignals(False)
            self.descripcion.setTextCursor(cursor)  # Restaurar posición del cursor

    def convertir_mitigacion_a_mayusculas(self):
            cursor = self.mitigacion.textCursor() 
            texto = self.mitigacion.toPlainText()
            self.mitigacion.blockSignals(True)  
            self.mitigacion.setPlainText(texto.upper())
            self.mitigacion.blockSignals(False)
            self.mitigacion.setTextCursor(cursor) 

    def convertir_comentarios_a_mayusculas(self):
            cursor = self.comentarios.textCursor() 
            texto = self.comentarios.toPlainText()
            self.comentarios.blockSignals(True) 
            self.comentarios.setPlainText(texto.upper())
            self.comentarios.blockSignals(False)
            self.comentarios.setTextCursor(cursor) 
        
    def limpiar_formulario(self):
        # Limpiar QLineEdit
        self.ID.clear()
        self.circuito.clear()
        self.UC.clear()
        self.material.clear()
        self.SAP.clear()
        self.enlace.clear()

    def limpiar_radio_buttons(self):
        for boton in [self.boton_emp, self.boton_sf]:
            boton.setAutoExclusive(False)
            boton.setChecked(False)
            boton.setAutoExclusive(True)

    # Resetear QComboBox
        self.sector.setCurrentIndex(0)
        self.planta.clear()
        self.programa.setCurrentIndex(0)
        self.iniciativa.setCurrentIndex(0)
        self.paro_planta.setCurrentIndex(0)
        self.status.setCurrentIndex(0)
        self.riesgo.setCurrentIndex(0)
        self.mecanismo.setCurrentIndex(0)

    # Limpiar QTextEdit
        self.descripcion.clear()
        self.mitigacion.clear()
        self.comentarios.clear()

    # Limpiar QDateEdit
        self.fecha_elab.setDate(QDate.currentDate())
        self.fecha_ven.setDate(QDate.currentDate())

    # Opcional: Resetear el radio button
        self.boton_emp.setChecked(False)
        self.boton_sf.setChecked(False)

    # Opcional: Volver a generar un ID vacío
        self.ID.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_Nuevo(app)
    window.show()
    sys.exit(app.exec())
