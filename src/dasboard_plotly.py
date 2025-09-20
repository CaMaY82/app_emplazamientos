import pandas as pd
import plotly.express as px
from conexiondb import globalconn

#conexion a bd
conexion = globalconn

#Creando DataFrame
df = pd.read_sql('SELECT * FROM "VISTA_EMP";', conexion)
matriz_emp = pd.crosstab(df["SECTOR"], df["ESTADO"])
matriz_emp = matriz_emp.reindex(columns=["VIGENTE", "VENCIDO"], fill_value=0)
#print (matriz_emp)

#Grafico de barras EMP VIGENTES Y VENCIDOS por sector
fig = px.bar(
    matriz_emp,
    x=matriz_emp.index,
    y=["VIGENTE", "VENCIDO"],
    title="Emplazamientos por Sector",
    labels={"value": "Cantidad", "SECTOR": "Sector"},
    color_discrete_sequence=["#024b7a", "#44a5c2"],
    barmode="stack",
    text_auto=True 
)
fig.update_traces(textfont_size = 20, textangle = 0, textposition = "outside")
fig.show()

#Grafico de pastel


#primero se filtran los vigentes y vencidos
df_filtrado = df[df["ESTADO"].isin(["VIGENTE", "VENCIDO"])]
#Filtro operando y fuera de operación
emp_op = df[df["STATUS OPERATIVO"].isin(["OPERANDO", "FUERA DE OPERACION"])]
matriz_emp_op = pd.crosstab(emp_op["SECTOR"], emp_op["STATUS OPERATIVO"])
matriz_emp_op = matriz_emp_op.reindex(columns=["OPERANDO", "FUERA DE OPERACION"], fill_value=0)
totales = matriz_emp_op.sum().to_frame().reset_index()
totales.columns = ["STATUS OPERATIVO", "TOTAL"]
print(matriz_emp_op)

fig2 = px.pie(
    totales, 
    names="STATUS OPERATIVO",
    values="TOTAL",
    title="Emplazamientos Operando y Fuera de Operación",  
    color = "STATUS OPERATIVO",
    color_discrete_map={"OPERANDO": "#44a5c2", "FUERA DE OPERACION": "#024b7a"},
)
fig2.update_traces(textposition='inside', textinfo='percent+label')
fig2.show()

print(df["STATUS OPERATIVO"].value_counts())


