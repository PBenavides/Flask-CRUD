import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from app.dashboard.figures import first_figure, second_figure

import pandas as pd
import plotly.graph_objects as go

fig = first_figure()

fig_ = second_figure()


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
          html.H2("Colegios con compañias top 5"),
          html.P(""),
          html.Div([
            dcc.Graph(
              id="graph_one",
              figure=fig
            )
          ],className="grafico-left")
        ], className="graficaLeft"),
        html.Div([
          html.H2("Top 3 Compañias por Colegio"),
          html.P(""),
          html.Div([
            dcc.Graph(
              id="graph_two",
              figure=fig_
            )
          ], className="grafico-right")
        ], className="graficaRight")
      ], className="graficaRelative")
    ], className="graficaBlock"),

    html.Div([
      html.Div([
        html.H2("Porcentaje de participacion - Nivel Estudiantil"),
        html.P(""),
        html.Div([
          dcc.Dropdown(id="graph-control-corp",
          options=["uno","dos"],
          value="SAGA"),
          dcc.Dropdown(id='graph-control-doctype',
          options=["tres","cuatro"],
          value="NOTAS"),
    
          html.Div([
          dcc.Graph(id="sentiment_graph")
                  ])
                ], className="grafico-left2")
              ], className="graficaLeft"),
          html.Div([
        html.H2("Porcentaje de participacion - Tipo de Colegio"),
        html.Div([
          html.Div([dcc.Graph(
              id="graph_three",
              figure=fig
            )
          ])
        ],className="grafico-right")
      ],className="graficaRight")
    ], className="graficaRelative")
              ], className="graficaBlock"),
      
    
  ], className="graficas")