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

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.vbox = QVBoxLayout(container)
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(container)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)
        self.vbox.addStretch(1)
        self.cargar_graficos()
        
    # Añadiendo plotly
    def add_plotly(self, fig, min_h=420, offline=False):
        html = fig.to_html(
            full_html=False,
            include_plotlyjs=True if offline else "cdn",
            config={"responsive": True, "displaylogo": False}
        )
        view = QWebEngineView()
        view.setHtml(html)
        view.setMinimumHeight(min_h)
        view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # Insertar antes del stretch final
        self.vbox.insertWidget(self.vbox.count() - 1, view)
    
    def cargar_graficos(self):
        from graficos_plotly import fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9

        figuras = [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9]

          # Detectar modo oscuro
        dark_mode = darkdetect.isDark()

        for fig in figuras:
            if dark_mode:
                fig.update_layout(
                     template="plotly_dark",
                     paper_bgcolor="black",
                     plot_bgcolor="black",
                     font=dict(color="white", size=14),  # tamaño y color global
                    legend=dict(
                        font=dict(color="white"),       # leyendas
                        bgcolor="rgba(0,0,0,0)"         # fondo transparente
                    )
            )
            else:
                 fig.update_layout(
                    template="plotly_white",
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    font=dict(color="black", size=14),
                    legend=dict(
                        font=dict(color="black"),
                        bgcolor="rgba(0,0,0,0)"
                    )
                )
        self.add_plotly(fig, min_h=1000)

        for fig in figuras:
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