import pandas as pd
import plotly.express as px
import plotly.io as pio
import darkdetect
from conexiondb import globalconn


#conexion a bd
conexion = globalconn

# -*- coding: utf-8 -*-
import pandas as pd
import plotly.express as px
import plotly.io as pio
import darkdetect

# ------------ Tema automático (dark / light) ------------
DARK = bool(darkdetect.isDark())

# Paleta y estilos dependientes del tema
text_color = "white" if DARK else "black"
paper_bg   = "#1E1E1E" if DARK else "white"
plot_bg    = "#1E1E1E" if DARK else "white"
grid_color = "rgba(255,255,255,0.08)" if DARK else "rgba(0,0,0,0.08)"
hover_bg   = "black" if DARK else "white"
hover_fg   = "white" if DARK else "black"

# (opcional) template global para figuras nuevas
pio.templates.default = "plotly_dark" if DARK else "plotly_white"

# Helper para aplicar layout base coherente
def aplicar_tema(fig):
    fig.update_layout(
        paper_bgcolor=paper_bg,           # si incrustas en PySide con fondo oscuro/claro
        plot_bgcolor=plot_bg,
        font=dict(color=text_color, size=14),
        title_font_color=text_color,
        legend=dict(
            title_font=dict(color=text_color),
            font=dict(color=text_color),
            bgcolor="rgba(0,0,0,0)"       # transparente
        ),
        xaxis=dict(
            title_font=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=grid_color
        ),
        yaxis=dict(
            title_font=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=grid_color
        ),
    )
    # hoverlabel coherente
    fig.update_traces(hoverlabel=dict(bgcolor=hover_bg, font=dict(color=hover_fg)))
    return fig
# --------------------------------------------------------

# ====== DATOS EMP ======
df = pd.read_sql('SELECT * FROM "VISTA_EMP";', conexion)
matriz_emp = pd.crosstab(df["SECTOR"], df["ESTADO"]).reindex(
    columns=["VIGENTE", "VENCIDO"], fill_value=0
)
suma_emp = matriz_emp["VIGENTE"] + matriz_emp["VENCIDO"]

# --- fig1: Barras EMP VIGENTE/VENCIDO por sector
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
    title=dict(
        text="Emplazamientos por Sector",
        x=0.5, xanchor="center", yanchor="top",
        font=dict(family="Arial Black", size=24)   # ← sin color fijo
    ),
)
fig1.update_traces(
    textfont_size=20,
    textangle=0,
    textposition="inside",
    hovertemplate="Sector %{x}<br>%{y} %{fullData.name}<extra></extra>",
)
aplicar_tema(fig1)

# --- fig2: Pie Operando / Fuera de operación (EMP)
df_filtrado = df[df["ESTADO"].isin(["VIGENTE", "VENCIDO"])]
totales = df_filtrado["STATUS OPERATIVO"].value_counts().reset_index()
totales.columns = ["STATUS OPERATIVO", "TOTAL"]

fig2 = px.pie(
    totales,
    names="STATUS OPERATIVO",
    values="TOTAL",
    title="Emplazamientos Operando y Fuera de Operación",
    color="STATUS OPERATIVO",
    color_discrete_map={"OPERANDO": "#118DFF", "FUERA DE OPERACION": "#12239E"},
)
fig2.update_layout(
    title=dict(
        text="Emplazamientos Operando y Fuera de Operación",
        x=0.5, xanchor="center", yanchor="top",
        font=dict(family="Arial Black", size=24)
    ),
)
fig2.update_traces(
    pull=[0.1, 0],
    textposition="inside",
    textinfo="percent+label",
    textfont_size=20,
    hovertemplate="%{value} %{label}<extra></extra>"
)
aplicar_tema(fig2)

# --- fig3: Donut por RIESGO (EMP)
riesgo = df_filtrado["RIESGO"].value_counts().reset_index()
riesgo.columns = ["RIESGO", "TOTAL"]

fig3 = px.pie(
    riesgo,
    names="RIESGO",
    values="TOTAL",
    title="Clase de riesgo en emplazamientos",
    color="RIESGO",
    color_discrete_map={"A": "#c24444", "B": "#f19935", "C": "#f2e205", "D": "#44c28c"},
    hole=0.7
)
fig3.update_layout(
    title=dict(
        text="Clase de riesgo en emplazamientos",
        x=0.5, xanchor="center", yanchor="top",
        font=dict(family="Arial Black", size=24)
    ),
)
fig3.update_traces(
    pull=[0.1, 0.01, 0.02, 0.03],
    textposition="outside",
    textinfo="label+value+percent",
    textfont_size=20,
    marker=dict(line=dict(color="white", width=2))
)
aplicar_tema(fig3)

# --- fig4: Sunburst Riesgo → Estado → Status Operativo (EMP)
emp_sb = df_filtrado.copy()
emp_sb["RIESGO"] = emp_sb["RIESGO"].fillna("Sin dato").astype(str).str.upper()
emp_sb["ESTADO"] = emp_sb["ESTADO"].str.upper()
emp_sb["STATUS OPERATIVO"] = emp_sb["STATUS OPERATIVO"].str.upper()

df_empagg = (
    emp_sb.groupby(["RIESGO", "ESTADO", "STATUS OPERATIVO"])
         .size().reset_index(name="TOTAL")
)
df_empagg["RIESGO"] = pd.Categorical(df_empagg["RIESGO"], ["A", "B", "C", "D"], ordered=True)
df_empagg["ESTADO"] = pd.Categorical(df_empagg["ESTADO"], ["VIGENTE", "VENCIDO"], ordered=True)
df_empagg["STATUS OPERATIVO"] = pd.Categorical(
    df_empagg["STATUS OPERATIVO"], ["OPERANDO", "FUERA DE OPERACIÓN"], ordered=True
)

fig4 = px.sunburst(
    df_empagg,
    path=["RIESGO", "ESTADO", "STATUS OPERATIVO"],
    values="TOTAL",
    color="RIESGO",
    color_discrete_map={"A": "#c24444", "B": "#f19935", "C": "#f2e205", "D": "#44c28c"},
    branchvalues="total"
)
fig4.update_traces(
    textinfo="label+value+percent root",
    hovertemplate="%{value} %{parent} %{label} = %{percentRoot:.0%} del Total<extra></extra>",
    marker=dict(line=dict(color="white", width=1)),
)
fig4.update_layout(
    title_text="Emplazamientos: Riesgo - Estado & Status Operativo",
    title_x=0.5,
    title_font=dict(family="Arial Black", size=24),
)
aplicar_tema(fig4)

# --- fig5: Barras horizontales por mecanismo (EMP)
mecanismos_emp = df_filtrado["MECANISMO DE DAÑO"].value_counts().reset_index()
mecanismos_emp.columns = ["MECANISMO DE DAÑO", "TOTAL"]
mecanismos_emp_ordenado = mecanismos_emp.sort_values(by="TOTAL", ascending=True)

fig5 = px.bar(
    mecanismos_emp_ordenado,
    x="TOTAL", y="MECANISMO DE DAÑO",
    title="Mecanismo de daño por emplazamiento",
    labels={"TOTAL": "Cantidad", "MECANISMO DE DAÑO": "Mecanismo de daño"},
    color_discrete_sequence=["#118DFF"],
    orientation="h",
    text_auto=True
)
fig5.update_layout(
    title=dict(text="<b>Mecanismo de daño por emplazamiento</b>", x=0.5),
    font=dict(size=18)   # color lo hereda del tema
)
fig5.update_traces(
    textposition="outside",
    texttemplate="%{value}",
    outsidetextfont=dict(family="Arial Black", size=15, color=text_color),
    cliponaxis=False
)
aplicar_tema(fig5)

# ====== DATOS SF ======
df_sf  = pd.read_sql('SELECT * FROM "VISTA_SF";', conexion)
matriz_sf = pd.crosstab(df_sf["SECTOR"], df_sf["ESTADO"]).reindex(
    columns=["VIGENTE", "VENCIDO"], fill_value=0
)

# --- fig6: Barras SF VIGENTE/VENCIDO por sector
fig6 = px.bar(
    matriz_sf,
    x=matriz_sf.index, y=["VIGENTE", "VENCIDO"],
    title="Solicitudes de Fabricación por Sector",
    labels={"value": "Cantidad", "SECTOR": "Sector"},
    color_discrete_sequence=["#58C7BE", "#52A59E"],
    barmode="stack",
    text_auto=True
)
fig6.update_layout(
    title=dict(
        text="Solicitudes de Fabricación por Sector",
        x=0.5, xanchor="center", yanchor="top",
        font=dict(family="Arial Black", size=24)
    ),
)
fig6.update_xaxes(
    title_text="Sector",
    title_font=dict(size=20, family="Arial Black"),
    tickfont=dict(size=20, family="Arial")
)
fig6.update_yaxes(
    title_text="Cantidad",
    title_font=dict(size=20, family="Arial Black"),
    tickfont=dict(size=20, family="Arial")
)
fig6.update_traces(
    textfont_size=20,
    textangle=0,
    textposition="inside",
    hovertemplate="Sector %{x}<br>%{y} %{fullData.name}<extra></extra>",
)
aplicar_tema(fig6)

# --- fig7: Pie Operando / Fuera de operación (SF)
sf_op = df_sf[df_sf["ESTADO"].isin(["VIGENTE", "VENCIDO"])]
sf_totales = sf_op["STATUS OPERATIVO"].value_counts().reset_index()
sf_totales.columns = ["STATUS OPERATIVO", "TOTAL"]

fig7 = px.pie(
    sf_totales,
    names="STATUS OPERATIVO",
    values="TOTAL",
    title="Solicitudes de fabricación Operando y Fuera de Operación",
    color="STATUS OPERATIVO",
    color_discrete_map={"OPERANDO": "#58C7BE", "FUERA DE OPERACION": "#52A59E"},
)
fig7.update_layout(
    title=dict(
        text="Solicitudes de fabricación Operando y Fuera de Operación",
        x=0.5, xanchor="center", yanchor="top",
        font=dict(family="Arial Black", size=24)
    ),
)
fig7.update_traces(
    pull=[0.1, 0],
    textposition="inside",
    textinfo="percent+label",
    textfont_size=20,
    hovertemplate="%{value} %{label}<extra></extra>"
)
aplicar_tema(fig7)

# --- fig8: Donut por RIESGO (SF)
sf_riesgo = sf_op["RIESGO"].value_counts().reset_index()
sf_riesgo.columns = ["RIESGO", "TOTAL"]

fig8 = px.pie(
    sf_riesgo,
    names="RIESGO",
    values="TOTAL",
    title="Clase de riesgo en Solicitudes de Fabricación",
    color="RIESGO",
    color_discrete_map={"A": "#c24444", "B": "#f19935", "C": "#f2e205", "D": "#44c28c"},
    hole=0.7
)
fig8.update_layout(
    title=dict(
        text="Clase de riesgo en Solicitudes de Fabricación",
        x=0.5, xanchor="center", yanchor="top",
        font=dict(family="Arial Black", size=24)
    ),
)
fig8.update_traces(
    pull=[0.1, 0.01, 0.02, 0.03],
    textposition="outside",
    textinfo="label+value+percent",
    textfont_size=20,
    marker=dict(line=dict(color="white", width=2))
)
aplicar_tema(fig8)

# --- fig9: Sunburst Riesgo → Estado → Status Operativo (SF)
sf_sb = sf_op.copy()
sf_sb["RIESGO"] = sf_sb["RIESGO"].fillna("Sin dato").astype(str).str.upper()
sf_sb["ESTADO"] = sf_sb["ESTADO"].str.upper()
sf_sb["STATUS OPERATIVO"] = sf_sb["STATUS OPERATIVO"].str.upper()

df_agg = (
    sf_sb.groupby(["RIESGO", "ESTADO", "STATUS OPERATIVO"])
         .size().reset_index(name="TOTAL")
)
df_agg["RIESGO"] = pd.Categorical(df_agg["RIESGO"], ["A", "B", "C", "D"], ordered=True)
df_agg["ESTADO"] = pd.Categorical(df_agg["ESTADO"], ["VIGENTE", "VENCIDO"], ordered=True)
df_agg["STATUS OPERATIVO"] = pd.Categorical(
    df_agg["STATUS OPERATIVO"], ["OPERANDO", "FUERA DE OPERACIÓN"], ordered=True
)

fig9 = px.sunburst(
    df_agg,
    path=["RIESGO", "ESTADO", "STATUS OPERATIVO"],
    values="TOTAL",
    color="RIESGO",
    color_discrete_map={"A": "#c24444", "B": "#f19935", "C": "#f2e205", "D": "#44c28c"},
    branchvalues="total"
)
fig9.update_traces(
    textinfo="label+value+percent root",
    hovertemplate="%{value} %{parent} %{label} = %{percentRoot:.0%} del Total<extra></extra>",
    marker=dict(line=dict(color="white", width=1)),
)
fig9.update_layout(
    title_text="Solicitudes de Fabricación: Riesgo - Estado & Status Operativo",
    title_x=0.5,
    title_font=dict(family="Arial Black", size=24),
)
aplicar_tema(fig9)

# --- fig10: Barras horizontales por mecanismo (SF)
sf_mecanismos = sf_op["MECANISMO DE DAÑO"].value_counts().reset_index()
sf_mecanismos.columns = ["MECANISMO DE DAÑO", "TOTAL"]
sf_mecanismos_ordenado = sf_mecanismos.sort_values(by="TOTAL", ascending=True)

fig10 = px.bar(
    sf_mecanismos_ordenado,
    x="TOTAL", y="MECANISMO DE DAÑO",
    title="Mecanismo de daño por Solicitudes de Fabricación",
    labels={"TOTAL": "Cantidad", "MECANISMO DE DAÑO": "Mecanismo de daño"},
    color_discrete_sequence=["#52A59E"],
    orientation="h",
    text_auto=True
)
fig10.update_layout(
    title=dict(text="<b>Mecanismo de daño por Solicitudes de Fabricación</b>", x=0.5),
    font=dict(size=18)
)
fig10.update_traces(
    textposition="outside",
    texttemplate="%{value}",
    outsidetextfont=dict(family="Arial Black", size=15, color=text_color),
    cliponaxis=False
)
aplicar_tema(fig10)



#fig1.show() #Gráfico de emplazamientos por sector vigentes y vencidos
#fig2.show() #Gráfico de pastel de emplazamientos operando y fuera de operación
#fig3.show() #Gráfico de Riesgos en Emplazamientos
#fig4.show() #Gráfico Sunbrust Riesgo de Emplazamientos
#fig5.show() #Gráfico de Mecanismo de daños en emplazamientos
#fig6.show() #Gráfico de SF por sector vigentes y vencidos
#fig7.show() #Gráfico de pastel de SF operando y fuera de operación
#fig8.show() #Gráfico de Riesgos en SF
#fig9.show() #Gráfico Sunbrust Riesgo de SF
#fig10.show() #Gráfico de Mecanismo de daños en SF



