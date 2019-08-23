import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import json
import numpy as np
from sklearn.externals import joblib
from uuid import uuid4
from datetime import datetime

userid = uuid4()

df = pd.read_csv(
    'tsne3d256.csv')
with open('label_order.pkl','rb') as f:
    options = joblib.load(f)
option_dict = []

options = options[8:]

for option in options:
    option_dict.append({'label':option.split('_')[1], 'value':option})

option_dict.append({'label':'Other','value':'9_other'})

suggest_dict = []

for i in range(len(df['clusters'])):
    if len(df.loc[df['clusters'] == df['clusters'][i]]) < 10 and df.loc[df['clusters'] == df['clusters'][i]].index[0] == i:
        suggest_dict.append({'label':'Review samples in clusters: ' + df.loc[df['clusters'] == df['clusters'][i]]['clusters'].reset_index(drop=True)[0], 'value':df.loc[df['clusters'] == df['clusters'][i]]['clusters'].reset_index(drop=True)[0]})

colors = {'text':'#7026A5'}

def Card(children, **kwargs):
    return html.Section(children, className="card-style")

def create_layout(app):

    return html.Div(children=[
                        html.H1(children='Audio Annotator',
                                style={
                                      'textAlign': 'center',
                                      'color': colors['text']
                                }),

                        html.Div(children='An application for cluster identification in multi-label data.',
                                 style={'textAlign': 'center',
                                        'color': colors['text']}),
                        html.Div([
                          html.Div([dcc.Dropdown(id='test_drop', options=suggest_dict, multi=False)],
                            style={'width':'50%'}),
                          html.Div(id='print-drop', children=dcc.Input(id='print-input', style={'display':'none'})),
                          html.Div([
                            dcc.Graph(
                                id='tsne-3d-256',
                                style={'width': '100%', 'float': 'left', 'display': 'inline-block', 'margin-left':-40, 'margin-top':20}
                            )
                          ],className='six columns',style={'display':'inline-block'}),
                          html.Div(id='dummy_div',children='DUMMY',style={'display':'none'}),

                          html.Div(id='filenames',style={'display':'none'}),
                          html.Div(id='dummy_options',style={'display':'none'}),

                          html.Div(
                            html.Div(
                                id='imgdiv',
                                children=[Card(children=
                                    [html.Div(id='img0'), html.Div(id='audio0'), html.Div(id='options0', children=dcc.Dropdown(id='options_0', style={'display':'none'})),html.Div(id='input0', children=dcc.Input(id='input_0',style={'display':'none'})),
                                     html.Div(id='img1'), html.Div(id='audio1'), html.Div(id='options1', children=dcc.Dropdown(id='options_1', style={'display':'none'})),html.Div(id='input1', children=dcc.Input(id='input_1',style={'display':'none'})),
                                     html.Div(id='img2'), html.Div(id='audio2'), html.Div(id='options2', children=dcc.Dropdown(id='options_2', style={'display':'none'})),html.Div(id='input2', children=dcc.Input(id='input_2',style={'display':'none'})),
                                     html.Div(id='img3'), html.Div(id='audio3'), html.Div(id='options3', children=dcc.Dropdown(id='options_3', style={'display':'none'})),html.Div(id='input3', children=dcc.Input(id='input_3',style={'display':'none'})),
                                     html.Div(id='img4'), html.Div(id='audio4'), html.Div(id='options4', children=dcc.Dropdown(id='options_4', style={'display':'none'})),html.Div(id='input4', children=dcc.Input(id='input_4',style={'display':'none'})),
                                     html.Div(id='img5'), html.Div(id='audio5'), html.Div(id='options5', children=dcc.Dropdown(id='options_5', style={'display':'none'})),html.Div(id='input5', children=dcc.Input(id='input_5',style={'display':'none'})),
                                     html.Div(id='img6'), html.Div(id='audio6'), html.Div(id='options6', children=dcc.Dropdown(id='options_6', style={'display':'none'})),html.Div(id='input6', children=dcc.Input(id='input_6',style={'display':'none'})),
                                     html.Div(id='img7'), html.Div(id='audio7'), html.Div(id='options7', children=dcc.Dropdown(id='options_7', style={'display':'none'})),html.Div(id='input7', children=dcc.Input(id='input_7',style={'display':'none'})),
                                     html.Div(id='img8'), html.Div(id='audio8'), html.Div(id='options8', children=dcc.Dropdown(id='options_8', style={'display':'none'})),html.Div(id='input8', children=dcc.Input(id='input_8',style={'display':'none'})),
                                     html.Div(id='img9'), html.Div(id='audio9'), html.Div(id='options9', children=dcc.Dropdown(id='options_9', style={'display':'none'})),html.Div(id='input9', children=dcc.Input(id='input_9',style={'display':'none'}))], 
                                    style={'width': '100%', 'float': 'left', 'display': 'inline-block'})], 
                                className='five columns'),
                            ),
                            html.Div(id='buttn',children=html.Button('Submit',id='submit_btn',type='submit',style={'display':'none'}),className='one column'),

                          
                        ])
                    ])


def demo_callbacks(app):

    @app.callback( 
        Output('tsne-3d-256', 'figure'),
        [Input('tsne-3d-256', 'clickData'),
         Input('dummy_div','children'),
         Input('test_drop','value')])
    def generate_figure(*clickDatas):
        clickData = clickDatas[0]
        dummy_div = clickDatas[1]

        ctx = dash.callback_context
        if ctx.triggered:
            trig = ctx.triggered[0]['prop_id'].split('.')[1]

            if trig == 'clickData':
                clickData = clickDatas[0]
                if clickData is not None:
                    point_text = clickData['points'][0]['hovertext'][9:]
            else:
                clickData = clickDatas[2]
                point_text = clickData
        
        axes = dict(title="", showgrid=True, zeroline=False, showticklabels=False)

        if clickData is not None:

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
                        hovertext=['cluster: ']*len(selectedpoints['clusters']) + selectedpoints['clusters'].astype(str),
                        hoverinfo='text',
                        showlegend=False
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
                        
                        hovertext=['cluster: ']*len(unselected['clusters']) + unselected['clusters'].astype(str),
                        hoverinfo='text',
                        showlegend=False
                    )

                ],
                'layout': go.Layout(
                    margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
                    hovermode='closest',
                    autosize=True,
                    clickmode='event+select',
                    uirevision=dummy_div,
                    scene={
                        'xaxis': axes,
                        'yaxis': axes,
                        'zaxis': axes

                    }, 
                )
            }

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
                                hovertext=['cluster: ']*len(df['clusters']) + df['clusters'].astype(str),
                                hoverinfo='text',
                        )
                ],

                'layout': go.Layout(
                        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
                        hovermode='closest', #width='100%', height='100%',
                        clickmode='event+select',
                        autosize=True,
                        uirevision=dummy_div,
                        scene={
                            'xaxis': axes,
                            'yaxis': axes,
                            'zaxis': axes

                    }
                )
            }

        return figure
    
    @app.callback(
        [Output('imgdiv', 'children'),
         Output('buttn','children'),
         Output('filenames','children')],
        [Input('tsne-3d-256', 'clickData'),
         Input('test_drop','value')])
    def display_images(*clickDatas):
        clickData = clickDatas[0]
        ctx = dash.callback_context
        if ctx.triggered:
            trig = ctx.triggered[0]['prop_id'].split('.')[1]

            if trig == 'clickData':
                clickData = clickDatas[0]
                if clickData is not None:
                    point_text = clickData['points'][0]['hovertext'][9:]
            else:
                clickData = clickDatas[1]
                point_text = clickData
        if clickData is not None:
            #point_text = clickData['points'][0]['hovertext'][9:]
            print(trig)
            paths = df.loc[df['clusters'] == point_text, ['files']].values
            path_list = [paths[i][0] for i in range(len(paths))]

            imgs_paths = [os.path.splitext(path_list[i])[0] + '.jpg' for i in range(len(path_list))]

            if len(imgs_paths) < 11:
                num_files = len(imgs_paths)
            else:
                num_files = 10

            files = np.random.choice(imgs_paths, num_files, replace=False)

            filenames = [os.path.splitext(files[i])[0] for i in range(len(files))]

            card = []
            for i in range(len(filenames)):

                audio = filenames[i] + '.wav'
                image = filenames[i] + '.jpg'

                card.append(Card([html.Img(src='/assets/SONYC/images/train/' + image, style={
                'display':'inline-block',
                'height': '100%',
                'width': '100%', 'margin-top':10
            }), html.Audio(src='/assets/SONYC/train/' + audio, controls=True, style={'display':'inline-block', 'vertical-align':'top','margin-left':10, 'margin-bottom':5}), 
                dcc.Dropdown(id='options_'+str(i), options=option_dict,style={'margin-bottom':5},
                    multi=True,placeholder='Select all that apply'), dcc.Input(id='input_'+str(i),style={'display':'none'})]))
            
            if len(filenames) < 10:
                for i in range(len(filenames),10):
                    card.append(Card([html.Img(style={
                'display':'none'}), html.Audio(style={'display':'none'}), 
                dcc.Dropdown(id='options_'+str(i), options=option_dict,style={'display':'none'}), dcc.Input(id='input_'+str(i),style={'display':'none'})]))



            return card, html.Button('Submit',id='submit_btn',type='submit', style={'display':'inline-block', 'vertical-align':'bottom', 'float':'left', 'margin-left':-40, 'margin-top':10}), json.dumps(filenames)
        else:
            card = []
            for i in range(10):

                card.append(Card([html.Img(id='img'+str(i), style={
                'display':'none'}), html.Audio(id='audio'+str(i),style={'display':'none'}), 
                dcc.Dropdown(id='options_'+str(i), options=option_dict,style={
                    'display': 'none'}), dcc.Input(id='input_'+str(i),style={'display':'none'})]))
            return card, None, None

    @app.callback(Output('input_0','style'),
        [Input('options_0', 'value')])

    def show_input_0(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_1','style'),
        [Input('options_1', 'value')])

    def show_input_1(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_2','style'),
        [Input('options_2', 'value')])

    def show_input_2(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_3','style'),
        [Input('options_3', 'value')])

    def show_input_3(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_4','style'),
        [Input('options_4', 'value')])

    def show_input_4(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_5','style'),
        [Input('options_5', 'value')])

    def show_input_5(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_6','style'),
        [Input('options_6', 'value')])

    def show_input_6(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_7','style'),
        [Input('options_7', 'value')])

    def show_input_7(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_8','style'),
        [Input('options_8', 'value')])

    def show_input_8(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback(Output('input_9','style'),
        [Input('options_9', 'value')])

    def show_input_9(options):
        if options is not None:
            if '9_other' in options:
                return {'display':'inline-block'}
        
        return {'display':'none'}

    @app.callback([Output('dummy_options','children'),
         Output('options_0', 'disabled'),
         Output('options_1', 'disabled'),
         Output('options_2', 'disabled'),
         Output('options_3', 'disabled'),
         Output('options_4', 'disabled'),
         Output('options_5', 'disabled'),
         Output('options_6', 'disabled'),
         Output('options_7', 'disabled'),
         Output('options_8', 'disabled'),
         Output('options_9', 'disabled'),
         Output('input_0', 'disabled'),
         Output('input_1', 'disabled'),
         Output('input_2', 'disabled'),
         Output('input_3', 'disabled'),
         Output('input_4', 'disabled'),
         Output('input_5', 'disabled'),
         Output('input_6', 'disabled'),
         Output('input_7', 'disabled'),
         Output('input_8', 'disabled'),
         Output('input_9', 'disabled')],
        [Input('submit_btn','n_clicks')],
        [State('options_0','value'),
         State('options_1','value'),
         State('options_2','value'),
         State('options_3','value'),
         State('options_4','value'),
         State('options_5','value'),
         State('options_6','value'),
         State('options_7','value'),
         State('options_8','value'),
         State('options_9','value'),
         State('input_0','value'),
         State('input_1','value'),
         State('input_2','value'),
         State('input_3','value'),
         State('input_4','value'),
         State('input_5','value'),
         State('input_6','value'),
         State('input_7','value'),
         State('input_8','value'),
         State('input_9','value'),
         State('filenames','children')])

    def show_values(btn_click, options_0, options_1, options_2, options_3, options_4, options_5, options_6, options_7, options_8, options_9, 
        input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,*files):
            filenames = files[0]
            data_options = [options_0, options_1, options_2, options_3, options_4, options_5, options_6, options_7, options_8, options_9]
            inputs = [input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9]
            print(btn_click)
            data = []
            print(filenames)
            print(data_options)

            card = []
            dcc_drop = []

            if filenames is not None:
                filenames = json.loads(files[0])
                for i in range(len(filenames)):
                    if data_options[i] is not None:
                        today = datetime.today()

                        t = today.strftime("%Y%m%d_%H%M%S")
                        data.append([userid, filenames[i], data_options[i], inputs[i], t])
                        dcc_drop.append(True)
                    else:
                        dcc_drop.append(False)
                if len(filenames) < 10:
                    for i in range(len(filenames), 10):
                        dcc_drop.append(False)
                dataframe = pd.DataFrame(data, columns=['userid','file_id', 'annotations','new_categories', 'timestamp'])

                if os.path.exists('annotations.csv'):
                    with open('annotations.csv', 'a', newline='\n') as f:
                        dataframe.to_csv(f, header=False, index=False)
                else:
                    with open('annotations.csv', 'w', newline='\n') as f:
                        dataframe.to_csv(f, index=False)

                return (json.dumps(options_0), dcc_drop[0], dcc_drop[1], dcc_drop[2], dcc_drop[3], dcc_drop[4], dcc_drop[5], dcc_drop[6], dcc_drop[7], 
                       dcc_drop[8], dcc_drop[9], dcc_drop[0], dcc_drop[1], dcc_drop[2], dcc_drop[3], dcc_drop[4], dcc_drop[5], dcc_drop[6], dcc_drop[7], 
                       dcc_drop[8], dcc_drop[9])
            else:
                return json.dumps(options_0), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None


'''
    @app.callback(
        Output('numclusters', 'value'),
        Input('numclusters', 'value'))

    def show_dropdowns():'''