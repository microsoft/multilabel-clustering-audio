import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    'tsne3d256.csv')

colors = {'text':'#7FDBFF'}

app.layout = html.Div(children=[
    html.H1(children='Hello Dash',
            style={
                  'textAlign': 'center',
                  'color': colors['text']
            }),

    html.Div(children='Dash: A web application framework for Python.',
             style={'textAlign': 'center',
                    'color': colors['text']}),
    html.Div([
      html.Div([
        dcc.Graph(
            id='tsne-3d-256',
            figure={
                'data': [
                    go.Scatter3d(
                        x=df['x'],
                        y=df['y'],
                        z=df['z'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 5,
                            'color': df['color'],
                            'colorscale': 'Viridis'
                        },
                        hovertext=['cluster: ']*len(df['clusters']) + df['clusters'].astype(str),
                        hoverinfo='text'
                    )
                ],
                'layout': go.Layout(
                    margin={'l': 20, 'b': 0, 't': 0, 'r': 0},
                    hovermode='closest', width=1000, height=1000,
                    clickmode='event+select'
                )
            }
        )
      ], style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),

      html.Div(id='imgdiv',[html.Img(id='img'), html.Audio(id='audio')], style={'width': '49%', 'display': 'inline-block', 'padding': '0 40'})
    ])
])


'''def display_image(dff, axis_type, title):
    return {
        img_filename = random.choice(os.listdir("C:\\Users\\t-anmend\\Documents\\interface\\src\\assets"))

        app.layout = html.Div([html.Img(id='img', src=img_filename)])
    }
'''

def highlight():
    def callback(*clickDatas):
        clickData = clickDatas[0]
        #print(clickData)

        if clickData is not None:
            point_text = clickData['points'][0]['hovertext'][9:]

            #pt = set([int(x) for x in point_text[point_text.find("{")+1:point_text.find("}")].split(', ')])

            #print(pt)
            #print(type(df['clusters'][0]))
            #print(df.loc[df['clusters'] == point_text])
            selectedpoints = df.loc[df['clusters'] == point_text]
            unselected = df.loc[df['clusters'] != point_text]
            figure = {
            'data': [
                    go.Scatter3d(
                        x=selectedpoints['x'],
                        y=selectedpoints['y'],
                        z=selectedpoints['z'],
                        mode='markers',
                        marker={
                                'opacity': 0.8,
                                'size': 5,
                                'color': selectedpoints['color'],
                                'colorscale': 'Viridis'
                                },
                        #selected={
                            #'marker':{
                                #'opacity': 0.8,
                                #'size': 5,
                                #'color': df['color'],
                                #'colorscale': 'Viridis'

                            #}
                            
                        #},
                        #unselected={
                            #'marker':{
                                #'opacity': 0.3
                            #}
                        #},
                        hovertext=['cluster: ']*len(selectedpoints['clusters']) + selectedpoints['clusters'].astype(str),
                        hoverinfo='text',
                        #selectedpoints=selectedpoints
                    ),
                    go.Scatter3d(
                        x=unselected['x'],
                        y=unselected['y'],
                        z=unselected['z'],
                        mode='markers',
                        marker={
                                'opacity': 0.2,
                                'size': 5,
                                'color': unselected['color'],
                                'colorscale': 'Viridis'
                                },
                        #selected={
                            #'marker':{
                                #'opacity': 0.8,
                                #'size': 5,
                                #'color': df['color'],
                                #'colorscale': 'Viridis'

                            #}
                            
                        #},
                        #unselected={
                            #'marker':{
                                #'opacity': 0.3
                            #}
                        #},
                        hovertext=['cluster: ']*len(unselected['clusters']) + unselected['clusters'].astype(str),
                        hoverinfo='text',
                        #selectedpoints=selectedpoints
                    )

                ],
                'layout': go.Layout(
                    margin={'l': 20, 'b': 0, 't': 0, 'r': 0},
                    hovermode='closest', width=1000, height=1000,
                    clickmode='event+select',
                )
            }

            html.Div([html.Img(id='img', src='/assets/flower.jpg'), html.Audio(id='audio', src='/assets/00_001449.wav', controls=True)], style={'width': '49%', 'display': 'inline-block', 'padding': '0 40'})

        else:
            
            figure = {
                'data': [
                    go.Scatter3d(
                                x=df['x'],
                                y=df['y'],
                                z=df['z'],
                                mode='markers',
                                marker={
                                        'opacity': 0.8,
                                        'size': 5,
                                        'color': df['color'],
                                        'colorscale': 'Viridis'
                                        },
                                #selected={
                                    #'marker':{
                                        #'opacity': 0.8,
                                        #'size': 5,
                                        #'color': df['color'],
                                        #'colorscale': 'Viridis'

                                    #}
                                    
                                #},
                                #unselected={
                                    #'marker':{
                                        #'opacity': 0.3
                                    #}
                                #},
                                hovertext=['cluster: ']*len(df['clusters']) + df['clusters'].astype(str),
                                hoverinfo='text',
                                #selectedpoints=selectedpoints
                        )
                ],

                'layout': go.Layout(
                        margin={'l': 20, 'b': 0, 't': 0, 'r': 0},
                        hovermode='closest', width=1000, height=1000,
                        clickmode='event+select',
                )
            }
        # set which points are selected with the `selectedpoints` property
        # and style those points with the `selected` and `unselected`
        # attribute. see
        # https://medium.com/@plotlygraphs/notes-from-the-latest-plotly-js-release-b035a5b43e21
        # for an explanation

        return figure

    return callback




app.callback(
    Output('tsne-3d-256', 'figure'),
    [Input('tsne-3d-256', 'clickData')]
)(highlight())


if __name__ == '__main__':
    app.run_server(debug=True)