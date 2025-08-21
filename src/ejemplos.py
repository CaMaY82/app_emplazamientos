from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QGridLayout, QMessageBox, QStackedWidget, QToolButton
)
from PySide6.QtCore import Qt, QSize
    # Si usas QSize: from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, QGuiApplication
import darkdetect
import sys
from pathlib import Path

# Tus módulos deben heredar de QWidget y aceptar `app` en el __init__
from busqueda import UI_Busqueda
from nuevo_registro import UI_Nuevo
from login import loginUI
from login_nuevo import login_nuevoUI


class MenuPrincipal(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        base_dir = Path(__file__).resolve().parent

        self.setWindowTitle("Menú Principal")
        self.resize(1280, 900)

        # ---- Layout central
        layout_principal = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)

        # ---- Header / barra superior
        frame_sup = QFrame()
        layout_sup = QHBoxLayout()
        frame_sup.setLayout(layout_sup)
        layout_principal.addWidget(frame_sup, 0, 0, Qt.AlignTop)

        logoPMX = base_dir.parent / "assets" / "pemex_logo.png"
        pemex = QPixmap(str(logoPMX))

        logo_pemex = QLabel()
        logo_pemex.setFixedSize(200, 90)
        logo_pemex.setPixmap(pemex)
        logo_pemex.setScaledContents(True)
        layout_sup.addWidget(logo_pemex)

        titulo = QLabel("Sistema de Administración de Emplazamientos y Solicitudes de Fabricación de la Refinería Madero")
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

        # ---- STACK: contenedor de páginas (home + módulos)
        self.stack = QStackedWidget()
        layout_principal.addWidget(self.stack, 1, 0)  # el stack ocupa la fila 1

        # ---- Página HOME (los botones grandes)
        central_widget_botones = QWidget()
        central_layout = QHBoxLayout()
        central_widget_botones.setLayout(central_layout)
        central_layout.setSpacing(80)
        central_layout.addStretch()

        # Buscar
        self.buscar_img = QLabel()
        self.buscar_img.setPixmap(QPixmap(base_dir.parent / "assets" / "buscar_icon.png"))
        self.buscar_img.setScaledContents(True)
        self.buscar_img.setFixedSize(100, 100)
        self.buscar = QPushButton("Buscar")
        self.buscar.setFixedSize(100, 50)
        layout_buscar = QVBoxLayout()
        layout_buscar.setContentsMargins(0,0,0,0)
        layout_buscar.addSpacing(2)
        layout_buscar.addWidget(self.buscar_img, alignment=Qt.AlignCenter)
        layout_buscar.addWidget(self.buscar, alignment=Qt.AlignCenter)
        buscar_widget = QWidget()
        buscar_widget.setLayout(layout_buscar)
        central_layout.addWidget(buscar_widget)
        self.buscar.clicked.connect(self.abrir_busqueda)

        # Editar (abre login)
        self.editar_img = QLabel()
        self.editar_img.setPixmap(QPixmap(base_dir.parent / "assets" / "editar_icon.png"))
        self.editar_img.setScaledContents(True)
        self.editar_img.setFixedSize(100, 100)
        self.editar = QPushButton("Editar")
        self.editar.setFixedSize(100, 50)
        layout_editar = QVBoxLayout()
        layout_editar.setContentsMargins(0,0,0,0)
        layout_editar.addSpacing(2)
        layout_editar.addWidget(self.editar_img, alignment=Qt.AlignCenter)
        layout_editar.addWidget(self.editar, alignment=Qt.AlignCenter)
        editar_widget = QWidget()
        editar_widget.setLayout(layout_editar)
        central_layout.addWidget(editar_widget)
        self.editar.clicked.connect(self.abrir_login_editar)

        # Nuevo Registro (abre login; tras validar, navega al módulo "nuevo")
        self.nuevo_img = QLabel()
        self.nuevo_img.setPixmap(QPixmap(base_dir.parent / "assets" / "nuevo_icon.png"))
        self.nuevo_img.setScaledContents(True)
        self.nuevo_img.setFixedSize(100, 100)
        self.nuevo_registro = QPushButton("Nuevo Registro")
        self.nuevo_registro.setFixedSize(100, 50)
        layout_nuevo = QVBoxLayout()
        layout_nuevo.setContentsMargins(0,0,0,0)
        layout_nuevo.addSpacing(2)
        layout_nuevo.addWidget(self.nuevo_img, alignment=Qt.AlignCenter)
        layout_nuevo.addWidget(self.nuevo_registro, alignment=Qt.AlignCenter)        
        nuevo_widget = QWidget()
        nuevo_widget.setLayout(layout_nuevo)
        central_layout.addWidget(nuevo_widget)
        self.nuevo_registro.clicked.connect(self.abrir_login_nuevo)

        # Dashboard (placeholder)
        self.dash_img = QLabel()
        self.dash_img.setPixmap(QPixmap(base_dir.parent / "assets" / "dashboard_icon.png"))
        self.dash_img.setScaledContents(True)
        self.dash_img.setFixedSize(100, 100)
        self.dashboard = QPushButton("Dashboard")
        self.dashboard.setFixedSize(100, 50)
        layout_dash = QVBoxLayout()
        layout_dash.setContentsMargins(0,0,0,0)
        layout_dash.addSpacing(2)
        layout_dash.addWidget(self.dash_img, alignment=Qt.AlignCenter)
        layout_dash.addWidget(self.dashboard, alignment=Qt.AlignCenter)        
        dash_widget = QWidget()
        dash_widget.setLayout(layout_dash)
        central_layout.addWidget(dash_widget)
        self.dashboard.clicked.connect(self.proximamente)

        #Buscar con Toolbutton
        icono_buscar = base_dir.parent / "assets" /"buscar_icon.png"
        self.buscar_btn = QToolButton()
        self.buscar_btn.setText("Buscar")
        self.buscar_btn.setIcon(QIcon(str(icono_buscar)))
        self.buscar_btn.setIconSize(QSize(64, 64))
        self.buscar_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.buscar_btn.setFixedSize(150, 200)        
        self.buscar_btn.setFixedSize(150, 200)
        self.buscar_btn.setIconSize(QSize(128, 128))
        self.buscar_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 24px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        layout_buscar.addWidget(self.buscar_btn, alignment=Qt.AlignCenter)
        self.buscar_btn.clicked.connect(self.abrir_busqueda)

        #Editar con toolbttton
        icono_editar = base_dir.parent / "assets" /"editar_icon.png"
        self.editar_btn = QToolButton()
        self.editar_btn.setText("Buscar")
        self.editar_btn.setIcon(QIcon(str(icono_editar)))
        self.editar_btn.setIconSize(QSize(64, 64))
        self.editar_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.editar_btn.setFixedSize(150, 200)        
        self.editar_btn.setFixedSize(150, 200)
        self.editar_btn.setIconSize(QSize(128, 128))
        self.editar_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 24px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        layout_editar.addWidget(self.editar_btn, alignment=Qt.AlignCenter)
        
        self.editar_btn.clicked.connect(self.abrir_login_editar)

        # Salir
        self.salir_img = QLabel()
        self.salir_img.setPixmap(QPixmap(base_dir.parent / "assets" / "salir_icon.png"))
        self.salir_img.setScaledContents(True)
        self.salir_img.setFixedSize(100, 100)
        self.salir = QPushButton("Salir")
        self.salir.setFixedSize(100, 50)
        layout_salir = QVBoxLayout()
        layout_salir.setContentsMargins(0,0,0,0)
        layout_salir.addSpacing(2)
        layout_salir.addWidget(self.salir_img, alignment=Qt.AlignCenter)
        layout_salir.addWidget(self.salir, alignment=Qt.AlignCenter)        
        salir_widget = QWidget()
        salir_widget.setLayout(layout_salir)
        central_layout.addWidget(salir_widget)
        self.salir.clicked.connect(self.salir_app)

        central_layout.addStretch()

        # ---- Agregar la HOME al stack (página 0)
        self.page_home = central_widget_botones
        self.stack.addWidget(self.page_home)

        # ---- Instanciar módulos y agregarlos al stack (páginas 1..n)
        self.busqueda = UI_Busqueda(self.app) # <-- importante: pasar self.app
        self.busqueda.volver_home.connect(self.ir_a_home)   
        self.nuevo = UI_Nuevo(self.app)
        self.stack.addWidget(self.busqueda)     # índice 1
        self.stack.addWidget(self.nuevo)        # índice 2

        # Página inicial
        self.stack.setCurrentWidget(self.page_home)

    # --------- Navegación interna del stack
    def abrir_busqueda(self):
        self.stack.setCurrentWidget(self.busqueda)

    def ir_a_busqueda(self):
        self.stack.setCurrentWidget(self.busqueda)

    def ir_a_nuevo(self):
        self.stack.setCurrentWidget(self.nuevo)
    
    def ir_a_home(self):
        self.stack.setCurrentWidget(self.page_home)

    # --------- Ventanas de login (externas al stack)
    def abrir_login_nuevo(self):
        self.login = login_nuevoUI(self.app)
        self.login.setWindowTitle("Iniciar sesión - Nuevo registro")
        self.login.setFixedSize(400, 600)

        base_dir = Path(__file__).resolve().parent
        icono = base_dir.parent / "assets" / "login icon.ico"
        self.login.setWindowIcon(QIcon(str(icono)))

        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.login.move(
            (screen.width() - self.login.width()) // 2,
            (screen.height() - self.login.height()) // 2
        )

        # Sugerencia: al validar en login_nuevoUI, emite una señal y conéctala aquí para:
        # self.ir_a_nuevo()
        self.login.show()

    def abrir_login_editar(self):
        self.login = loginUI(self.app)
        self.login.setFixedSize(400, 600)
        base_dir = Path(__file__).resolve().parent
        self.login.setWindowTitle("Iniciar Sesión")
        icono_ventana = base_dir.parent / "assets" / "login icon.ico"
        self.login.setWindowIcon(QIcon(str(icono_ventana)))

        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.login.move(
            (screen.width() - self.login.width()) // 2,
            (screen.height() - self.login.height()) // 2
        )

        # Igual que arriba: al validar, puedes navegar a una página de edición si la agregas al stack
        self.login.show()

    # --------- Utilidades
    def salir_app(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Salir")
        msg.setText("¿Estás seguro que deseas salir?")
        msg.setIcon(QMessageBox.Question)

        boton_si = msg.addButton("Sí", QMessageBox.YesRole)
        msg.addButton("No", QMessageBox.NoRole)

        msg.exec()

        if msg.clickedButton() == boton_si:
            QApplication.quit()

    def proximamente(self):
        QMessageBox.information(self, "Dashboard", "Estará disponible próximamente.")


if __name__ == "__main__":
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
    ventana.show()

    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon_2.ico"
    ventana.setWindowIcon(QIcon(str(icono_ventana)))

    sys.exit(app.exec())
