import pandas as pd
from pathlib import Path
import sqlite3 as sql



#Ruta de la base de datos

db_path = str(Path(__file__).resolve().parent.parent / "db" / "EMP.db")

#conexion a bd
conn = sql.connect(str(db_path))

df = pd.read_sql('SELECT * FROM "VISTA_EMP";', conn)

#tabla de emp por sector

matriz_emp = pd.crosstab(df["SECTOR"], df["ESTADO"])

matriz_emp = matriz_emp.reindex(columns=["VIGENTE", "VENCIDO"], fill_value=0)

# Columna de totales
matriz_emp["TOTAL_EMP"] = matriz_emp["VIGENTE"] + matriz_emp["VENCIDO"]

totales = pd.DataFrame(matriz_emp.sum()).T
totales.index = ["TOTAL_GENERAL"]

# Concatenar
matriz_emp = pd.concat([matriz_emp, totales])

print(matriz_emp.reset_index())

matriz_plot[["VIGENTE", "VENCIDO", "TOTAL_SF"]].plot(
    kind="bar", figsize=(10,6)
)

plt.title("Totales, Vigentes y Vencidos por SECTOR")
plt.xlabel("Sector")
plt.ylabel("Cantidad de EMP")
plt.legend(title="Categoría")
plt.tight_layout()
plt.show()

conn.close()




