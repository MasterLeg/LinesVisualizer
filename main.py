import logging
import sys

# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from plotly import subplots

# Project internal imports
from utils.hours import Hours
from databases.datagate import DataGate


class WebApp:

    def __init__(self, line, scope):
        # External CSS
        external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

        colors = {
            'background': 'rgb(20, 22, 25)',
            'text': 'rgb(210, 210, 210)',
            'grids': 'rgb(180, 180, 180)',
            'success': 'rgb(101, 180, 85)',
            'warning': 'rgb(255, 201, 14)',
            'danger': 'rgb(255, 11, 11)',
        }

        # Dash board layout
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.title = 'Lines Visualizer'

        # HTML Layout
        self.app.layout = html.Div(style={'backgroundColor': colors['background'], 'height': '100vh'}, children=[
            html.Div([
                dcc.Graph(id='live-update-graph', style={'height': 900}),
                dcc.Interval(
                    id='interval-component',
                    interval=2 * 1000,  # 2 seconds (in miliseconds)
                    n_intervals=0
                )
            ])
        ])

        # Method to update the figure
        @self.app.callback(Output(component_id='live-update-graph', component_property='figure'),
                           Input(component_id='interval-component', component_property='n_intervals'))
        def update_graph_live(n):
            # Create DataBase objects
            databases = DataGate().databases
            objectives = {'SSL1': {'Started': 25,
                                   'Finished': 31},
                          'SSL3': {'Started': 25,
                                   'Finished': 31}}
            database = databases[line][kind]

            # Get the hours in whole datetime format
            hours = Hours()
            current_timestamp = database.get_current_timestamp()
            last_hour = hours.last_hour(current_timestamp)
            current_hour = hours.current_hour(current_timestamp)
            next_hour = hours.next_hour(current_timestamp)

            now_unix = hours.now_unix()
            dates_unix_list = hours.get_unix_dates_list()

            dates_list = hours.get_datetime_hours_list(15)

            # Get manufactured cartridges
            previous_cartridges = database.get_cartridges_between_datetimes(last_hour, current_hour)
            current_cartridges = database.get_cartridges_between_datetimes(current_hour, next_hour)
            finished_cartridges_by_hour = database.get_split_hour_cartridges(now_unix, dates_unix_list)
            last_cartridge_date = database.get_last_cartridge_date()

            # Line speed indicator
            time_since_last_cartridge = int((current_timestamp - last_cartridge_date).total_seconds())

            specs = {
                'Started': [[{"colspan": 2}, None], [{"colspan": 2}, None]],
                'Finished': [[{"colspan": 2}, None], [{}, {}]]
            }

            # Create the figure with subplots
            fig = subplots.make_subplots(rows=2, cols=2,
                                         specs=specs[scope],
                                         vertical_spacing=0.2,
                                         subplot_titles=(f"{line} - {scope} Cartridges per Hour",
                                                         f"{line} - Line Speed",
                                                         f"{line} - Hours Comparison"))

            # Create the Cartridges every 15 minutes last 24 hours
            fig.add_trace({'name': 'Line Rhythm',
                           'type': 'scatter',
                           'x': dates_list,
                           'y': finished_cartridges_by_hour,
                           'mode': 'lines+markers',
                           'marker': dict(color=colors['success']),
                           'fill': 'tozeroy'
                           },
                          row=1,
                          col=1
                          )

            # Add the objective line
            fig.add_trace({'x': dates_list,
                           'y': [objectives[line][scope]] * len(finished_cartridges_by_hour),
                           'type': 'scatter',
                           'mode': 'lines',
                           'name': 'Line Rhythm',
                           'marker': dict(color=colors['warning']),
                           },
                          row=1,
                          col=1
                          )

            fig.add_trace({'type': 'bar',
                           'name': 'Line Rhythm',
                           'x': [time_since_last_cartridge],
                           'y': ['Last '],
                           'text': [time_since_last_cartridge],
                           'textposition': 'auto',
                           'orientation': 'h',
                           'marker': dict(color=colors['success']),
                           },
                          row=2,
                          col=1
                          )

            # Comparison last hour and current hour
            if scope == 'Finished':
                fig.add_trace({'x': [f'{str(last_hour.hour)}:00h - {str(current_hour.hour)}:00h',
                                     f'{str(current_hour.hour)}:00h - {str(next_hour.hour)}:00h'],
                               'y': [previous_cartridges, current_cartridges],
                               'text': [previous_cartridges, current_cartridges],
                               'textposition': 'auto',
                               'type': 'bar',
                               'marker_color': ['rgb(90, 133, 86)', colors['success']]
                               },
                              row=2,
                              col=2
                              )

            fig.layout.plot_bgcolor = colors['background']
            fig.layout.paper_bgcolor = 'black'

            # Set grids properties
            fig.update_xaxes(linewidth=2, linecolor=colors['grids'], gridwidth=1, gridcolor=colors['grids'])
            fig.update_yaxes(gridwidth=1, gridcolor=colors['grids'], zerolinewidth=1, zerolinecolor=colors['grids'])

            # Change the layout for the Line Speed subplot
            speed_position = dict(row=2, col=1)

            # Set the axis titles
            fig.update_yaxes(title='Cartridges', row=1, col=1)
            fig.update_xaxes(title='Time (s)', row=2, col=1)
            fig.update_yaxes(title='Cartridges', row=2, col=2)

            # Disabling the grids
            fig.update_yaxes(showgrid=False, row=2, col=1)
            fig.update_xaxes(showgrid=False, row=2, col=2)

            # Set axis sizes
            fig.update_yaxes(range=[0, 50], row=1, col=1)
            fig.update_xaxes(range=[0, 150], row=2, col=1)
            fig.update_yaxes(range=[0, 150], row=2, col=2)

            # Line Speed: Change the bar plot color according to the line speed value
            if time_since_last_cartridge < 35:
                fig.update_traces(marker_color=colors['success'], row=speed_position['row'], col=speed_position['col'])
            elif 35 <= time_since_last_cartridge < 45:
                fig.update_traces(marker_color=colors['warning'], row=speed_position['row'], col=speed_position['col'])
            else:
                fig.update_traces(marker_color=colors['danger'], row=speed_position['row'], col=speed_position['col'])

            # Set title and default font size
            fig.update_layout(title=line + ' ' + scope + ' Cartridges',
                              title_x=0.5,
                              font=dict(
                                  size=18,
                                  color=colors['text']),
                              uniformtext_minsize=98,
                              uniformtext_mode='show',
                              showlegend=False)
            return fig


if __name__ == '__main__':
    # Configure base logger object
    logging.basicConfig(filename='logfile.txt',
                        format=u'%(asctime)s - %(levelname)s - [%(name)s]: %(message)s',
                        filemode='w',
                        level=logging.ERROR
                        )

    # Create a logging object
    logger = logging.getLogger()

    try:
        # Get the commands introduced once running the script
        command = sys.argv[1]
        # Save the exceptions into the logfile
    except IndexError as e:
        # Assign default value for the command line
        command = '2'
        print('Not introduced any command for the python script execution')
        print(f'Using the default command = {command}')

    try:
        commands = {'1': {'line': 'SSL1',
                          'kind': 'Started',
                          'port': 8000},
                    '2': {'line': 'SSL1',
                          'kind': 'Finished',
                          'port': 8001},
                    '3': {'line': 'SSL3',
                          'kind': 'Started',
                          'port': 8002},
                    '4': {'line': 'SSL3',
                          'kind': 'Finished',
                          'port': 8003}}

        line = commands[command]['line']
        kind = commands[command]['kind']
        port = commands[command]['port']

        print('Running ' + line + ' ' + kind + ' LINES VISUALIZER')
        WebApp(line, kind).app.run_server('0.0.0.0', port, debug=False)

    except Exception as e:
        # Save in logger file
        print('Not introduced any command for the python script execution')
        logger.error('Error: {}'.format(e), exc_info=True)
