# main.py
from PySide6.QtWidgets import QApplication, QMessageBox
from menu_principal import MenuPrincipal
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MenuPrincipal(app)
    ventana.show()
    sys.exit(app.exec())

