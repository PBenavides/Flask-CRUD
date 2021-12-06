import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd

#Acá debería jalar mis datos para el reporte.
df = pd.DataFrame({
     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

layout =  html.Div([#Banner
  html.Div([
  html.Div([
    html.P("Junior Achievement Peru")
    ], className="nombreApp"),
  html.Div([
    html.Img(src="http://jawperu.org/wp-content/themes/twentytwelve-child/images/logo_ja_peru.jpg", alt="logo")
  ], className="logoBBVA")
  ], className="header"),

  #Contenedor de los 4 dash

  html.Div([
    html.Div([
      html.Div([

        html.Div([
          html.H2("Porcentaje de participantes por grado"),
          html.P(""),
          html.Div([
            dcc.Graph(
              id="graph_one",
              figure=fig
            )
          ],className="grafico-left")
        ], className="graficaLeft"),
        html.Div([
          html.H2("Numero de compañias por zona geografica"),
          html.P(""),
          html.Div([
            dcc.Graph(
              id="graph_two",
              figure=fig
            )
          ], className="grafico-right")
        ], className="graficaRight")
      ], className="graficaRelative")
    ], className="graficaBlock"),

    html.Div([
      html.Div([
        html.H2("Otro gato"),
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
              ], className="graficaLeft")
              ], className="graficaBlock"),
      html.Div([
        html.Div([
          html.Div([

          ])
        ],className="grafico-right")
      ],className="graficaRight")
    ], className="graficaRelative")
    
  ], className="graficas")