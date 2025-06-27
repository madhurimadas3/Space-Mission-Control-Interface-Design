# src/app.py

import dash
from dash import html, dcc
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Mission Control Interface"),
    
    dcc.Graph(
        id='orbit-plot',
        figure=go.Figure().update_layout(
            title="Orbital Path Placeholder",
            xaxis_title="X Position (km)",
            yaxis_title="Y Position (km)"
        )
    ),
    
    html.Div(id='telemetry', children="Simulated telemetry will appear here.")
])

if __name__ == "__main__":
    app.run(debug=True)
