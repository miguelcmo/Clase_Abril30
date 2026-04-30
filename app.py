import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard IoT")

# Subir archivo
file = st.file_uploader("Sube tu archivo CSV")

if file:
    df = pd.read_csv(file)

    # Filtros
    if "device_id" in df.columns:
        device_ids = df["device_id"].unique()
        selected_device = st.selectbox("Filtrar por device_id", options=device_ids)
        df = df[df["device_id"] == selected_device]

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        start_date = st.date_input("Fecha inicial", df["timestamp"].min())
        end_date = st.date_input("Fecha final", df["timestamp"].max())
        df = df[(df["timestamp"] >= pd.to_datetime(start_date)) & (df["timestamp"] <= pd.to_datetime(end_date))]

    st.write("Vista previa de los datos:", df.head())

    # Estadísticas
    temp_mean = df["temperature"].mean()
    energy_mean = df["energy_consumption"].mean()
    vibration_max = df["vibration"].max()
    state_counts = df["state"].value_counts() if "state" in df.columns else None

    st.write("Temperatura promedio:", round(temp_mean, 2))
    st.write("Consumo energético promedio:", round(energy_mean, 2))
    st.write("Máxima vibración:", vibration_max)
    if state_counts is not None:
        st.write("Conteo de estados:", state_counts)

    # Gráficas
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

    # Interpretaciones dinámicas
    st.subheader("Interpretaciones")
    if temp_mean > 30:
        st.warning("Advertencia: La temperatura promedio supera los 30°C.")
    if state_counts is not None and "FAIL" in state_counts.index and state_counts["FAIL"] > 0:
        st.error("Alerta: Se detectaron registros en estado FAIL.")
