import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Curva de la Bañera", layout="centered")
st.title("📉 Curva de la Bañera - Registro de Fallas de Luminarias")

st.markdown("Agrega luminarias desde la barra lateral para visualizar su posición en la curva de la bañera.")

# Inicializar almacenamiento en sesión
if "data" not in st.session_state:
    st.session_state.data = []

# 📌 FORMULARIO EN SIDEBAR
with st.sidebar:
    st.header("🛠️ Ingreso de datos")
    with st.form("form_luminaria"):
        id_luminaria = st.text_input("ID del equipo", value="LUM-01")
        ubicacion = st.text_input("Ubicación", value="Parque Central")
        fecha_instalacion = st.date_input("Fecha de instalación")
        fecha_falla = st.date_input("Fecha de falla (estimada)")
        horas_funcionamiento = st.number_input("Horas de funcionamiento", min_value=0, value=12000)
        mtbf = st.number_input("MTBF estimado (horas)", min_value=1, value=100000)

        submitted = st.form_submit_button("➕ Agregar luminaria")
        if submitted:
            st.session_state.data.append({
                "ID": id_luminaria,
                "Horas_Funcionamiento": horas_funcionamiento,
                "MTBF": mtbf,
                "Fecha_Instalacion": fecha_instalacion.strftime("%Y-%m-%d"),
                "Fecha_Falla": fecha_falla.strftime("%Y-%m-%d"),
                "Ubicacion": ubicacion
            })
            st.success(f"Luminaria '{id_luminaria}' agregada correctamente.")

# Convertir datos a DataFrame
df = pd.DataFrame(st.session_state.data)

# Curva base
x = list(range(0, 50001, 1000))
y = [0.001 + (1 / (i + 500)) if i < 10000 else 0.001 for i in x]
y += [((i - 30000)**2 / 1e9) + 0.001 for i in x if i > 30000]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x[:len(y)], y=y, mode='lines', name='Curva de la bañera', line=dict(color='blue')))

# Secciones de la curva
fig.add_vrect(x0=0, x1=10000, fillcolor="lightgray", opacity=0.3, annotation_text="Fallas tempranas", annotation_position="top left")
fig.add_vrect(x0=10000, x1=30000, fillcolor="lightgreen", opacity=0.3, annotation_text="Fallas aleatorias", annotation_position="top left")
fig.add_vrect(x0=30000, x1=50000, fillcolor="salmon", opacity=0.3, annotation_text="Desgaste", annotation_position="top left")

# Puntos de luminarias
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

# Configuración del gráfico
fig.update_layout(
    title="Curva de la Bañera - Visualización Interactiva",
    xaxis_title="Horas de funcionamiento",
    yaxis_title="Tasa de fallas (referencial)",
    showlegend=False,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Mostrar tabla si hay datos
if not df.empty:
    st.markdown("### 📋 Tabla de luminarias registradas")
    st.dataframe(df, use_container_width=True)
