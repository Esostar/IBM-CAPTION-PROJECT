import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the automobiles data into pandas dataframe
auto_data =  pd.read_csv('automobileEDA.csv', 
                            encoding = "ISO-8859-1",
                            )

#Layout Section of Dash

app.layout = html.Div(children=[html.H1('US Domestic Airline Flights Performance.', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),

     #outer division starts
     html.Div([
                   # First inner divsion for  adding dropdown helper text for Selected Drive wheels
                    html.Div(["choose Year: ", dcc.Input(id='input-year', value='2005', 
                                type='number', style={'height':'50px', 'font-size': 35}),], 
                     ),
                    #Second Inner division for adding 2 inner divisions for 2 output graphs 

                        dcc.Dropdown(id='input-type', 
                   options=[
                           {'label': 'Yearly Airline Performance Report', 'value': 'OPT1'},
                           {'label': 'Yearly Airline Delay Report', 'value': 'OPT2'}
                           ],
                  placeholder='Select a report type',
                  style={'width': '80%', 'padding': '3px', 'font-size': 24, 'text-align-last': 'center'})
        ],
        value='OPT1'
        ),
                    #Second Inner division for adding 2 inner divisions for 2 output graphs 

                    html.Div([
                
                        html.Div([ ], id='plot4'),
                        html.Div([ ], id='plot5')

                        
                    ], style={'display': 'flex'}),

    ])
    #outer division ends

])
#layout ends

#Place to add @app.callback Decorator
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children'),
               Output(component_id='plot3', component_property='children'),
               Output(component_id='plot4', component_property='children'),
               Output(component_id='plot5', component_property='children')]
               Input(component_id='demo-dropdown', component_property='value'))

   
#Place to define the callback function .
def display_selected_drive_charts(value):
   

   
   filtered_df = auto_data[auto_data['drive-wheels']==value].groupby(['drive-wheels','body-style'],as_index=False). \
            mean()
        
   filtered_df = filtered_df
   
   fig1 = px.pie(filtered_df, values='price', names='body-style', title="Pie Chart")
   fig2 = px.bar(filtered_df, x='body-style', y='price', title='Bar Chart')
   line_fig = px.line(line_data, x='Month', y='AirTime', color='Reporting_Airline', title='Average monthly flight time')
   tree_fig = px.treemap(tree_data, path=['DestState', 'Reporting_Airline'], 
                      values='Flights',
                      color='Flights',
                      color_continuous_scale='RdBu',
                      title='Flight count by airline to destination state'
                )
    
   return [px.Graph(figure=fig1),
            px.Graph(figure=fig2),
             px.Graph(figure=line_fig),
             px.Graph(figure=tree_fig)
               ]

   
   

if __name__ == '__main__':
    app.run_server()
    