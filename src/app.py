import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('nashville_crashes.csv')

# Sort the unique crash types alphabetically
sorted_types = sorted(df['Type'].unique())

# Convert the 'Type' column to a categorical data type with a defined category order
df['Type'] = pd.Categorical(df['Type'], categories=sorted_types, ordered=True)

# Create a color map for crash types
#color_map = {type_: px.colors.qualitative.Plotly[i] for i, type_ in enumerate(sorted_types)}
color_map = {type_: px.colors.qualitative.Safe[i] for i, type_ in enumerate(sorted_types)}

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    html.H1(
        children='Nashville Crash Data Visualization',
        style={'fontFamily': 'sans-serif'}
    ),

    # RangeSlider for selecting date range
    dcc.RangeSlider(
        id='date-range-slider',
        min=df['DateStamp'].min(),
        max=df['DateStamp'].max(),
        step=2629800,  # One day in seconds
        value=[df['DateStamp'].min(), df['DateStamp'].max()],
        marks={int(timestamp): str(pd.to_datetime(timestamp, unit='s').date()) 
               for timestamp in range(int(df['DateStamp'].min()), int(df['DateStamp'].max()), 86400 * 365)}  # Mark every 30 days
    ),

    dcc.Graph(id='crash-data-scatter')
])

# Callback to update the graph based on selected crash type and date range
@app.callback(
    Output('crash-data-scatter', 'figure'),
    [Input('date-range-slider', 'value')]
)
def update_graph(selected_date_range):

    # Filter the dataframe based on the selected type and date range
    filtered_df = df[df['DateStamp'].between(*selected_date_range)]

    # Update the scatter plot
    fig = px.scatter(filtered_df,
                     x='Long', 
                     y='Lat', 
                     color='Type', 
                     color_discrete_map=color_map,
                     labels={"Type":"Crash Type (Safe Colors)"},
                     category_orders={
                         "Type": ["Angle",
                                  "Front to Rear",
                                  "Head to Head",
                                  "Non-Collision",
                                  "Rear to Rear",
                                  "Rear to Side",
                                  "Swipe, Same Side",
                                  "Swipe, Opposite Sides",
                                  "Other",
                                  "Unknown"]
                     })

    fig.update_layout(
        autosize=False,
        width=1400,
        height=800,
        margin=dict(l=50, r=50, b=50, t=50, pad=4),
        plot_bgcolor="#f0f0f0"
    )
    fig.update_xaxes(range=[-87.1, -86.5])

    fig.update_yaxes(range=[36, 36.4])

    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)
