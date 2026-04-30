import streamlit as st          # Importa Streamlit para crear la interfaz web
import pandas as pd             # Importa pandas para manejar y analizar datos
import matplotlib.pyplot as plt # Importa matplotlib para generar gráficas

# Título principal de la aplicación
st.title("Dashboard IoT")

# Componente para subir archivo CSV
file = st.file_uploader("Sube tu archivo CSV")

# Si el usuario sube un archivo...
if file:
    # Leer el CSV en un DataFrame de pandas
    df = pd.read_csv(file)

    # --- FILTROS ---
    # Filtrar por device_id si existe esa columna
    if "device_id" in df.columns:
        device_ids = df["device_id"].unique()
        selected_device = st.selectbox("Filtrar por device_id", options=device_ids)
        df = df[df["device_id"] == selected_device]

    # Filtrar por rango de fechas si existe columna timestamp
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        start_date = st.date_input("Fecha inicial", df["timestamp"].min())
        end_date = st.date_input("Fecha final", df["timestamp"].max())
        df = df[(df["timestamp"] >= pd.to_datetime(start_date)) & (df["timestamp"] <= pd.to_datetime(end_date))]

    # Mostrar vista previa de los datos
    st.write("Vista previa de los datos:", df.head())

    # --- ESTADÍSTICAS ---
    temp_mean = df["temperature"].mean()              # Promedio de temperatura
    energy_mean = df["energy_consumption"].mean()     # Promedio de consumo energético
    vibration_max = df["vibration"].max()             # Máximo valor de vibración
    state_counts = df["state"].value_counts() if "state" in df.columns else None  # Conteo de estados

    # Mostrar estadísticas en pantalla
    st.write("Temperatura promedio:", round(temp_mean, 2))
    st.write("Consumo energético promedio:", round(energy_mean, 2))
    st.write("Máxima vibración:", vibration_max)
    if state_counts is not None:
        st.write("Conteo de estados:", state_counts)

    # --- GRÁFICAS ---
    st.subheader("Gráficas")

    # Serie de tiempo: temperatura vs tiempo
    if "timestamp" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["timestamp"], df["temperature"])
        ax.set_title("Temperatura vs Tiempo")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Temperatura")
        st.pyplot(fig)

    # Histograma de consumo energético
    fig, ax = plt.subplots()
    ax.hist(df["energy_consumption"], bins=30, color="skyblue", edgecolor="black")
    ax.set_title("Distribución de Consumo Energético")
    ax.set_xlabel("Consumo energético")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

    # Relación entre variables: temperatura vs consumo energético
    fig, ax = plt.subplots()
    ax.scatter(df["temperature"], df["energy_consumption"], alpha=0.5)
    ax.set_title("Temperatura vs Consumo Energético")
    ax.set_xlabel("Temperatura")
    ax.set_ylabel("Consumo energético")
    st.pyplot(fig)

    # --- INTERPRETACIONES DINÁMICAS ---
    st.subheader("Interpretaciones")
    if temp_mean > 30:
        st.warning("Advertencia: La temperatura promedio supera los 30°C.")
    if state_counts is not None and "FAIL" in state_counts.index and state_counts["FAIL"] > 0:
        st.error("Alerta: Se detectaron registros en estado FAIL.")
