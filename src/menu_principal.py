from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QGridLayout, QMessageBox, QStackedWidget, QToolButton, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup    
from PySide6.QtGui import QIcon, QPixmap, QGuiApplication, QCloseEvent, QAction
import darkdetect
import sys
from pathlib import Path

# Tus módulos deben heredar de QWidget y aceptar `app` en el __init__
from busqueda import UI_Busqueda
from nuevo_registro import UI_Nuevo
from login import loginUI
from login_nuevo import login_nuevoUI
from editar_registro import UI_editar
from dashboard import Dashboard

def slide_to(stacked, next_index, direction="left", duration=260, easing=QEasingCurve.OutCubic):
    """Transición deslizante entre páginas de un QStackedWidget."""
    if next_index < 0 or next_index == stacked.currentIndex():
        return
    if stacked.property("_animating"):
        return
    stacked.setProperty("_animating", True)

    curr  = stacked.currentWidget()
    nextw = stacked.widget(next_index)

    area = stacked.rect()
    w, h = area.width(), area.height()

    if direction == "left":
        start_next = QRect(-w, 0, w, h); end_next = QRect(0, 0, w, h); end_curr = QRect(w, 0, w, h)
    elif direction == "right":
        start_next = QRect(w, 0, w, h);  end_next = QRect(0, 0, w, h); end_curr = QRect(-w, 0, w, h)
    elif direction == "up":
        start_next = QRect(0, -h, w, h); end_next = QRect(0, 0, w, h); end_curr = QRect(0, h, w, h)
    else:  # "down"
        start_next = QRect(0, h, w, h);  end_next = QRect(0, 0, w, h); end_curr = QRect(0, -h, w, h)

    nextw.setGeometry(start_next)
    nextw.show()
    nextw.raise_()

    group = QParallelAnimationGroup(stacked)

    a_curr = QPropertyAnimation(curr, b"geometry")
    a_curr.setDuration(duration)
    a_curr.setEndValue(end_curr)
    a_curr.setEasingCurve(easing)

    a_next = QPropertyAnimation(nextw, b"geometry")
    a_next.setDuration(duration)
    a_next.setEndValue(end_next)
    a_next.setEasingCurve(easing)

    group.addAnimation(a_curr)
    group.addAnimation(a_next)

    def _finish():
        stacked.setCurrentIndex(next_index)
        curr.hide()
        nextw.setGeometry(0, 0, w, h)
        stacked.setProperty("_animating", False)

    group.finished.connect(_finish)
    group.start(QPropertyAnimation.DeleteWhenStopped)

#Animacion de Fade
def fade_to(stacked, next_index, duration=220, easing=QEasingCurve.OutCubic):
    if next_index < 0 or next_index == stacked.currentIndex():
        return
    nextw = stacked.widget(next_index)
    eff = QGraphicsOpacityEffect(nextw)
    nextw.setGraphicsEffect(eff)
    eff.setOpacity(0.0)
    stacked.setCurrentIndex(next_index)

    anim = QPropertyAnimation(eff, b"opacity", stacked)
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(easing)
    anim.start(QPropertyAnimation.DeleteWhenStopped)

    

class MenuPrincipal(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        base_dir = Path(__file__).resolve().parent

        #Barra de menú
        barra = self.menuBar()
        menu = barra.addMenu("SAESMA")
        # Crear acciones
        about = QAction("Acerca de...", self)
        about.triggered.connect(self.mostrar_acerca_de)
        salir = QAction("Salir", self)
        salir.triggered.connect(self.close)

        # Agregar acciones al menú
        menu.addAction(about)
        menu.addSeparator()
        menu.addAction(salir)
    
        self.setWindowTitle("Menú Principal")
        self.setMinimumSize(1050, 600)
        #self.resize(1280, 900)

        # ---- Layout central
        self.layout_principal = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.layout_principal)
        self.setCentralWidget(central_widget)

        # ---- Header / barra superior
        self.frame_sup = QFrame()
        self.layout_sup = QHBoxLayout()
        self.frame_sup.setLayout(self.layout_sup)
        self.layout_principal.addWidget(self.frame_sup, 0, 0, Qt.AlignTop)

        logoPMX = base_dir.parent / "assets" / "pemex_logo.png"
        pemex = QPixmap(str(logoPMX))

        logo_pemex = QLabel()
        logo_pemex.setFixedSize(200, 90)
        logo_pemex.setPixmap(pemex)
        logo_pemex.setScaledContents(True)
        self.layout_sup.addWidget(logo_pemex)

        if darkdetect.isDark():
            logoApp = QPixmap(base_dir.parent / "assets" / "app_logo.png")
        else:
            logoApp = QPixmap(base_dir.parent / "assets" / "app_logo.png")

        logo_app = QLabel()
        logo_app.setFixedSize(200, 100)
        logo_app.setScaledContents(True)
        logo_app.setPixmap(logoApp)
        logo_app.setToolTip("Sistema de Administración de Emplazamientos y Solicitudes de Fabricación Madero")
        logo_app.setStyleSheet("""
         QToolTip {
        background-color: #FFFFFF;
        color: black;
        font-size: 24px;
        border: 1px solid black;
        }
        """)
        self.layout_sup.addWidget(logo_app)

        self.titulo = QLabel("Sistema de Administración de Emplazamientos y Solicitudes de Fabricación de la Refinería Madero")
        self.titulo.setWordWrap(True)
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-weight: bold; font-size: 18px")
        #layout_sup.addWidget(self.titulo, alignment=Qt.AlignCenter)

        if darkdetect.isDark():
            logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo_dark.png")
        else:
            logoIT = QPixmap(base_dir.parent / "assets" / "inspeccion_logo.png")

        logo_inspeccion = QLabel()
        logo_inspeccion.setFixedSize(200, 100)
        logo_inspeccion.setScaledContents(True)
        logo_inspeccion.setPixmap(logoIT)
        self.layout_sup.addWidget(logo_inspeccion)

        # ---- STACK: contenedor de páginas (home + módulos)
        self.stack = QStackedWidget()
        self.layout_principal.addWidget(self.stack, 1, 0)  # el stack ocupa la fila 1

        # Para que el stack ocupe todo cuando se oculta el header
        self.layout_principal.setRowStretch(0, 0)  # header
        self.layout_principal.setRowStretch(1, 1)  # stack

        # ---- Página HOME (los botones grandes)
        central_widget_botones = QWidget()
        central_layout = QHBoxLayout()
        central_widget_botones.setLayout(central_layout)
        central_layout.setSpacing(80)
        central_layout.addStretch()

        # Buscar       
        layout_buscar = QVBoxLayout()
        layout_buscar.setContentsMargins(0,0,0,0)
        layout_buscar.addSpacing(2)       
        buscar_widget = QWidget()
        buscar_widget.setLayout(layout_buscar)
        central_layout.addWidget(buscar_widget)
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
            font-size: 18px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        layout_buscar.addWidget(self.buscar_btn, alignment=Qt.AlignCenter)
        self.buscar_btn.clicked.connect(self.abrir_busqueda)
       
        # Nuevo Registro (abre login; tras validar, navega al módulo "nuevo")
        layout_nuevo = QVBoxLayout()
        layout_nuevo.setContentsMargins(0,0,0,0)
        layout_nuevo.addSpacing(2)
        nuevo_widget = QWidget()
        nuevo_widget.setLayout(layout_nuevo)
        central_layout.addWidget(nuevo_widget)
        icono_nuevo = base_dir.parent / "assets" /"nuevo_icon.png"
        self.nuevo_btn = QToolButton()
        self.nuevo_btn.setText("Nuevo Registro")
        self.nuevo_btn.setIcon(QIcon(str(icono_nuevo)))
        self.nuevo_btn.setIconSize(QSize(64, 64))
        self.nuevo_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nuevo_btn.setFixedSize(150, 200)
        self.nuevo_btn.setIconSize(QSize(128, 128))
        self.nuevo_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 18px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        layout_nuevo.addWidget(self.nuevo_btn, alignment = Qt.AlignCenter)
        self.nuevo_btn.clicked.connect(self.abrir_login_nuevo)

        # Editar (abre login)
        layout_editar = QVBoxLayout()
        layout_editar.setContentsMargins(0,0,0,0)
        layout_editar.addSpacing(2)
        editar_widget = QWidget()
        editar_widget.setLayout(layout_editar)
        central_layout.addWidget(editar_widget)
        icono_editar = base_dir.parent / "assets" /"editar_icon.png"
        self.editar_btn = QToolButton()
        self.editar_btn.setText("Editar")
        self.editar_btn.setIcon(QIcon(str(icono_editar)))
        self.editar_btn.setIconSize(QSize(64, 64))
        self.editar_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.editar_btn.setFixedSize(150, 200)        
        self.editar_btn.setFixedSize(150, 200)
        self.editar_btn.setIconSize(QSize(128, 128))
        self.editar_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 18px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        layout_editar.addWidget(self.editar_btn, alignment=Qt.AlignCenter)        
        self.editar_btn.clicked.connect(self.abrir_login_editar)
        

        # Dashboard
        layout_dash = QVBoxLayout()
        layout_dash.setContentsMargins(0,0,0,0)
        layout_dash.addSpacing(2)
        dash_widget = QWidget()
        dash_widget.setLayout(layout_dash)
        central_layout.addWidget(dash_widget)
        icono_dashboard = base_dir.parent / "assets" /"dashboard_icon.png"
        self.dashboard_btn = QToolButton()
        self.dashboard_btn.setText("Dashboard")
        self.dashboard_btn.setIcon(QIcon(str(icono_dashboard)))
        self.dashboard_btn.setIconSize(QSize(64, 64))
        self.dashboard_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.dashboard_btn.setFixedSize(150, 200)
        self.dashboard_btn.setIconSize(QSize(128, 128))
        self.dashboard_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 18px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        layout_dash.addWidget(self.dashboard_btn, alignment = Qt.AlignCenter)
        self.dashboard_btn.clicked.connect(self.abrir_dashboard)   

        
        
        # Salir
        layout_salir = QVBoxLayout()
        layout_salir.setContentsMargins(0,0,0,0)
        layout_salir.addSpacing(2)
        salir_widget = QWidget()
        salir_widget.setLayout(layout_salir)
        central_layout.addWidget(salir_widget)
        icono_salir = base_dir.parent / "assets" /"salir_icon.png"
        self.salir_btn = QToolButton()
        self.salir_btn.setText("Salir")
        self.salir_btn.setIcon(QIcon(str(icono_salir)))
        self.salir_btn.setIconSize(QSize(64, 64))
        self.salir_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.salir_btn.setFixedSize(150, 200)
        self.salir_btn.setIconSize(QSize(128, 128))
        self.salir_btn.setStyleSheet("""
        QToolButton {
            font-weight: normal;
            font-size: 18px;
            background-color: transparent;
            border: 0px solid rgba(0,0,0,35);
            border-radius: 12px;
            padding: 10px 12px;
            }
            
            """)
        #layout_salir.addWidget(self.salir_btn, alignment = Qt.AlignCenter)
        #self.salir_btn.clicked.connect(self.salir_app)
        self.salir_btn.clicked.connect(self.close)

        central_layout.addStretch()       

        # ---- Agregar la HOME al stack (página 0)
        self.page_home = central_widget_botones
        self.stack.addWidget(self.page_home)

        # ---- Instanciar módulos y agregarlos al stack (páginas 1..n)
        self.busqueda = UI_Busqueda(self.app) # <-- importante: pasar self.app
        self.busqueda.volver_home.connect(self.ir_a_home)   
        self.nuevo = UI_Nuevo(self.app)
        self.nuevo.volver_home.connect(self.ir_a_home)
        self.editar = UI_editar(self.app)
        self.editar.volver_home.connect(self.ir_a_home)
        self.dashboard = Dashboard(self.app)
        self.dashboard.volver_home.connect(self.ir_a_home)
        self.stack.addWidget(self.busqueda)     # índice 1
        self.stack.addWidget(self.nuevo)        # índice 2
        self.stack.addWidget(self.editar)       # índice 3
        self.stack.addWidget(self.dashboard)    # índice 4

        self.titulos_por_pagina = {
            self.page_home: "Sistema De Administración De Emplazamientos \n&\n Solicitudes De Fabricación \nDe Refinería Madero",
            self.busqueda:  "BUSCAR REGISTRO",
            self.nuevo:     "REGISTRAR NUEVO",
            self.editar: "EDITAR REGISTRO", 
        }

        # Reaccionar al cambio de página
        self.stack.currentChanged.connect(self.actualizar_titulo)

        # Página inicial + título inicial
        self.stack.setCurrentWidget(self.page_home)
        self.actualizar_titulo(self.stack.currentIndex())

    def actualizar_titulo(self, idx: int):
        w = self.stack.widget(idx)
        texto = self.titulos_por_pagina.get(w, "Aplicación")
        self.titulo.setText(texto)
        self.setWindowTitle(f"{texto} — SAESMA")  # opcional

    # --------- Navegación interna del stack
    def abrir_busqueda(self):
        self.frame_sup.hide()
        self.busqueda.limpiar_resultados()
        #self.stack.setCurrentWidget(self.busqueda)
        idx = self.stack.indexOf(self.busqueda)
        slide_to(self.stack, idx, direction="left", duration=260)
        #fade_to(self.stack, self.stack.indexOf(self.busqueda), duration=1700)
        

    def ir_a_nuevo(self):
        #self.stack.setCurrentWidget(self.nuevo)
        self.frame_sup.hide()
        idx = self.stack.indexOf(self.nuevo)
        slide_to(self.stack, idx, direction="left", duration=260)
        #fade_to(self.stack, self.stack.indexOf(self.nuevo), duration=1700)
    
    def ir_a_editar(self):        
        #self.stack.setCurrentWidget(self.editar)
        self.frame_sup.hide()
        idx = self.stack.indexOf(self.editar)
        slide_to(self.stack, idx, direction="left", duration=260)
        #fade_to(self.stack, self.stack.indexOf(self.editar), duration=1700)
        self.editar.limpiar_campos()
        self.editar.limpiar_tabla()

    def abrir_dashboard(self):
        self.frame_sup.hide()
        idx = self.stack.indexOf(self.dashboard)
        slide_to(self.stack, idx, direction="left", duration=260)
        
        
    
    def ir_a_home(self):
        #self.stack.setCurrentWidget(self.page_home)
        idx = self.stack.indexOf(self.page_home)
        slide_to(self.stack, self.stack.indexOf(self.page_home), direction="right", duration=260)
        self.frame_sup.show()

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

        self.login.auth_ok.connect(self._on_login_nuevo_ok)
        self.login.show()

        # Sugerencia: al validar en login_nuevoUI, emite una señal y conéctala aquí para:
        # self.ir_a_nuevo()

    def _on_login_nuevo_ok(self):
        print("Login OK (recibí la señal)")                  # debug
        self.ir_a_nuevo()                                    # o slide_to(...)
        self.login.close()
        self.login = None   

    def abrir_login_editar(self):
        self.login = loginUI(self.app)
        self.login.setWindowTitle("Iniciar Sesión")
        self.login.setFixedSize(400, 600)

        base_dir = Path(__file__).resolve().parent
        icono_ventana = base_dir.parent / "assets" / "login icon.ico"
        self.login.setWindowIcon(QIcon(str(icono_ventana)))

        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.login.move(
            (screen.width() - self.login.width()) // 2,
            (screen.height() - self.login.height()) // 2
        )

        self.login.auth_ok.connect(self._on_login_editar_ok)
        self.login.show()
        
        # Igual que arriba: al validar, puedes navegar a una página de edición si la agregas al stack
    def _on_login_editar_ok(self):
        print("Login OK (recibí la señal)")                  # debug
        self.ir_a_editar()                                    # o slide_to(...)
        self.login.close()
        self.login = None  
        
    #def _on_login_nuevo_ok(self):
        # Navega dentro del stack (sin abrir ventanas nuevas)
        # Si usas animación: slide_to(self.stack, self.stack.indexOf(self.nuevo), direction="left", duration=260)
        #self.ir_a_nuevo()
        # Cierra y limpia el diálogo de login
        #self.login.close()
        #self.login = None   

    # --------- Utilidades
    def salir_app(self) -> bool:
        msg = QMessageBox(self)
        msg.setWindowTitle("Salir")
        msg.setText("¿Estás seguro que deseas salir?")
        msg.setIcon(QMessageBox.Information)
        si = msg.addButton("Sí", QMessageBox.YesRole)
        no = msg.addButton("No", QMessageBox.NoRole)
        for b in (si, no):
            b.setMinimumSize(80, 40)
            b.setStyleSheet("font-size: 14px;")
        msg.exec()
        return msg.clickedButton() is si

    def closeEvent(self, event: QCloseEvent):
        if self.salir_app():
            event.accept()
        else:
            event.ignore()
    
    def mostrar_acerca_de(self):
        QMessageBox.about(
            self,
            "Acerca de",
            "<b>SAESMA</b><br>"
            "Sistema de Administración de Emplazamientos y Solicitudes de Fabricación de la Refinería Madero<br><br>"
            "Desarrollado por Juan Javier Velázquez Escalante - Inspección Técnica""<br>"
            "Refinería Madero<br>"
            "Versión 1.0<br>"
            "© 2025 PlumeSoft"
        )
        
        


    def proximamente(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Dashboard")
        msg.setText("Dashboard, Estará disponible próximamente.")
        msg.setIcon(QMessageBox.Information)
        boton_ok = msg.addButton("OK", QMessageBox.AcceptRole)
        boton_ok.setMinimumSize(80, 40)
        

        msg.exec()


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

    screen = QGuiApplication.primaryScreen().availableGeometry()
    ventana.move(
        (screen.width() - ventana.width()) // 2,
        (screen.height() - ventana.height()) // 2
    )

    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "app_icon_2.ico"
    ventana.setWindowIcon(QIcon(str(icono_ventana)))

    sys.exit(app.exec())
