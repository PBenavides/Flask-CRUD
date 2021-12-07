import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.database import get_db

colores = ['rgb(247,252,245)', 'rgb(229,245,224)', 'rgb(199,233,192)', 'rgb(161,217,155)', 'rgb(116,196,118)', 'rgb(65,171,93)', 'rgb(35,139,69)','rgb(0,109,44)',
    'rgb(0,68,27)']

def first_figure():
    """Grafico de Participación - Region
    Reponde a la pregunta: ¿cómo es la participacion según región?
    """

    PARTICIPACION_REGION = "SELECT SUM(NRO_ESTUDIANTES) AS TOTAL_ESTUDIANTES, REGION\
    FROM (SELECT ESTD_COL.NRO_ESTUDIANTES, ESTD_COL.COD_COLEGIO, COL.TIPO_COL, COL.NOMBRE_COL, COL.REGION\
    FROM(SELECT COUNT(*) AS NRO_ESTUDIANTES, COD_COLEGIO\
    FROM ESTUDIANTE\
    GROUP BY COD_COLEGIO) ESTD_COL\
    LEFT JOIN COLEGIO COL ON ESTD_COL.COD_COLEGIO = COL.COD_COLEGIO)\
    GROUP BY REGION\
    ORDER BY TOTAL_ESTUDIANTES DESC"

    conn, cursor = get_db()
    cursor.execute(PARTICIPACION_REGION)
    data = cursor.fetchall()

    data_region = pd.DataFrame(data, columns=['Nro_participantes','Región'])

    fig = px.pie(data_region, values='Nro_participantes',names='Región') #color_discrete_sequence= colores)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return fig

def second_figure():
    """Grafico de Participación - Tipo de Colegio
    Reponde a la pregunta: ¿cómo es la participacion según el tipo de colegio?
    """

    PARTICIPACION_TIPO = """SELECT SUM(NRO_ESTUDIANTES) AS TOTAL_ESTUDIANTES, TIPO_COL
    FROM (SELECT ESTD_COL.NRO_ESTUDIANTES, ESTD_COL.COD_COLEGIO, COL.TIPO_COL, COL.NOMBRE_COL, COL.REGION
    FROM(SELECT COUNT(*) AS NRO_ESTUDIANTES, COD_COLEGIO
    FROM ESTUDIANTE
    GROUP BY COD_COLEGIO) ESTD_COL
    LEFT JOIN COLEGIO COL ON ESTD_COL.COD_COLEGIO = COL.COD_COLEGIO)
    GROUP BY TIPO_COL
    ORDER BY TOTAL_ESTUDIANTES DESC"""

    conn, cursor = get_db()
    cursor.execute(PARTICIPACION_TIPO)
    data = cursor.fetchall()

    data_region = pd.DataFrame(data, columns=['Nro_participantes','Tipo de Colegio'])

    fig = px.pie(data_region, values='Nro_participantes',names='Tipo de Colegio') #color_discrete_sequence= colores)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return fig

def third_figure():
    """Tabla de puntajes de mejores colegios.
    """

    MEJORES_COLEGIOS = """SELECT C.COD_CIA, C.NOMBRE_CIA, P.PUNT_ACUM, J.REGION, J.TIPO_COL, J.NOMBRE_COL
    FROM COMPAÑIA C
    LEFT JOIN PARTICIPA_EN P ON P.COD_CIA = C.COD_CIA
    LEFT JOIN (SELECT COL.REGION, COL.TIPO_COL, COL.NOMBRE_COL, E.COD_CIA
    FROM ESTUDIANTE E LEFT JOIN COLEGIO COL ON COL.COD_COLEGIO = E.COD_COLEGIO) J ON J.COD_CIA = C.COD_CIA
    ORDER BY P.PUNT_ACUM DESC"""

    conn, cursor = get_db()
    cursor.execute(MEJORES_COLEGIOS)
    data = cursor.fetchall()
    df_mc = pd.DataFrame(data, columns=['COD-CIA','NOMBRE','PUNTAJE','REGION','TIPO','NOMBRE']).drop_duplicates()

    fig = go.Figure(data=[
    go.Table(
    header = dict(values=list(df_mc.columns),
                 fill_color='paleturquoise',
                 align='left'),
    cells = dict(values=[df_mc['COD-CIA'], df_mc.NOMBRE, df_mc.PUNTAJE, df_mc.REGION,
                         df_mc.TIPO, df_mc.NOMBRE], fill_color='lavender', align='left')
    )
    ])

    return fig 


def last_figure():
    """PROMEDIO DE NOTAS POR REGION
    """

    PROMEDIO_REGION = """SELECT ROUND(AVG(PUNT_ACUM),2) AS PROMEDIO_PUNTAJES, REGION 
    FROM (SELECT C.COD_CIA, C.NOMBRE_CIA, P.PUNT_ACUM, J.REGION, J.TIPO_COL, J.NOMBRE_COL
    FROM COMPAÑIA C
    LEFT JOIN PARTICIPA_EN P ON P.COD_CIA = C.COD_CIA
    LEFT JOIN (SELECT COL.REGION, COL.TIPO_COL, COL.NOMBRE_COL, E.COD_CIA
    FROM ESTUDIANTE E LEFT JOIN COLEGIO COL ON COL.COD_COLEGIO = E.COD_COLEGIO) J ON J.COD_CIA = C.COD_CIA)
    GROUP BY REGION"""

    conn, cursor = get_db()

    cursor.execute(PROMEDIO_REGION)
    data = cursor.fetchall()
    df_pr = pd.DataFrame(data, columns=['Promedio Puntaje','Región']).sort_values('Promedio Puntaje', ascending=False)

    fig = px.bar(df_pr, x="Región", y="Promedio Puntaje")
    
    return fig