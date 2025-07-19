from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, QToolButton, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
import darkdetect
import sys
from pathlib import Path

from busqueda import UI_Busqueda
from nuevo_registro import UI_Nuevo
from login import loginUI


class MenuPrincipal(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        base_dir = Path(__file__).resolve().parent
        
        self.setWindowTitle("Menú Principal")
        self.resize(1800, 900)

        layout_principal = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)

        # Frame superior
        frame_sup = QFrame()
        layout_sup = QHBoxLayout()
        frame_sup.setLayout(layout_sup)
        layout_principal.addWidget(frame_sup, 0, 0, Qt.AlignTop)

        base_dir = Path(__file__).resolve().parent
        logoPMX = base_dir.parent / "assets" / "pemex_logo.png"
        pemex = QPixmap(str(logoPMX))

        logo_pemex = QLabel()
        logo_pemex.setFixedSize(200, 90)
        logo_pemex.setPixmap(pemex)
        logo_pemex.setScaledContents(True)
        layout_sup.addWidget(logo_pemex)

        titulo = QLabel("Bienvenidos al Sistema de Administración de Emplazamientos y Solicitudes de Fabricación de La Refinería Madero")
        titulo.setWordWrap(True)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 18px")
        layout_sup.addWidget(titulo, alignment=Qt.AlignCenter)

        if darkdetect.isDark():
            logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo_dark.png")
        else:
            logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo.png")

        logo_inspeccion = QLabel()
        logo_inspeccion.setFixedSize(200, 100)
        logo_inspeccion.setScaledContents(True)
        logo_inspeccion.setPixmap(logoIT)
        layout_sup.addWidget(logo_inspeccion)

        # --- Íconos y botones centrados (con tus nombres originales) ---
        central_widget_botones = QWidget()
        central_layout = QHBoxLayout()
        central_widget_botones.setLayout(central_layout)
        central_layout.setSpacing(80)

        # Buscar
        self.buscar_img = QLabel()
        self.buscar_img.setPixmap(QPixmap(base_dir.parent / "assets" / "buscar_icon.png"))
        self.buscar_img.setScaledContents(True)
        self.buscar_img.setFixedSize(100, 100)
        self.buscar = QPushButton("Buscar")
        #self.buscar.setFixedSize(150, 50)
        layout_buscar = QVBoxLayout()
        layout_buscar.addWidget(self.buscar_img, alignment=Qt.AlignCenter)
        layout_buscar.addWidget(self.buscar, alignment=Qt.AlignCenter)
        layout_buscar.addSpacing(15)
        buscar_widget = QWidget()
        buscar_widget.setLayout(layout_buscar)
        central_layout.addWidget(buscar_widget)
        self.buscar.clicked.connect(self.abrir_busqueda)

        # Editar
        self.editar_img = QLabel()
        self.editar_img.setPixmap(QPixmap(base_dir.parent / "assets" / "editar_icon.png"))
        self.editar_img.setScaledContents(True)
        self.editar_img.setFixedSize(100, 100)
        self.editar = QPushButton("Editar")
        self.editar.setFixedSize(150, 50)
        layout_editar = QVBoxLayout()
        layout_editar.addWidget(self.editar_img, alignment=Qt.AlignCenter)
        layout_editar.addWidget(self.editar, alignment=Qt.AlignCenter)
        layout_editar.addSpacing(15)
        editar_widget = QWidget()
        editar_widget.setLayout(layout_editar)
        central_layout.addWidget(editar_widget)
        self.editar.clicked.connect(self.abrir_editar)

        # Nuevo Registro
        self.nuevo_img = QLabel()
        self.nuevo_img.setPixmap(QPixmap(base_dir.parent / "assets" / "nuevo_icon.png"))
        self.nuevo_img.setScaledContents(True)
        self.nuevo_img.setFixedSize(100, 100)
        self.nuevo_registro = QPushButton("Nuevo Registro")
        self.nuevo_registro.setFixedSize(150, 50)
        layout_nuevo = QVBoxLayout()
        layout_nuevo.addWidget(self.nuevo_img, alignment=Qt.AlignCenter)
        layout_nuevo.addWidget(self.nuevo_registro, alignment=Qt.AlignCenter)
        layout_nuevo.addSpacing(15)
        nuevo_widget = QWidget()
        nuevo_widget.setLayout(layout_nuevo)
        central_layout.addWidget(nuevo_widget)

        # Dashboard
        self.dash_img = QLabel()
        self.dash_img.setPixmap(QPixmap(base_dir.parent / "assets" / "dashboard_icon.png"))
        self.dash_img.setScaledContents(True)
        self.dash_img.setFixedSize(100, 100)
        self.dashboard = QPushButton("Dashboard")
        self.dashboard.setFixedSize(150, 50)
        layout_dash = QVBoxLayout()
        layout_dash.addWidget(self.dash_img, alignment=Qt.AlignCenter)
        layout_dash.addWidget(self.dashboard, alignment=Qt.AlignCenter)
        layout_dash.addSpacing(15)
        dash_widget = QWidget()
        dash_widget.setLayout(layout_dash)
        central_layout.addWidget(dash_widget)

        # Salir
        self.salir_img = QLabel()
        self.salir_img.setPixmap(QPixmap(base_dir.parent / "assets" / "salir_icon.png"))
        self.salir_img.setScaledContents(True)
        self.salir_img.setFixedSize(100, 100)
        self.salir = QPushButton("Salir")
        self.salir.setFixedSize(150, 50)
        layout_salir = QVBoxLayout()
        layout_salir.addWidget(self.salir_img, alignment=Qt.AlignCenter)
        layout_salir.addWidget(self.salir, alignment=Qt.AlignCenter)
        layout_salir.addSpacing(15)
        salir_widget = QWidget()
        salir_widget.setLayout(layout_salir)
        central_layout.addWidget(salir_widget)

        layout_principal.addWidget(central_widget_botones, 1, 0, alignment=Qt.AlignCenter)
        
        central_layout.addStretch()
        central_layout.addWidget(buscar_widget)
        central_layout.addWidget(editar_widget)
        central_layout.addWidget(nuevo_widget)
        central_layout.addWidget(dash_widget)
        central_layout.addWidget(salir_widget)
        central_layout.addStretch()

    def abrir_busqueda(self):
        # Pasa self.app al crear la ventana de búsqueda
        self.ventana_busqueda = UI_Busqueda(self.app)
        self.ventana_busqueda.show()

    def nuevo_registro(self):
        self.ventana_nuevo = UI_Nuevo(self.app)
        self.ventana_nuevo.show()
        
    


    def abrir_editar(self):
        login = loginUI(app)
        if login.exec():  # Si login fue exitoso
            self.stacked.setCurrentWidget(self.editar_widget)
        else:
            QMessageBox.warning(self, "Acceso denegado", "Credenciales inválidas")

        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    if darkdetect.isDark():
        app.setStyleSheet("""
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2e2e2e;
                color: white;
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
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QPushButton, QTableWidget {
                background-color: #eceff1;
                color: black;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton:pressed {
                padding-left: 2px;
                padding-top: 2px;
                border: 1px inset gray;
            }
        """)

    ventana = MenuPrincipal(app)
    ventana.showMaximized()

    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon_2.ico"
    ventana.setWindowIcon(QIcon(str(icono_ventana)))

    sys.exit(app.exec())