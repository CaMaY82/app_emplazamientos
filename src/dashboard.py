import pandas as pd
from pathlib import Path
import sqlite3 as sql
import matplotlib.pyplot as plt


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
#print(matriz_emp.reset_index())

df_plot = matriz_emp.loc[matriz_emp.index != "TOTAL_GENERAL", ["VIGENTE", "VENCIDO"]]
fig, ax = plt.subplots(figsize=(10, 6))
df_plot.plot(kind="bar", ax=ax)

ax.set_title("EMPLAZAMIENTOS")
ax.set_xlabel("Sector")
ax.set_ylabel("")
ax.legend(title="Categoría")

# Etiquetas de datos por barra
for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", label_type="edge", padding=3)

plt.tight_layout()
plt.xticks(rotation=360, ha="right")  # alineadas a la derecha
plt.tight_layout()                   # ajusta el espacio automáticamente
#plt.xticks(rotation=360)
#plt.show()

#creando tabla para tipo de riesgo
matriz_riesgo = pd.crosstab(df["SECTOR"], ["RIESGO"]).reindex(columns=list("ABCD"), fill_value=0)

global_counts = df["RIESGO"].value_counts().reindex(list("ABCD"), fill_value=0)

values = global_counts.values

def autopct_with_count(pct):
    total = values.sum()
    count = int(round(pct * total / 100.0))
    return f"{count} ({pct:.1f}%)" if count > 0 else ""  # oculta etiquetas en 0

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(
    values,
    labels=[f"Riesgo {k}" for k in global_counts.index],
    startangle=90,
    autopct=autopct_with_count,  # ← cantidad y %
    labeldistance=1.05, pctdistance=0.7  # opcional si se enciman
)


ax.set_title("Tipo de Riesgo en Emplazamintos")
ax.axis("equal")
plt.tight_layout()
plt.show()




