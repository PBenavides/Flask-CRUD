import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




def first_figure():
    """Top 3 Compañías por Colegio
    """
    df = pd.DataFrame({
     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    #Defino las figuras para luego llamarlas en el div.
    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    return fig

def second_figure():
    """
    
    """
    df_ = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_.Rank, df_.State, df_.Postal, df_.Population],
                fill_color='lavender',
                align='left'))
    ])

    return fig