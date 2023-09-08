from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)
server = app.server

app.title = "MCM7003 Data Visualization Demo"

df = pd.read_csv('https://raw.githubusercontent.com/AsifTamoso/kpop/main/kpop_idols_boy_groups.csv')
dfGirl = pd.read_csv('https://raw.githubusercontent.com/AsifTamoso/kpop/main/kpop_idols_girl_groups.csv')

# Create a Plotly Express scatter plot for boys group
def create_scatter_plot(x_column, y_column):
    fig1 = px.scatter(df, x=x_column, y=y_column)
    fig1.update_layout(
        title=f'{x_column} Vs {y_column} Boys Group',
        xaxis_title=x_column,
        yaxis_title=y_column
    )
    return fig1

# Create a Plotly Express box plot for boys group
fig2 = px.box(df, x='Orig. Memb.', y='Active', title='Boyband Status')

# Create a Plotly Express box plot for girls group
fig3 = px.box(dfGirl, x='Orig. Memb.', y='Active', title='Girlband Status')

app.layout = html.Div(
    [
        html.H1("Data Visualization KPOP Project"),
        
        dcc.Tabs([
            dcc.Tab(label='Members Vs Orig. Memb. Boys Group', children=[
                dcc.Graph(figure=fig1),
                html.Label("Select X-axis Column"),
                html.Br(),
                dcc.Dropdown(
                    id='scatter-x-axis-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value='Members'
                ),
                html.Label("Select Y-axis Column"),
                dcc.Dropdown(
                    id='scatter-y-axis-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value='Orig. Memb.'
                ),
                dcc.Graph(id='scatter-plot')  # Interactive scatter plot
            ]),
            dcc.Tab(label='Boyband Status', children=[
                html.Br(),
                html.Label("Select Range for X-Axis"),
                dcc.RangeSlider(
                    id='x-axis-range-slider',
                    min=df['Orig. Memb.'].min(),
                    max=df['Orig. Memb.'].max(),
                    step=1,
                    marks={str(i): str(i) for i in range(int(df['Orig. Memb.'].min()), int(df['Orig. Memb.'].max())+1)},
                    value=[df['Orig. Memb.'].min(), df['Orig. Memb.'].max()]
                ),
                dcc.Graph(id='boyband-box-plot', figure=fig2)
            ]),
            dcc.Tab(label='Girlband Status', children=[
                dcc.Graph(figure=fig3),
                # Add interactive components for this tab here
            ]),
        ])
    ]
)

# Callback to update the scatter plot based on user inputs
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatter-x-axis-dropdown', 'value'),
    Input('scatter-y-axis-dropdown', 'value')
)
def update_scatter_plot(x_column, y_column):
    return create_scatter_plot(x_column, y_column)

# Callback to update the box plot based on user-selected range
@app.callback(
    Output('boyband-box-plot', 'figure'),
    Input('x-axis-range-slider', 'value')
)
def update_box_plot(x_range):
    updated_fig = px.box(
        df, 
        x='Orig. Memb.', 
        y='Active',
        title='Boyband Status',
        range_x=x_range
    )
    return updated_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8065)
