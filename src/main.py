import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from menu_principal import MenuPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MenuPrincipal(app)
    ventana.show()
    sys.exit(app.exec())