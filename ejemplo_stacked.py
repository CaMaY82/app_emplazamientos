from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QStackedWidget, QLabel, QHBoxLayout
)
import sys

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo QStackedWidget")

        # Creamos las diferentes "pantallas"
        self.pantalla_inicio = QWidget()
        self.pantalla_config = QWidget()
        
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.pantalla_inicio)  # índice 0
        self.stack.addWidget(self.pantalla_config)  # índice 1

        # Contenido de pantalla_inicio
        layout_inicio = QVBoxLayout()
        layout_inicio.addWidget(QLabel("Bienvenido a la pantalla de inicio"))
        btn_abrir_config = QPushButton("Ir a Configuración")
        btn_abrir_config.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout_inicio.addWidget(btn_abrir_config)
        self.pantalla_inicio.setLayout(layout_inicio)

        # Contenido de pantalla_config
        layout_config = QVBoxLayout()
        layout_config.addWidget(QLabel("Configuraciones"))
        btn_volver = QPushButton("Volver al inicio")
        btn_volver.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout_config.addWidget(btn_volver)
        self.pantalla_config.setLayout(layout_config)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.stack)
        self.setLayout(layout_principal)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
