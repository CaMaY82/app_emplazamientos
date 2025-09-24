from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QRadioButton, QComboBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QGridLayout, QHeaderView, QLineEdit, QSpacerItem, QToolButton, QTextEdit, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
import darkdetect
import sys
from pathlib import Path
from functools import partial
from conexiondb import globalconn



class Dashboard(QWidget):
    volver_home = Signal()

    def __init__(self, app):
        super().__init__()

        base_dir = Path(__file__).resolve().parent

        # ----- layout raíz -----
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ----- botón regresar (arriba-izquierda, fijo) -----
        icono_regresar = base_dir.parent / "assets" / "regresar_icon.png"

        self.regresar = QToolButton(self)
        self.regresar.setObjectName("btnRegresar")
        self.regresar.setIcon(QIcon(str(icono_regresar)))
        self.regresar.setIconSize(QSize(50, 50))
        self.regresar.setToolButtonStyle(Qt.ToolButtonIconOnly)  # <-- icono puro
        self.regresar.setAutoRaise(True)
        self.regresar.setFocusPolicy(Qt.NoFocus)
        self.regresar.setCursor(Qt.PointingHandCursor)

        # Un SOLO stylesheet (no lo sobrescribas después)
        self.regresar.setStyleSheet("""
        #btnRegresar {
            background: transparent;
            border: none;
            padding: 0;
            margin: 6px;          /* aire externo */
        }
        #btnRegresar:hover { background: transparent; }
        #btnRegresar:pressed { background: transparent; }
        #btnRegresar::menu-indicator { image: none; width:0; height:0; }
        """)

        self.regresar.clicked.connect(self.volver_home.emit)
        root.addWidget(self.regresar, alignment=Qt.AlignLeft)

        # ----- scroll + contenedor de gráficas -----
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.vbox = QVBoxLayout(container)
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        scroll.setWidget(container)

        root.addWidget(scroll)

        # fondos negros en todos los niveles
        container.setStyleSheet("background: black;")
        scroll.setStyleSheet("background: black;")
        scroll.viewport().setStyleSheet("background: black;")  # <- clave
        self.setStyleSheet("background: black;")

        # stretch al final para que todo quede pegado arriba
        self.vbox.addStretch(1)

        self.cargar_graficos()

    # Añadir figura de Plotly sin márgenes blancos
    def add_plotly(self, fig, min_h=600, offline=False, fill_height=True):
        
        if fill_height:
            fig.update_layout(height=min_h, autosize=True,
                          margin=dict(l=40, r=20, t=60, b=40))  # márgenes razonables
        
        frag = fig.to_html(
            full_html=False,
            include_plotlyjs=True if offline else "cdn",
            config={"responsive": True, "displaylogo": False}
        )

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background: black;   /* o 'transparent' si prefieres */
  }}
</style>
</head>
<body>
{frag}
</body>
</html>"""

        view = QWebEngineView()
        view.setAttribute(Qt.WA_StyledBackground, True)
        view.setStyleSheet("background: black; border: 0;")
        try:
            view.page().setBackgroundColor(QColor("black"))
        except Exception:
            pass

        view.setHtml(html)
        view.setMinimumHeight(min_h)
        view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Insertar antes del stretch final
        self.vbox.insertWidget(self.vbox.count() - 1, view)

    def cargar_graficos(self):
        from graficos_plotly import fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10
        for fig in [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10]:
            self.add_plotly(fig, min_h=1000)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtGui import QIcon
    import sys

    app = QApplication(sys.argv)
    ventana = QMainWindow()
    ventana.setWindowTitle("Dashboard")
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "dashboard2.ico"
    
    # Pasa `app` 
    ui =Dashboard(app)
    ventana.setCentralWidget(ui)
    ventana.setWindowIcon(QIcon(str(icono_ventana)))
    ventana.show()
    
    sys.exit(app.exec())