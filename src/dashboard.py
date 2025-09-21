import pandas as pd
import matplotlib.pyplot as plt
from conexiondb import globalconn


#conexion a bd

conexion = globalconn
df = pd.read_sql('SELECT * FROM "VISTA_EMP";', conexion)



#tabla de emp por sector
matriz_emp = pd.crosstab(df["SECTOR"], df["ESTADO"])
matriz_emp = matriz_emp.reindex(columns=["VIGENTE", "VENCIDO"], fill_value=0)

#matriz de riesgo por emplazamiento 

#filtrar vigente y vencido

df_filtrado = df[df["ESTADO"].isin(["VIGENTE", "VENCIDO"])]

#Normalizar valores de riezgo (aparece 2 columnas de "c")
df_filtrado["RIESGO"] = df_filtrado["RIESGO"].str.strip().str.upper()

#crear la tabla
matriz_emp_riesgo = pd.crosstab(
    [df_filtrado["SECTOR"], df_filtrado["ESTADO"]],
    df_filtrado["RIESGO"]
).reindex(columns=["A","B","C","D"], fill_value=0)

#print(matriz_emp_riesgo)

#print(matriz_emp)

# Columna de totales
matriz_emp["TOTAL_EMP"] = matriz_emp["VIGENTE"] + matriz_emp["VENCIDO"]
totales = pd.DataFrame(matriz_emp.sum()).T
totales.index = ["TOTAL_GENERAL"]

# Concatenar
matriz_emp_totales = pd.concat([matriz_emp, totales])
#print(matriz_emp_totales)

#grafico:

fig, ax = plt.subplots(figsize=(8, 5))

# Solo graficamos VIGENTE y VENCIDO
matriz_emp[["VIGENTE", "VENCIDO"]].plot(
    kind="bar",
    stacked=True,
    color=["#024b7a", "#44a5c2"],
    alpha=0.85,
    ax=ax
)

ax.set_title("Emplazamientos por Sector")
ax.set_xlabel("Sector")
ax.set_ylabel("Cantidad")
ax.legend(title="Estado")

# Etiquetas dentro de cada segmento
for cont in ax.containers:
    ax.bar_label(cont, label_type="center", fontsize=12, color="white", fontweight="bold")

totales = matriz_emp[["VIGENTE", "VENCIDO"]].sum(axis=1).values
xs = range(len(matriz_emp))


for idx, total in enumerate(totales):
    ax.text(idx, total, str(int(total)),
            ha="center", va="bottom", fontsize=12, color="black")

plt.xticks(rotation=360)
yticks = ax.get_yticks()
ax.set_yticks([t for t in yticks if t != 0])
fig.patch.set_alpha(0)          # figura transparente
ax.set_facecolor('none')
plt.tight_layout()
#plt.show()

#grafico de pastel con riesgo

colores = ["#B9DDF1", "#9FCAE6", "#73A4CA", "#497AA7"]
df["ESTADO"] = df["ESTADO"].str.strip().str.upper()
df["RIESGO"] = df["RIESGO"].str.strip().str.upper()
df_filtrado = df[df["ESTADO"].isin(["VIGENTE", "VENCIDO"])]
riesgo_counts = df_filtrado["RIESGO"].value_counts().reindex(list("ABCD"), fill_value=0)
fig, ax = plt.subplots(figsize=(6, 6))
explode = [0.5] * len(riesgo_counts)
ax.pie(
    riesgo_counts.values,
    labels=riesgo_counts.index,
    autopct=lambda p: f"{p:.1f}%\n({int(p*riesgo_counts.sum()/100)})",
    colors=(colores),
    startangle=90,
    labeldistance=1.1,   # empuja etiquetas hacia afuera
    pctdistance=0.8,
)
ax.set_title("Riesgos en Emplazamientos")
ax.axis("equal")  # círculo perfecto

plt.tight_layout()
plt.show()


df_op = df[df["STATUS OPERATIVO"].isin(["OPERANDO", "FUERA DE OPERACIÓN"])]

df_op_no_atn = df_op["ESTADO"].isin(["VIGENTE", "VENCIDO"])








