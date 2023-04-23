import math
import random as rd
from scipy.stats import kstwo, chi2


# =====================================================================================================================
#
# GENERADORES
#
# =====================================================================================================================

def generar_serie_uniforme(n, a, b) -> list[float]:
    """
    Genera una serie de n números aleatorios manteniendo una distribución uniforme.

    :param n: Cantidad de elementos a generar en la serie.
    :type n: int
    :param a: Límite inferior de la distribución.
    :type a: float
    :param b: Límite superior de la distribución.
    :type b: float
    :return: Una serie de n números con distribución uniforme.
    :rtype: list[float]
    """

    if a > b:
        a, b = b, a

    muestras = []
    for i in range(n):
        muestras.append(rd.random() * (b - a) + a)

    return muestras


def generar_serie_normal(n, media, desviacion) -> list[float]:
    """
    Genera una serie de n números aleatorios manteniendo una distribución normal.

    :param n: Cantidad de elementos a generar en la serie.
    :type n: int
    :param desviacion: La desviación estándar de la distribución.
    :type desviacion: float
    :param media: La media de la distribución.
    :type media: float
    :return: Una serie de n números aleatorios con distribución normal.
    :rtype: list[float]
    """
    numeros_aleatorios = []
    for i in range(n):
        r1 = rd.random()
        r2 = rd.random()
        while r1 == 0:
            r1 = rd.random()
        z = math.sqrt(-2.0 * math.log(r1)) * math.cos(2 * math.pi * r2)
        numeros_aleatorios.append(media + desviacion * z)
    return numeros_aleatorios


def generar_serie_exponencial_negativa(n, lam) -> list[float]:
    """
    Genera una serie de n números aleatorios manteniendo una distribución exponencial negativa.

    :param n: Cantidad de elementos a generar en la serie.
    :type n: int
    :param lam: El valor Lambda de la distribución.
    :type lam: float
    :return: Una serie de n números aleatorios con distribución exponencial negativa.
    :rtype: list[float]
    """

    muestras = []
    for i in range(n):
        muestras.append(-(1 / lam) * math.log(1 - rd.random()))

    return muestras


def generar_serie_poisson(n, lam) -> list[int]:
    """
    Genera una serie de n números aleatorios manteniendo una distribución de Poisson.

    :param n: Cantidad de elementos a generar en la serie.
    :type n: int
    :param lam: El valor Lambda de la distribución.
    :type lam: float
    :return: Una serie de n números aleatorios con distribución de Poisson.
    :rtype: list[int]
    """

    serie = []
    for i in range(n):
        p = 1
        x = -1
        a = math.e ** (-lam)
        while p >= a:
            u = rd.random()
            p *= u
            x = x + 1
        serie.append(x)
    return serie


# =====================================================================================================================
#
# CÁLCULOS DE FRECUENCIA OBSERVADA Y ESPERADA
#
# =====================================================================================================================

def calcular_parametros(muestras) -> (int, float, float, float):

    cant_muestras = len(muestras)

    media = sum(muestras) / cant_muestras

    varianza = 0
    for i in muestras:
        varianza += (i - media) ** 2
    varianza /= cant_muestras - 1

    desv_est = math.sqrt(varianza)

    return cant_muestras, media, varianza, desv_est


def generar_intervalos_dist_continua(muestras, cant_intervalos) -> (list[float], list[float], list[float], list[int]):

    # Cálculos iniciales

    maximo = max(muestras)
    minimo = min(muestras)
    rango = (maximo - minimo) / cant_intervalos

    # Generación de listas de límite inferior y superior

    lista_li = [minimo]
    lista_ls = [minimo + rango]

    for i in range(1, cant_intervalos):
        lista_li.append(lista_ls[i - 1])
        lista_ls.append(lista_ls[i - 1] + rango)

    # Generación de lista de marcas

    lista_marca = []
    for i in range(cant_intervalos):
        lista_marca.append((lista_ls[i] + lista_li[i]) / 2)

    # Generación de lista de frecuencia observada

    lista_frec_observada = [0] * cant_intervalos

    for i in muestras:
        for j in range(cant_intervalos):
            if lista_li[j] <= i < lista_ls[j]:
                lista_frec_observada[j] += 1
                break

    lista_frec_observada[-1] += muestras.count(maximo)

    # Retornos

    return lista_li, lista_ls, lista_marca, lista_frec_observada


def generar_intervalos_dist_discreta(muestras) -> (list[int], list[int]):

    # Cálculos iniciales

    maximo = max(muestras)
    minimo = min(muestras)

    # Generación de lista de marcas

    lista_marca = [i for i in range(minimo, maximo + 1)]

    # Generación de lista de frecuencias observadas

    lista_frec_observada = []
    for n in lista_marca:
        lista_frec_observada.append(muestras.count(n))

    # Retorno

    return lista_marca, lista_frec_observada


def calcular_frecuencia_esperada_uniforme(cant_muestras, cant_intervalos) -> list[float]:

    # Generación de lista de frecuencia esperada

    lista_frec_esperada = [cant_muestras / cant_intervalos] * cant_intervalos

    # Retorno

    return lista_frec_esperada


def calcular_frecuencia_esperada_normal(lista_li, lista_ls, lista_marca, cant_muestras, media, desv_est) -> list[float]:

    # Generación de lista de frecuencia esperada

    lista_frec_esperada = []
    for i in range(len(lista_marca)):
        numerador = math.exp(-(1 / 2) * ((lista_marca[i] - media) / desv_est) ** 2)
        denominador = (1 / (desv_est * math.sqrt(2 * math.pi)))
        probabilidad = numerador * denominador * (lista_ls[i] - lista_li[i])
        lista_frec_esperada.append(probabilidad * cant_muestras)

    # Retorno

    return lista_frec_esperada


def calcular_frecuencia_esperada_exp_neg(lista_li, lista_ls, cant_muestras, media) -> list[float]:

    # Cálculos iniciales

    lam = 1 / media

    # Generación de lista de frecuencia esperada

    lista_frec_esperada = []
    for i in range(len(lista_li)):
        probabilidad = -math.exp(-lam * lista_ls[i]) + math.exp(-lam * lista_li[i])
        lista_frec_esperada.append(probabilidad * cant_muestras)

    # Retorno

    return lista_frec_esperada


def calcular_frecuencia_esperada_poisson(lista_marca, lam, cant_muestras) -> list[float]:

    # Generación de lista de frecuencias esperadas

    lista_frec_esperada = []
    for n in lista_marca:
        probabilidad = lam ** n * math.exp(-lam) / math.factorial(n)
        lista_frec_esperada.append(int(round(probabilidad * cant_muestras, 0)))

    # Retorno

    return lista_frec_esperada


# =====================================================================================================================
#
# PRUEBAS DE BONDAD DE AJUSTE
#
# =====================================================================================================================

def calcular_chi2(lista_frec_observada, lista_frec_esperada, distribucion) -> (float, float, int, float):

    # Agrupamiento de frecuencias de forma que cada valor de frecuencias esperadas sea >= 5:

    nuevo_fo = []
    nuevo_fe = []

    acum_fe = 0
    acum_fo = 0

    for i in range(len(lista_frec_esperada)):

        acum_fe += lista_frec_esperada[i]
        acum_fo += lista_frec_observada[i]

        if acum_fe >= 5:
            nuevo_fe.append(acum_fe)
            nuevo_fo.append(acum_fo)
            acum_fe = 0
            acum_fo = 0

    if not nuevo_fe:
        nuevo_fe.append(acum_fe)
        nuevo_fo.append(acum_fo)
    elif acum_fo > 0 or acum_fe > 0:
        nuevo_fe[-1] += acum_fe
        nuevo_fo[-1] += acum_fo

    lista_frec_observada = nuevo_fo
    lista_frec_esperada = nuevo_fe

    # Chi-Cuadrado calculado:

    chi2_calculado = 0
    for i in range(len(lista_frec_observada)):
        chi2_calculado += (lista_frec_observada[i] - lista_frec_esperada[i]) ** 2 / lista_frec_esperada[i]

    # Chi-Cuadrado tabulado:

    m = {"U": 0, "EN": 1, "N": 2, "P": 1}
    k = len(lista_frec_observada)
    try:
        grados_libertad = k - 1 - m[distribucion]
    except KeyError:
        raise NameError
    nivel_de_confianza = 0.95
    chi2_tabulado = chi2.ppf(nivel_de_confianza, grados_libertad)

    # Retorno

    return chi2_calculado, chi2_tabulado, nivel_de_confianza, grados_libertad


def calcular_ks(lista_frec_observada, lista_frec_esperada) -> (float, float, float):

    # Constantes

    cant_muestras = sum(lista_frec_observada)

    # K-S calculado:

    ks_calculado = po_acum = pe_acum = 0
    for i in range(len(lista_frec_observada)):
        po_acum += lista_frec_observada[i] / cant_muestras
        pe_acum += lista_frec_esperada[i] / cant_muestras
        dif = abs(po_acum - pe_acum)
        if dif > ks_calculado:
            ks_calculado = dif

    # K-S tabulado:

    nivel_de_confianza = 0.95
    ks_tabulado = kstwo.ppf(nivel_de_confianza, cant_muestras)

    # Retornos

    return ks_calculado, ks_tabulado, nivel_de_confianza
