import pandas as pd
import plotly.express as px
from conexiondb import globalconn


#conexion a bd
conexion = globalconn

#Creando DataFrame
df = pd.read_sql('SELECT * FROM "VISTA_EMP";', conexion)
matriz_emp = pd.crosstab(df["SECTOR"], df["ESTADO"])
matriz_emp = matriz_emp.reindex(columns=["VIGENTE", "VENCIDO"], fill_value=0)

#suma de vencidos y vigentes
suma_emp = matriz_emp["VIGENTE"] + matriz_emp["VENCIDO"]

#Grafico de barras EMP VIGENTES Y VENCIDOS por sector
fig1 = px.bar(
    matriz_emp,
    x=matriz_emp.index,
    y=["VIGENTE", "VENCIDO"],
    title="Emplazamientos por Sector",
    labels={"value": "Cantidad", "SECTOR": "Sector"},
    color_discrete_sequence=["#118DFF", "#12239E"],
    barmode="stack",
    text_auto=True 
)

fig1.update_layout(
    title={
        'text': "Emplazamientos por Sector",
        'x': 0.5,  # 0=izquierda, 0.5=centro, 1=derecha
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            family="Arial Black",
            size=24,
            color="black"
        )
    },
    legend=dict(
        title="Estado",  # Cambiar el título de "variable" a "Estado"
        font=dict(
            size=20,       # Tamaño de fuente de la leyenda
            color="black"  # Color de texto de la leyenda
        )
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

fig1.update_traces(
    textfont_size = 20, 
    textangle = 0, 
    textposition = "inside",
    hoverlabel=dict(
        bgcolor="white",   # Fondo blanco
        font_size=14,      # Tamaño de fuente
        font_color="black"),
    hovertemplate="Sector %{x}<br>%{y} %{fullData.name}<extra></extra>", # Color del texto
    )


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
    color_discrete_map={"OPERANDO": "#118DFF", "FUERA DE OPERACION": "#12239E"}, 
)
fig2.update_layout(
    title=dict(
        text="Emplazamientos Operando y Fuera de Operación",
        x=0.5,           # 0=izq, 0.5=centro, 1=der
        xanchor="center",
        yanchor="top",
        font=dict(
            family="Arial Black",
            size=24,
            color="black"
        )
    ),
    legend=dict(
        title=dict(text="Estado"),  # título de la leyenda
        font=dict(size=15, color="black")
    ), 
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
) 

fig2.update_traces(
    pull =[0.1, 0],
    textposition='inside',
    textinfo='percent+label',
    textfont_size = 20,
    hoverlabel=dict(
        bgcolor="white",   # Fondo blanco
        font_size=14,      # Tamaño de fuente
        font_color="black"
        ),
    hovertemplate="%{value} %{label}<extra></extra>"
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
    color_discrete_sequence = ["#118DFF"],
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
    color_discrete_sequence=["#58C7BE", "#52A59E"],
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
            family="Arial Black",
            size=24,
            color="black"
        )
    },
    legend=dict(
        title="Estado",  # Cambiar el título de "variable" a "Estado"
        font=dict(
            size=20,       # Tamaño de fuente de la leyenda
            color="black"  # Color de texto de la leyenda
        )
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
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
    textfont_size = 20, 
    textangle = 0, 
    textposition = "inside",
    hoverlabel=dict(
        bgcolor="white",   # Fondo blanco
        font_size=14,      # Tamaño de fuente
        font_color="black"),
    hovertemplate="Sector %{x}<br>%{y} %{fullData.name}<extra></extra>", # Color del texto
    )

#grafico de pastel de SF operando y Fuera de operación.
sf_op = df_sf[df_sf["ESTADO"].isin(["VIGENTE", "VENCIDO"])]
#Filtro operando y fuera de operación
sf_totales = sf_op["STATUS OPERATIVO"].value_counts().reset_index()
sf_totales.columns = ["STATUS OPERATIVO", "TOTAL"]

#grafico
fig6 = px.pie(
    sf_totales, 
    names="STATUS OPERATIVO",
    values="TOTAL",
    title="ESolicitudes de fabricación Operando y Fuera de Operación",  
    color = "STATUS OPERATIVO",
    color_discrete_map={"OPERANDO": "#58C7BE", "FUERA DE OPERACION": "#52A59E"},
)
fig6.update_layout(
    title=dict(
        text="Emplazamientos Operando y Fuera de Operación",
        x=0.5,           # 0=izq, 0.5=centro, 1=der
        xanchor="center",
        yanchor="top",
        font=dict(
            family="Arial Black",
            size=24,
            color="black"
        )
    ),
    legend=dict(
        title=dict(text="Estado"),  # título de la leyenda
        font=dict(size=15, color="black")
    ), 
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
) 

fig6.update_traces(
    pull =[0.1, 0],
    textposition='inside',
    textinfo='percent+label',
    textfont_size = 20,
    hoverlabel=dict(
        bgcolor="white",   # Fondo blanco
        font_size=14,      # Tamaño de fuente
        font_color="black"
        ),
    hovertemplate="%{value} %{label}<extra></extra>"
    )

#Grafico de riesgo en SF
sf_riesgo = sf_op["RIESGO"].value_counts().reset_index()
sf_riesgo.columns = ["RIESGO", "TOTAL"]

fig7 = px.pie(
        sf_riesgo, 
        names="RIESGO",
        values="TOTAL",
        title="Clase de riesgo en Solicitudes de Fabricación",  
        color = "RIESGO",
        color_discrete_map={"A": "#c24444", "B": "#f19935", "C": "#f2e205", "D": "#44c28c"},
        hole = 0.7
    )
fig7.update_layout(
        title={
            'text': "Clase de riesgo en Solicitudes de Fabricación",
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
fig7.update_traces(
        pull=[0.1, 0.01, 0.02, 0.03],
        textposition='outside', 
        textinfo='label+value+percent', 
        textfont_size = 20,
        marker=dict(line=dict(color="white", width=2))
    )
#Sunbrust SF
sf_sb = sf_op.copy()
sf_sb["RIESGO"] = sf_sb["RIESGO"].fillna("Sin dato").astype(str).str.upper()
sf_sb["ESTADO"] = sf_sb["ESTADO"].str.upper()
sf_sb["STATUS OPERATIVO"] = sf_sb["STATUS OPERATIVO"].str.upper()

df_agg = (
    sf_sb.groupby(["RIESGO", "ESTADO", "STATUS OPERATIVO"])
         .size().reset_index(name="TOTAL")
)

df_agg["RIESGO"] = pd.Categorical(df_agg["RIESGO"], ["A","B","C","D",], ordered=True)
df_agg["ESTADO"] = pd.Categorical(df_agg["ESTADO"], ["VIGENTE","VENCIDO"], ordered=True)
df_agg["STATUS OPERATIVO"] = pd.Categorical(df_agg["STATUS OPERATIVO"],
                                            ["OPERANDO","FUERA DE OPERACIÓN"], ordered=True)

fig8 = px.sunburst(
    df_agg,
    path=["RIESGO", "ESTADO", "STATUS OPERATIVO"],
    values="TOTAL",
    color="RIESGO",
    color_discrete_map={"A": "#c24444", "B": "#f19935", "C": "#f2e205", "D": "#44c28c"},
    branchvalues="total"
)

fig8.update_traces(
    textinfo="label+value+percent root",
    #hovertemplate="%{currentPath}<br>Total: %{value}<br>%{percentRoot} del total<extra></extra>",
    hovertemplate="%{value} %{parent} %{label} = %{percentRoot:.0%} del Total<extra></extra>",
    marker=dict(line=dict(color="white", width=1)),
    hoverlabel=dict(bgcolor="white", font=dict(size=16, color="black"))
)

fig8.update_layout(
    title_text="Solicitudes de Fabricación: Riesgo - Estado & Status Operativo",
    title_x=0.5,
    title_font=dict(family="Arial Black", size=24, color="black"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

#Mecanismos de daño en SF
#

sf_mecanismos = sf_op["MECANISMO DE DAÑO"].value_counts().reset_index()
sf_mecanismos.columns = ["MECANISMO DE DAÑO", "TOTAL"]
sf_mecanismos_ordenado = sf_mecanismos.sort_values(by="TOTAL", ascending=True)

fig9 = px.bar(
    sf_mecanismos_ordenado,
    x = "TOTAL",
    y = "MECANISMO DE DAÑO",
    title = "Mecanismo de daño",
    labels = {"TOTAL": "Cantidad", "MECANISMO DE DAÑO": "Mecanismo de daño"},
    color_discrete_sequence = ["#52A59E"],
    orientation = "h",
    text_auto = True
)
fig9.update_layout(
    title={'text':"<b>Mecanismo de daño por emplazamiento</b>", 'x':0.5},
    xaxis_title="Cantidad",
    yaxis_title="Mecanismo de daño",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="black", size=18)
)
fig9.update_traces(
    textposition="outside",               # valores afuera de la barra
    texttemplate="%{value}",              # solo el número
    outsidetextfont=dict(
        family="Arial Black",             # fuente negrita
        size=15,
        color="black"
    ),
    cliponaxis=False                      # evita que se corten al pegarse al eje
)


#fig1.show() #Gráfico de emplazamientos por sector vigentes y vencidos
#fig2.show() #Gráfico de pastel de emplazamientos operando y fuera de operación
#fig3.show() #Gráfico de Riesgos en Emplazamientos
#fig4.show() #Gráfico de Mecanismo de daños en emplazamientos
#fig5.show() #Gráfico de SF por sector vigentes y vencidos
#fig6.show() #Gráfico de pastel de SF operando y fuera de operación
#fig7.show() #Gráfico de Riesgos en SF
#fig8.show() #Gráfico Sunbrust de SF
#fig9.show() #Gráfico de Mecanismo de daños en SF



