import dash_bootstrap_components as dbc
from dash import dcc, html


def generar_barra_navegacion() -> dbc.Navbar:
    """
    Genera una barra de navegación para la página web.

    :return: La barra de navegación.
    :rtype: dbc.Navbar
    """
    barra_navegacion = dbc.Navbar(
        dbc.Container([

            dbc.NavItem(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src="/assets/icons/simulation.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("UTN FRC - Simulación",
                                                className="ms-2", href="/")),
                    ],
                    align="center",
                    className="g-0",
                )),

            dbc.NavItem(
                dbc.NavLink("Inicio", href="/", style={"color": "white"}),
                class_name="ms-auto px-1"),

            dbc.NavItem(
                dbc.NavLink("TP2", href="/tp2/", style={"color": "white"}),
                class_name="px-3"),

            html.A(
                html.Img(src="/assets/icons/github-mark-white.svg",
                         height="30px"),
                href="https://github.com/FranGiordano/utn-frc-sim-tp2",
                style={"textDecoration": "none"},
                target="_blank"
            ),
        ]),
        color="primary",
        dark=True
    )

    return barra_navegacion


def generar_tipos_distribuciones() -> dbc.InputGroup:
    """
    Genera un dropdown para la selección del tipo de distribución.

    :return: El dropdown de distribuciones.
    :rtype: dbc.InputGroup
    """

    tipo_distribucion = dbc.InputGroup([
        dbc.Select(
            id="controls-dist",
            options=[
                {"label": "Exponencial Negativa", "value": "EN"},
                {"label": "Normal", "value": "N"},
                {"label": "Poisson", "value": "P"},
                {"label": "Uniforme", "value": "U"},
            ],
            value="U"
        ),
        dbc.InputGroupText("Distribución")
    ])

    return tipo_distribucion


def generar_parametros() -> dbc.Row:
    """
    Genera una fila con los forms de parámetros y el botón de generar gráfico.

    :return: La fila con los forms de parámetros y el botón de generar gráfico.
    :rtype: dbc.Row
    """
    parametros = dbc.Row([

        dbc.Col(id="form-cantidad", children=[
            dbc.FormFloating([
                dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number",
                          min=0, step=1, value=10000, required=True),
                dbc.Label("Cantidad de muestras"),
            ])]),

        dbc.Col(id='form-intervalos',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_intervalos",
                                  placeholder="Cantidad de intervalos",
                                  type="number", min=1, step=1,
                                  value=15, required=True),
                        dbc.Label("Cantidad de intervalos"),
                    ])]),

        dbc.Col(id="form-limite-inferior", children=[
            dbc.FormFloating([
                dbc.Input(id="in_limite_inferior", placeholder="Límite inferior", type="number",
                          value=-10, required=True, step=0.0001),
                dbc.Label("Límite inferior"),
            ])], style={"display": "none"}),

        dbc.Col(id="form-limite-superior", children=[
            dbc.FormFloating([
                dbc.Input(id="in_limite_superior", placeholder="Límite superior", type="number",
                          value=10, required=True, step=0.0001),
                dbc.Label("Límite superior"),
            ])], style={"display": "none"}),

        dbc.Col(id='form-media',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_media", placeholder="Media", type="number",
                                  value=0, required=True, step=0.0001),
                        dbc.Label("Media"),
                    ])], style={"display": "none"}),

        dbc.Col(id="form-desv", children=[
            dbc.FormFloating([
                dbc.Input(id="in_desviacion", placeholder="Desviación Estándar", type="number", min=0.0001,
                          value=1, required=True, step=0.0001),
                dbc.Label("Desviación Estándar"),
            ])], style={"display": "none"}),

        dbc.Col(id="form-lambda", children=[
            dbc.FormFloating([
                dbc.Input(id="in_lambda", placeholder="Lambda", type="number",
                          value=5, required=True, step=0.0001, min=0.0001),
                dbc.Label("Lambda"),
            ])], style={"display": "none"}),

        dbc.Col(dbc.Button("Generar distribución",
                           id="btn_cargar_grafico",
                           color="primary"),
                class_name="col-auto align-self-end")
    ])

    return parametros


def generar_visualizacion(histograma, muestras, datos_frecuencias, datos_chi2, datos_ks=None) -> html.Div:
    """
    Genera las visualizaciones a los resultados procesados.

    :param histograma: Figura del histograma.
    :type histograma: go.Figure
    :param muestras: Lista de elementos de la muestra.
    :type muestras: list[float]
    :param datos_frecuencias: Diccionario con los datos de frecuencias.
    :type datos_frecuencias: dict[str, list[float]]
    :param datos_chi2: Diccionario con los datos de la prueba de chi2.
    :type datos_chi2: dict[str, float]
    :param datos_ks: Diccionario con los datos de la prueba de ks.
    :type datos_ks: dict[str, float]
    :return: Un div con las visualizaciones.
    :rtype: html.Div
    """

    visualizacion = html.Div([

        # Histograma

        dcc.Graph(figure=histograma),

        dbc.Accordion([

            # Frecuencias observadas y esperadas

            dbc.AccordionItem(html.Div(crear_tabla(datos_frecuencias), className="table-container"),
                              title="Frecuencias observadas y esperadas"),

            # Pruebas de ajuste

            dbc.AccordionItem([
                dbc.Row([
                    crear_columna_chi2(datos_chi2),
                    crear_columna_ks(datos_ks) if datos_ks is not None else dbc.Col(class_name="d-none"),
                ])
            ], title="Pruebas de bondad de ajuste"),

            # Números generados

            dbc.AccordionItem([
                html.Div([
                    html.Ul([html.Li(str(round(n, 2))) for n in muestras[:1000]], className="columnas")
                ], className="table-container"),
            ], title="Lista de 1000 primeros números generados"),

        ], start_collapsed=True, always_open=True),
    ])

    return visualizacion


def crear_columna_chi2(datos_chi2) -> dbc.Col:
    """
    Genera la columna correspondiente a las pruebas de chi2

    :param datos_chi2: Diccionario con los datos de la prueba de chi2.
    :type datos_chi2: dict[str, float]
    :return: La columna con las visualizaciones correspondientes.
    :rtype: dbc.Col
    """

    # Se crea una alerta en base al resultado de la prueba

    if datos_chi2["Grados de libertad"] <= 0:
        alerta = dbc.Alert("La cantidad de muestras no es suficiente para conseguir el χ2 tabulado ó se presentó un "
                           "error de cálculo", color="danger")
    elif datos_chi2["χ2 calculado"] <= datos_chi2["χ2 tabulado"]:
        alerta = dbc.Alert(
            "El test de χ2 no rechaza la hipótesis nula", color="success")
    else:
        alerta = dbc.Alert(
            "El test de χ2 rechaza la hipótesis nula", color="danger")

    # Se genera una columna con: título, alerta y tabla

    columna_chi2 = dbc.Col([
        html.Center(html.H4("Chi-cuadrado")),
        crear_tabla(datos_chi2),
        alerta
    ])

    return columna_chi2


def crear_columna_ks(datos_ks):
    """
    Genera la columna correspondiente a las pruebas de ks

    :param datos_ks: Diccionario con los datos de la prueba de ks.
    :type datos_ks: dict[str, float]
    :return: La columna con las visualizaciones correspondientes.
    :rtype: dbc.Col
    """

    # Se crea una alerta en base al resultado de la prueba

    if datos_ks["K-S calculado"] <= datos_ks["K-S tabulado"]:
        alerta = dbc.Alert(
            "El test de K-S no rechaza la hipótesis nula", color="success")
    else:
        alerta = dbc.Alert(
            "El test de K-S rechaza la hipótesis nula", color="danger")

    # Se genera una columna con: título, alerta y tabla

    columna_ks = dbc.Col([
        html.Center(html.H4("Kolmogorov-Smirnov")),
        crear_tabla(datos_ks),
        alerta
    ])

    return columna_ks


def crear_tabla(diccionario) -> dbc.Table:
    """
    Genera una tabla en base a los datos de un diccionario.

    :param diccionario: Un diccionario con keys de tipo str y values de tipo list[float] o float
    :type diccionario: Union[dict[str,list[float]], dict[str, float]]
    :return: La tabla con los valores correspondientes.
    :rtype: dbc.Table
    """

    # Se crea el encabezado de la tabla

    table_header = [html.Thead(html.Tr([html.Th(i) for i in diccionario.keys()]))]

    # Se crea el cuerpo de la tabla

    rows = []
    lista_body = list(diccionario.values())

    # Para la creación de las filas se itera sobre las listas contenidas en cada value del diccionario. En caso de que
    # el value esté dado por un escalar y no por una lista, se convierte este escalar a lista:

    try:
        n = len(lista_body[0])
    except TypeError:
        lista_body = [[escalar] for escalar in lista_body]
        n = 1

    for i in range(n):
        row = html.Tr([html.Td(lista[i]) for lista in lista_body])
        rows.append(row)

    table_body = [html.Tbody(rows)]

    # Creación de la tabla

    table = dbc.Table(table_header + table_body, class_name="w-auto mx-auto", striped=True, bordered=True,
                      responsive=True)

    return table
