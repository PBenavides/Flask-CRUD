from dash import dcc
from dash import html
import plotly.express as px

from app.dashboard.figures import first_figure, second_figure, third_figure, last_figure

import pandas as pd
import plotly.graph_objects as go

fig = first_figure()

fig_2 = second_figure()

fig_3 = third_figure()

fig_4 = last_figure()

layout =  html.Div([      #Banner
  html.Div([
  html.Div([
    html.P("Junior Achievement Peru")
    ], className="nombreApp"),
  html.Div([
    html.Img(src="http://jawperu.org/wp-content/themes/twentytwelve-child/images/logo_ja_peru.jpg", alt="logo")
  ], className="logoJA")
  ], className="header"),

  #--------------------------------Contenedor de los 4 dash--------------------------------
  html.Div([
    html.Div([
      html.Div([

        html.Div([
          html.H2("Participación de Colegios por Región"),
          html.P(""),
          html.Div([
            dcc.Graph(
              id="graph_one",
              figure=fig
            )
          ],className="grafico-left")
        ], className="graficaLeft"),
        html.Div([
          html.H2("Rendimiento de Colegios por Región"),
          html.P(""),
          html.Div([
            dcc.Graph(
              id="graph_two",
              figure=fig_4
            )
          ], className="grafico-right")
        ], className="graficaRight")
      ], className="graficaRelative")
    ], className="graficaBlock"),

    html.Div([
      html.Div([
        html.H2("Tabla de Rendimiento de Colegios"),
        html.P(""),
        html.Div([
          html.Div([dcc.Graph(
              id="graph_three",
              figure=fig_3
            )
                  ])
                ], className="grafico-left2")
              ], className="graficaLeft"),
          html.Div([
        html.H2("Porcentaje de participacion - Tipo de Colegio"),
        html.Div([
          html.Div([dcc.Graph(
              id="graph_four",
              figure=fig_2
            )
          ])
        ],className="grafico-right")
      ],className="graficaRight")
    ], className="graficaRelative")
              ], className="graficaBlock"),
      
    
  ], className="graficas")