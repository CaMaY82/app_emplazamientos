import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from menu_principal import MenuPrincipal
from login_menu import login_menu
import sys, os

def app_root() -> Path:
    if hasattr(sys, "_MEIPASS"):                 # exe --onefile (carpeta temporal)
        return Path(sys._MEIPASS)
    if getattr(sys, "frozen", False):            # exe --onedir
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent # desarrollo (tu raíz)

ROOT = app_root()
os.chdir(ROOT)

# DEBUG: quitar luego
try:
    from datetime import datetime
    log = ROOT / "assets_check.txt"
    items = "\n".join(str(p) for p in (ROOT/"assets").glob("*"))
    log.write_text(
        f"[{datetime.now()}]\nROOT={ROOT}\nCWD={Path.cwd()}\n"
        f"assets existe: {(ROOT/'assets').exists()}\n"
        f"Ejemplos en assets:\n{items}\n",
        encoding="utf-8"
    )
except Exception as e:
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(ROOT / "assets" / "app_icon.ico")))

    # --- Splash opcional ---
    splash = None
    splash_img = ROOT / "assets" / "splash.png"
    if splash_img.exists():
        splash = QSplashScreen(QPixmap(str(splash_img)))
        splash.setWindowFlag(Qt.FramelessWindowHint)
        splash.show()
        app.processEvents()

    # --- Login primero ---
    login = login_menu(app)   # <-- instancia
    login.setWindowTitle("SAESMA MADERO")

    if splash:
            splash.finish(login)

    

    def abrir_menu():
        # guarda la referencia en `app` para que no se libere
        app.menu = MenuPrincipal(app)
        app.menu.show()

       
    # señal que emite LoginMenu cuando valida
    login.auth_ok.connect(abrir_menu)

    login.show()
    sys.exit(app.exec())