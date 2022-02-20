import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import json
from bs4 import BeautifulSoup as bs
import requests
import os.path as path


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],  #LUX
                # meta_tags=[{'name': 'viewport',
                #            'content': 'width=device-width, initial-scale=1.0'}]
                )
'''
def take_xcom_id(**context):
    last_cme_id = context['task_instance'].xcom_pull(
        key='last_cme_activity', value=last_cme

    return last_cme_id
last_cme_id = take_xcom_id()
print(f'AQUIIIIIIIIIIII-----##################{last_cme_id}')
'''
'''
def new_event_xcom(**context):
    new_event_bool = context['task_instance'].xcom_pull(
        key='new_cme_boolean', value=new_event
    )
'''
#last_cme_id = take_xcom_id()
# new_event_bool = new_event_xcom()
with open('/home/javier/repos/Coronal_Mass_Ejection_Alert_System/new_event.json', "r") as file:
    new_event_json = json.load(file)

# Last Event
#last_cme_path = 'last_100_events/2021-10-28T01:23:00-CME-001.json'  # Xcom
# last_cme_path = f'last_100_events/{}.json'
#last_cme_path = path.abspath(path.join('dashapp.py', "../last_100_events/{}.json".format('2021-10-28T01:23:00-CME-001')))
#last_cme_path = '/home/javier/repos/Coronal_Mass_Ejection_Alert_System/last_100_events/{}.json'.format('2021-10-28T01:23:00-CME-001')
#with open(last_cme_path, "r") as file:
#    last_cme = json.load(file)

# Is a new event?
new_event_bool = [True if new_event_json['new_event'] == 'yes' else False][0]
print(new_event_bool)
last_activityID = new_event_json['activityID']

last_cme_path = '/home/javier/repos/Coronal_Mass_Ejection_Alert_System/last_100_events/{}.json'.format(last_activityID)
with open(last_cme_path, "r") as file:
    last_cme = json.load(file)


# new_event = False
def alert(new_event):
    if new_event:
        message = f"NEW ACTIVITY DETECTED!! {last_cme['activityID']}"
        color = 'danger'
    else:
        message = f"Last Event Detected {last_cme['activityID']}"
        color = 'info'
    return message, color


message, color = alert(new_event=new_event_bool)

try:
    # gif
    cme_link_gif = last_cme['cmeAnalyses'][0]['enlilList'][0]['link']
    soup = bs(requests.get(cme_link_gif).content, 'html.parser')
    # List of gifs
    gifs_list = []
    for a in soup.find_all('a'):
        if 'gif' in a.get('href'):
            gifs_list.append(a.get('href'))
    # Last CME gif
    last_cme_gif = gifs_list[0]
except:
    print('NO GIF')
    gifs_list = ['No gif', 'No gif']

try:
    note = last_cme['note']
except:
    note = 'No note available'
try:
    estimated_earth_impact = last_cme['cmeAnalyses'][0]['enlilList'][0]['estimatedShockArrivalTime']
except:
    estimated_earth_impact = 'No estimated earth impact available'
try:
    speed = last_cme['cmeAnalyses'][0]['speed']
except:
    speed = 'No speed available'
try:
    type = last_cme['cmeAnalyses'][0]['type']
except:
    type = 'No type available'
try:
    link_analysis = last_cme['cmeAnalyses'][0]['link']
except:
    link_analysis = 'No link available'
try:
    link_model_outputs = last_cme['cmeAnalyses'][0]['enlilList'][0]['link']
except:
    link_model_outputs = 'No link available'


# Layout section: Boostrap
# ------------------------------------------------------------------
app.layout = dbc.Container(
    className="",
    children=[
        dbc.Row(
            className="",
            children=[
                dbc.Col(html.H1("",
                                className='pt-4 text-center',
                                style={'color': 'rgb(132,11,11)'}
                                ),
                        width=12,
                        ),
            ],
            style={"height": "5vh", "backgroundColor": "#100508"}
        ),
        dbc.Row(
            className="",
            children=[
                dbc.Col(
                    children=[

                        dbc.Row(
                            children=[
                                html.H2("Coronal Mass Ejection CME",
                                        className='pt-4 text-center',
                                        style={'color': 'rgb(132,11,11)'}
                                        ),
                                dcc.Markdown(
                                    children=['''
                                        Coronal Mass Ejections (CMEs) are large expulsions of plasma and 
                                        magnetic field from the Sun’s corona. They can eject billions of tons 
                                        of coronal material and carry an embedded magnetic field (frozen in flux) 
                                        that is stronger than the background solar wind interplanetary 
                                        magnetic field (IMF) strength. CMEs travel outward from the Sun at 
                                        speeds ranging from slower than 250 kilometers per second (km/s) to as fast 
                                        as near 3000 km/s. The fastest Earth-directed CMEs can reach our planet in 
                                        as little as 15-18 hours. Slower CMEs can take several days to arrive. 
                                    '''],
                                    style={'color': '#B6DDF6'},
                                    className='pb-1',
                                ),
                                dcc.Link(
                                    'National Oceanic and Atmospheric Administration',
                                    href='https://www.swpc.noaa.gov/phenomena/coronal-mass-ejections',
                                    className="text-center",
                                    style={"backgroundColor": "#100508", 'color': '#77C6FB'},
                                    refresh=True,
                                ),
                            ],
                            style={"height": "30vh", "backgroundColor": "#100508"}
                        ),

                        dbc.Row(
                            children=[
                            ],
                            style={"height": "20vh", "backgroundColor": "#100508"}
                        ),

                        dbc.Row(
                            children=[
                                html.Img(
                                    src='https://i0.wp.com/eos.org/wp-content/uploads/2017/09/Earth_to_Scale_short_500.gif?resize=500%2C500&ssl=1',
                                    alt='NO GIF AVAILABLE',
                                    style={"height": "35vh"}
                                    #   className='ml-5'
                                ),
                                dcc.Link(
                                    'LinkedIn',
                                    href='https://www.linkedin.com/in/javier-casta%C3%B1o-candela-b89039208/',
                                    className="text-center",
                                    style={"backgroundColor": "#100508", 'color': '#77C6FB'},
                                    refresh=True,
                                ),
                            ],
                            style={"height": "40vh", "backgroundColor": "#100508"}
                        ),
                    ],

                    width=3,
                    style={'backgroundColor': 'black'}
                ),

                dbc.Col(
                    children=[
                        html.H3(
                            "Coronal Mass Ejection  Alert System",
                            className='pt-4 text-center',
                            style={'color': 'rgb(132,11,11)'}
                        ),
                        dbc.Alert(
                            id='alert',
                            children=message,   # "NEW ACTIVITY DETECTED!!!!",
                            color=color,   # "danger",
                            className='text-center',
                        ),
             #           html.Div(
              #              id="placeholder",
               #             style={"display": "none"}
                #        ),
                        html.Audio(
                            id='audio',
                            key='audiokey',
                            src='assets/alert.mp3',
                            muted=False,
                            autoPlay=new_event_bool,   #new_event,
                        #    controls=True,
                            loop='loop',
                        #    preload='auto',
                           # Sound from Zapsplat.com (credit)
                        ),
                        dcc.Markdown(
                            children=[
                                f'''
                                #### Activity ID
                                {last_cme['activityID']}
                                '''
                            ],
                            className='pt-2',
                        ),
                        dcc.Markdown(
                            children=[
                                f'''
                                #### Note
                                {note}
                                '''
                            ],
                            className='pt-2',
                        ),
                        dcc.Markdown(
                            children=[
                                f'''
                                #### Estimated Earth Impact
                                {estimated_earth_impact}
                                '''
                            ],
                            className='pt-2',
                        ),
                        dcc.Markdown(
                            children=[
                                f'''
                                #### Speed
                                {speed} km/s
                                '''
                            ],
                            className='pt-2',
                        ),
                        dcc.Markdown(
                            children=[
                                f'''
                                #### Type
                                {type}
                                '''
                            ],
                            className='pt-2',
                        ),
                        dcc.Markdown(
                            children=[
                                f'''
                                #### Link to Analysis
                                {link_analysis}
                                '''
                            ],
                            className='pt-2',
                        ),
                        dcc.Markdown(
                            children=[
                                f'''
                                #### Link to Model Outputs
                                {link_model_outputs}
                                '''
                            ],
                            className='pt-2',
                        ),
                    ],

                    width=5
                ),
                dbc.Col(
                    children=[
                        html.Img(
                            src=gifs_list[0],
                            alt='NO GIF AVAILABLE',
                            style={"height": "40vh"},
                            className='pt-5'
                        ),

                        html.Img(
                            src=gifs_list[1],
                            alt='NO GIF AVAILABLE',
                            style={"height": "40vh"},
                            className='pt-5'
                        ),
                    ],

                    width=4),
            ],
            style={"height": "90vh", "backgroundColor": "white"}
        ),
        dbc.Row(
            className="",
            children=[
                dbc.Col(
                    width=12,
                    ),
            ],
            style={"height": "5vh", "backgroundColor": "#100508"}
        )
    ],
    fluid=True,
    style={"height": "100vh",
           "background-color": "#03182D"}
)
'''
@app.callback(
    Output(component_id='audio', component_property='autoPlay'),
    Input(component_id='alert', component_property='color'))
def play(color):
    if color == 'danger':
        return True
    else:
        return False
'''

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
