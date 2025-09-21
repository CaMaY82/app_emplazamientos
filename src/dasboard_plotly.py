import pandas as pd
import plotly.express as px
from conexiondb import globalconn

#conexion a bd
conexion = globalconn

#Creando DataFrame
df = pd.read_sql('SELECT * FROM "VISTA_EMP";', conexion)
matriz_emp = pd.crosstab(df["SECTOR"], df["ESTADO"])
matriz_emp = matriz_emp.reindex(columns=["VIGENTE", "VENCIDO"], fill_value=0)

#Grafico de barras EMP VIGENTES Y VENCIDOS por sector
fig1 = px.bar(
    matriz_emp,
    x=matriz_emp.index,
    y=["VIGENTE", "VENCIDO"],
    title="Emplazamientos por Sector",
    labels={"value": "Cantidad", "SECTOR": "Sector"},
    color_discrete_sequence=["#024b7a", "#44a5c2"],
    barmode="stack",
    text_auto=True 
)
fig1.update_layout(
    title={
        'text': "Emplazamientos por Sector",
        'x': 0.5,   # 0=izquierda, 0.5=centro, 1=derecha
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
        family="Arial black",
        size=24,
        color  = "black",
        )
    },
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
fig1.update_traces(textfont_size = 15, textangle = 0, textposition = "inside")


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
    },
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

)
fig2.update_traces(
    pull =[0.1, 0],
    textposition='inside',
    textinfo='percent+label',
    textfont_size = 20
    )


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
        'yanchor': 'top',
        'font': dict(
        family="Arial black",
        size=24,
        color  = "black",
        )
    },
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
fig3.update_traces(
    pull=[0.1, 0.01, 0.02, 0.03],
    textposition='outside', 
    textinfo='label+value+percent', 
    textfont_size = 20,
    marker=dict(line=dict(color="white", width=2))
)


#grafico de barras horizontales
#Creación de los dataframes
mecanismos_emp = df_filtrado["MECANISMO DE DAÑO"].value_counts().reset_index()
mecanismos_emp.columns = ["MECANISMO DE DAÑO", "TOTAL"]
mecanismos_emp_ordenado = mecanismos_emp.sort_values(by="TOTAL", ascending=True)

fig4 = px.bar(
    mecanismos_emp_ordenado,
    x = "TOTAL",
    y = "MECANISMO DE DAÑO",
    title = "Mecanismo de daño",
    labels = {"TOTAL": "Cantidad", "MECANISMO DE DAÑO": "Mecanismo de daño"},
    color_discrete_sequence = ["#44a5c2"],
    orientation = "h",
    text_auto = True
)
fig4.update_layout(
    title={'text':"<b>Mecanismo de daño por emplazamiento</b>", 'x':0.5},
    xaxis_title="Cantidad",
    yaxis_title="Mecanismo de daño",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="black", size=18)
)
fig4.update_traces(
    textposition="outside",               # valores afuera de la barra
    texttemplate="%{value}",              # solo el número
    outsidetextfont=dict(
        family="Arial Black",             # fuente negrita
        size=15,
        color="black"
    ),
    cliponaxis=False                      # evita que se corten al pegarse al eje
)

#Solicitudes de fabricación
#dataframe
df_sf  = pd.read_sql('SELECT * FROM "VISTA_SF";', conexion)
matriz_sf = pd.crosstab(df_sf["SECTOR"], df_sf["ESTADO"])
matriz_sf = matriz_sf.reindex(columns=["VIGENTE", "VENCIDO"], fill_value=0)
#grafico de barras
fig5 = px.bar(
    matriz_sf,
    x=matriz_sf.index,
    y=["VIGENTE", "VENCIDO"],
    title="Solicitudes de fabricación por Sector",
    labels={"value": "Cantidad", "SECTOR": "Sector"},
    color_discrete_sequence=["#58C7BE", "#6FD3F4"],
    barmode="stack",
    text_auto=True 
)
fig5.update_layout(
    title={
        'text': "Solicitudes de Fabricación por Sector",
        'x': 0.5,   # 0=izquierda, 0.5=centro, 1=derecha
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
        family="Arial black",
        size=24,
        color  = "black",
        )
    },
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    
)
fig5.update_xaxes(
    title_text="Sector",
    title_font=dict(size=20, family="Arial Black", color="black"),
    tickfont=dict(size=20, family="Arial", color="black")
)
fig5.update_yaxes(
    title_text="Cantidad",
    title_font=dict(size=20, family="Arial Black", color="black"),
    tickfont=dict(size=20, family="Arial", color="black")
)
fig5.update_traces(
    textfont=dict(
        size=15,
        family="Arial Black",
        color="black"
    ),
    textfont_size = 15,
    textangle = 0, 
    textposition = "inside"
)

fig1.show() #Gráfico de emplazamientos por sector vigentes y vencidos
fig2.show() #Gráfico de pastel de emplazamientos operando y fuera de operación
fig3.show() #Gráfico de Riesgos en Emplazamientos
fig4.show() #Gráfico de Mecanismo de daños en emplazamientos
fig5.show() #Gráfico de SF por sector vigentes y vencidos




