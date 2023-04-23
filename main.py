import streamlit as st
import soporte.simulacion as sim
from plotly import graph_objs as go


# Título de la aplicación
st.title("Generador de Números Aleatorios")

# Entrada de parámetros
distribucion = {"Normal": "N",
                "Uniforme": "U",
                "Exponencial": "EN",
                "Poisson": "P"}

dc = st.selectbox("Selecciona una distribución", distribucion)
muestras = []
cant_intervalos = 1

def crear_histograma(lista_marca, lista_frec_observada, lista_frec_esperada) -> go.Figure:
    """
    Genera un histograma para una distribución.

    :param lista_frec_observada: 1ra lista de valores a representar en el eje y.
    :type lista_frec_observada: list[int]
    :param lista_frec_esperada: 2da lista de valores a representar en el eje y.
    :type lista_frec_esperada: list[float]
    :param lista_marca: Valores a representar en el eje x.
    :type lista_marca: list[float]
    :return: Figura con el histograma generado.
    :rtype: go.Figure
    """

    # Creación de histograma

    fig = go.Figure(
        layout=go.Layout(
            xaxis={"title": "Marca de clase"},
            yaxis={"title": "Frecuencia"}

        )
    )

    fig.add_trace(
        go.Bar(
            x=lista_marca,
            y=lista_frec_observada,
            name="Frecuencia observada",
            marker_line={"width": 1, "color": "black"}
        )
    )

    fig.add_trace(
        go.Bar(
            x=lista_marca,
            y=lista_frec_esperada,
            name="Frecuencia esperada",
            marker_line={"width": 1, "color": "black"}
        )
    )

    return fig




n = st.number_input("Tamaño de la muestra", value=10000, step=1)

if distribucion[dc] == "N":
        media = st.number_input("Media", value=0.0, step=0.1)
        desv = st.number_input("Desviación estándar", value=1.0, step=0.1)

elif distribucion[dc] == "U":
    li = st.number_input("Valor mínimo", value=0.0, step=0.1)
    ls = st.number_input("Valor máximo", value=1.0, step=0.1)

elif distribucion[dc] in ["EN", "P"]:
    lam = st.number_input("Lambda", value=5.0, step=0.1)

if distribucion[dc] in ["N", "U", "EN"]:
    intervalos = st.number_input("Cantidad de Intervalos", value=15, step=1)

if st.button("Generar Histograma"):

    match distribucion[dc]:

        case "U":

            # Generación de muestras
            serie = sim.generar_serie_uniforme(int(n), float(li), float(ls))

            # Cálculo de parámetros
            cant_muestras, media, varianza, desv_est = sim.calcular_parametros(serie)

            # Generación de intervalos, frecuencias observadas y esperadas
            lista_li, lista_ls, lista_marca, lista_fo = sim.generar_intervalos_dist_continua(serie, int(intervalos))
            lista_fe = sim.calcular_frecuencia_esperada_uniforme(cant_muestras, int(intervalos))

        case "N":

            # Generación de muestras
            serie = sim.generar_serie_normal(int(n), float(media), float(desv))

            # Cálculo de parámetros
            cant_muestras, media, varianza, desv_est = sim.calcular_parametros(serie)

            # Generación de intervalos, frecuencias observadas y esperadas
            lista_li, lista_ls, lista_marca, lista_fo = sim.generar_intervalos_dist_continua(serie, int(intervalos))
            lista_fe = sim.calcular_frecuencia_esperada_normal(lista_li, lista_ls, lista_marca, cant_muestras, media,
                                                               desv_est)

        case "EN":


            # Generación de muestras
            serie = sim.generar_serie_exponencial_negativa(int(n), float(lam))

            # Cálculo de parámetros
            cant_muestras, media, varianza, desv_est = sim.calcular_parametros(serie)

            # Generación de intervalos, frecuencias observadas y esperadas
            lista_li, lista_ls, lista_marca, lista_fo = sim.generar_intervalos_dist_continua(serie, int(intervalos))
            lista_fe = sim.calcular_frecuencia_esperada_exp_neg(lista_li, lista_ls, cant_muestras, media)

        case "P":

            # Generación de muestras
            serie = sim.generar_serie_poisson(int(n), float(lam))

            # Cálculo de parámetros
            cant_muestras, media, varianza, desv_est = sim.calcular_parametros(serie)

            # Generación de intervalos, frecuencias observadas y esperadas
            lista_marca, lista_fo = sim.generar_intervalos_dist_discreta(serie)
            lista_fe = sim.calcular_frecuencia_esperada_poisson(lista_marca, media, cant_muestras)

        # Prueba de bondad de ajuste

    chi2_calculado, chi2_tabulado, nivel_de_confianza, grados_libertad = sim.calcular_chi2(lista_fo, lista_fe,
                                                                                           distribucion[dc])
    ks_calculado, ks_tabulado, nivel_de_confianza = sim.calcular_ks(lista_fo, lista_fe)

    # Carga de datos en diccionarios

    if distribucion in ["U", "N", "EN"]:
        datos_frecuencia = {
            "#": range(intervalos),
            "Desde": [round(i, 4) for i in lista_li],
            "Hasta": [round(i, 4) for i in lista_ls],
            "Marca de clase": [round(i, 4) for i in lista_marca],
            "Frecuencia observada": lista_fo,
            "Frecuencia esperada": [round(i, 0) for i in lista_fe]
        }
    else:
        datos_frecuencia = {
            "#": [i for i in range(len(lista_fo))],
            "Marca de clase": lista_marca,
            "Frecuencia observada": lista_fo,
            "Frecuencia esperada": lista_fe
        }

    datos_chi2 = {
        "Nivel de confianza": nivel_de_confianza,
        "Grados de libertad": grados_libertad,
        "χ2 calculado": round(chi2_calculado, 4),
        "χ2 tabulado": round(chi2_tabulado, 4),
    }

    datos_ks = {
        "Nivel de confianza": nivel_de_confianza,
        "Cantidad de muestras": n,
        "K-S calculado": round(ks_calculado, 4),
        "K-S tabulado": round(ks_tabulado, 4)
    }

    # Generación de visualizacion

    #alerta_chi2 = crear_alerta_chi2(grados_libertad, chi2_calculado, chi2_tabulado)
    #alerta_ks = crear_alerta_ks(ks_calculado, ks_tabulado)
    histograma = crear_histograma(lista_marca, lista_fo, lista_fe)


    st.header("Histograma")
    st.plotly_chart(histograma)

    st.header("Frecuencias Observadas y Esperadas")

    st.table(datos_frecuencia)

    st.header("Pruebas de Bondad de Ajuste")
    st.subheader("Chi cuadrado")
    st.table(datos_chi2)

    # Se crea una alerta en base al resultado de la prueba

    if grados_libertad <= 0:
        st.warning(
            "La cantidad de muestras no es suficiente para conseguir el χ2 tabulado ó se presentó un "
            "error de cálculo")
    elif chi2_calculado <= chi2_tabulado:
        st.info("El test de χ2 no rechaza la hipótesis nula")
    else:
        st.error("El test de χ2 rechaza la hipótesis nula")

    st.subheader("KS")
    st.table(datos_ks)
    if ks_calculado <= ks_tabulado:
        st.info(
            "El test de K-S no rechaza la hipótesis nula")
    else:
        st.warning(
            "El test de K-S rechaza la hipótesis nula")
