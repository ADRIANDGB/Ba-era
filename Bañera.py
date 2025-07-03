import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Curva de la Bañera - Fallas de Luminarias")

# Cargar datos de ejemplo
df = pd.DataFrame({
    "ID": ["LUM-01", "LUM-02", "LUM-03"],
    "Horas_Funcionamiento": [50, 15000, 41000],
    "MTBF": [100000, 100000, 100000],
    "Fecha_Instalacion": ["2022-01-01", "2020-01-01", "2018-01-01"],
    "Fecha_Falla": ["2022-03-01", "2023-06-01", "2023-01-01"],
    "Ubicacion": ["Parque A", "Avenida B", "Calle C"]
})

# Crear curva de la bañera
x = list(range(0, 50001, 1000))
y = [0.001 + (1 / (i + 500)) if i < 10000 else 0.001 for i in x]
y += [((i - 30000)**2 / 1e9) + 0.001 for i in x if i > 30000]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x[:len(y)], y=y, mode='lines', line=dict(color='blue'), name='Curva de la bañera'))

# Zonas
fig.add_vrect(x0=0, x1=10000, fillcolor="lightgray", opacity=0.3, annotation_text="Fallas tempranas", annotation_position="top left")
fig.add_vrect(x0=10000, x1=30000, fillcolor="lightgreen", opacity=0.3, annotation_text="Fallas aleatorias", annotation_position="top left")
fig.add_vrect(x0=30000, x1=50000, fillcolor="salmon", opacity=0.3, annotation_text="Desgaste", annotation_position="top left")

# Puntos de los equipos
for _, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["Horas_Funcionamiento"]],
        y=[0.005],
        mode="markers",
        marker=dict(size=10, color='red'),
        name=row["ID"],
        hovertemplate=
            f"<b>ID:</b> {row['ID']}<br>" +
            f"<b>Ubicación:</b> {row['Ubicacion']}<br>" +
            f"<b>Horas:</b> {row['Horas_Funcionamiento']}<br>" +
            f"<b>Instalación:</b> {row['Fecha_Instalacion']}<br>" +
            f"<b>Falla:</b> {row['Fecha_Falla']}<extra></extra>"
    ))

fig.update_layout(
    title="Curva de la Bañera - Visualización de Fallas",
    xaxis_title="Horas de funcionamiento",
    yaxis_title="Tasa de fallas (referencial)",
    showlegend=False,
    height=500
)

st.plotly_chart(fig, use_container_width=True)
