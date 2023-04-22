import streamlit as st
import soporte.simulacion as sim

# Título de la aplicación
st.title("Generador de Números Aleatorios")

# Entrada de parámetros
distribucion = {"Normal": "N",
                        "Uniforme": "U",
                        "Exponencial": "EN",
                        "Poisson": "P"}

dist_choice = st.selectbox("Selecciona una distribución", distribucion)
muestras = []
cant_intervalos = 1


if dist_choice in ["Normal", "Uniforme", "Exponencial"]:
    if dist_choice == "Normal":
        mean = st.number_input("Media", value=0.0, step=0.1)
        std = st.number_input("Desviación estándar", value=1.0, step=0.1)
        size = st.number_input("Tamaño de la muestra", value=10000, step=1)
        muestras = sim.generar_serie_normal(size, std, mean)

    elif dist_choice == "Uniforme":
        low = st.number_input("Valor mínimo", value=0.0, step=0.1)
        high = st.number_input("Valor máximo", value=1.0, step=0.1)
        size = st.number_input("Tamaño de la muestra", value=10000, step=1)
        muestras = sim.generar_serie_uniforme(size, low, high)

    elif dist_choice == "Exponencial":
        lam = st.number_input("Lambda", value=5.0, step=0.1)
        size = st.number_input("Tamaño de la muestra", value=10000, step=1)
        muestras = sim.generar_serie_exponencial_negativa(size, lam)

    cant_intervalos = st.number_input("Cantidad de Intervalos", value=10, step=1)

    if st.button("Generar Histograma"):
        fig = sim.generar_histograma_continua(muestras, cant_intervalos)
        st.plotly_chart(fig)

        t_datos = sim.calcular_frecuencias_continua(muestras, cant_intervalos, distribucion[dist_choice])
        st.table(t_datos)


elif dist_choice == "Poisson":
    lam = st.number_input("Lambda", value=5.0, step=0.1)
    size = st.number_input("Tamaño de la muestra", value=10000, step=1)
    muestras = sim.generar_serie_poisson(size, lam)

    if st.button("Generar Histograma Poisson"):
        fig = sim.generar_histograma_poisson(muestras)
        st.plotly_chart(fig)

        t_datos = sim.calcular_frecuencias_poisson(muestras)
        st.table(t_datos)
