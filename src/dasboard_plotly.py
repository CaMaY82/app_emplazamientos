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
fig.update_layout(
    title={
        'text': "Emplazamientos por Sector",
        'x': 0.5,   # 0=izquierda, 0.5=centro, 1=derecha
        'xanchor': 'center',
        'yanchor': 'top'
    }
)
fig.update_traces(textfont_size = 20, textangle = 0, textposition = "outside")
fig.show()

#Grafico de pastel


#primero se filtran los vigentes y vencidos
df_filtrado = df[df["ESTADO"].isin(["VIGENTE", "VENCIDO"])]
#Filtro operando y fuera de operación
totales = df_filtrado["STATUS OPERATIVO"].value_counts().reset_index()
totales.columns = ["STATUS OPERATIVO", "TOTAL"]
print(totales)


fig2 = px.pie(
    totales, 
    names="STATUS OPERATIVO",
    values="TOTAL",
    title="Emplazamientos Operando y Fuera de Operación",  
    color = "STATUS OPERATIVO",
    color_discrete_map={"OPERANDO": "#44a5c2", "FUERA DE OPERACION": "#024b7a"},
)
fig2.update_layout(
    title={
        'text': "Emplazamientos Operando y Fuera de Operación",
        'x': 0.5,   # 0=izquierda, 0.5=centro, 1=derecha
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
        family="Arial black",
        size=24,
        color  = "black",
        )
    }
)
fig2.update_traces(
    pull =[0.1, 0],
    textposition='inside',
    textinfo='percent+label',
    textfont_size = 20
    )
fig2.show()

#Grafico por clase de riesgo
riesgo = df_filtrado["RIESGO"].value_counts().reset_index()
riesgo.columns = ["RIESGO", "TOTAL"]
print(riesgo)

fig3 = px.pie(
    riesgo, 
    names="RIESGO",
    values="TOTAL",
    title="Clase de riesgo en emplazamientos",  
    color = "RIESGO",
    color_discrete_map={"A": "#c24444", "B": "#f19935", "C": "#f2e205", "D": "#44c28c"},
    hole = 0.7
)
fig3.update_layout(
    title={
        'text': "Clase de riesgo en emplazamientos",
        'x': 0.5,   # 0=izquierda, 0.5=centro, 1=derecha
        'xanchor': 'center',
        'yanchor': 'top'
    }
)
fig3.update_traces(
    pull=[0.1, 0.01, 0.02, 0.03],
    textposition='outside', 
    textinfo='label+value+percent', 
    textfont_size = 20,
    marker=dict(line=dict(color="white", width=2))
)
fig3.show()

#grafico de barras horizontales


