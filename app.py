######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'NBA!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/blob/master/data/NBA_players_2015.csv'
githublink = 'https://github.com/farkasdilemma/304-titanic-dropdown/blob/main/app.py'


###### Import a dataframe #######
df = pd.read_csv("https://raw.git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/master/data/NBA_players_2015.csv?token=AAAKJEDTOCI6NUD6ZELUHK3CIPLCE")
#df['Female']=df['Sex'].map({'male':0, 'female':1})
#df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
variables_list=list(df['bref_team_id'].unique())

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose an NBA team to see their top players by points in 2015:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(team_var):
    
    top_players = df.sort_values(['bref_team_id','pts'],ascending = False).groupby('bref_team_id')[['player','bref_team_id','PER','VORP','WS']].head(3)
    x_names = list(top_players[top_players['bref_team_id']==team_var]['player'])

    #results=pd.DataFrame(top_players)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=x_names,
        y=top_players[top_players['bref_team_id']==team_var]['PER'],
        name='PER',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=x_names,
        y=top_players[top_players['bref_team_id']==team_var]['WS'],
        name='Win Shares',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=x_names,
        y=top_players[top_players['bref_team_id']==team_var]['VORP'],
        name='Value Over Replacement Player',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Players'), # x-axis label
        yaxis = dict(title = str(team_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
