# src/app.py
import time
from dash import Dash, html, dcc, Input, Output, State, dash_table
import plotly.graph_objects as go

from sim.orbit import orbit_state
from sim.telemetry import telemetry_state
from sim.commands import CommandBuffer

app = Dash(__name__)
server = app.server

t0 = time.time()
cmd_buf = CommandBuffer()

# --- Build a static orbit map (Earth background) ---
def make_orbit_base_fig():
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=[0],
        lat=[0],
        mode="markers",
        marker=dict(size=8, color="red"),
        name="Satellite"
    ))
    fig.update_geos(
        projection_type="equirectangular",
        showcountries=True,
        showcoastlines=True,
        lataxis_range=[-90, 90],
        lonaxis_range=[-180, 180]
    )
    fig.update_layout(
        dragmode=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    return fig

# Static base figure
orbit_base_fig = make_orbit_base_fig()

# --- Layout ---
app.layout = html.Div([
    html.H2("Mission Control Dashboard (Concept)"),

    dcc.Interval(id="tick", interval=1000, n_intervals=0),

    html.Div([
        html.Div([
            html.H4("Orbit Visualization"),
            dcc.Graph(id="orbit-fig", figure=orbit_base_fig)
        ], style={"flex": 2, "padding": "0.5rem"}),

        html.Div([
            html.H4("Telemetry"),
            html.Div(id="telemetry-box"),
            html.H4("Alerts"),
            html.Ul(id="alerts-box")
        ], style={"flex": 1, "padding": "0.5rem"})
    ], style={"display": "flex"}),

    html.Div([
        html.H4("Command Input"),
        dcc.Input(id="cmd-input", type="text", placeholder="e.g. POINT_TO 45 -93", style={"width": "60%"}),
        html.Button("Send", id="cmd-send"),
    ], style={"padding": "0.5rem"}),

    html.Div([
        html.H4("Command History"),
        dash_table.DataTable(
            id="cmd-table",
            columns=[
                {"name": "time", "id": "time"},
                {"name": "cmd", "id": "cmd"},
                {"name": "args", "id": "args"},
            ],
            data=[]
        )
    ], style={"padding": "0.5rem"})
])

# --- Callbacks ---
@app.callback(
    Output("orbit-fig", "figure"),
    Output("telemetry-box", "children"),
    Output("alerts-box", "children"),
    Output("cmd-table", "data"),
    Input("tick", "n_intervals")
)
def update(n):
    t_s = n
    orb = orbit_state(t_s)
    tel = telemetry_state(t_s)

    # Update marker position
    fig = orbit_base_fig.to_dict()  # Make a fresh copy
    fig = go.Figure(fig)
    fig.data[0].lon = [orb["lon"]]
    fig.data[0].lat = [orb["lat"]]


    # Telemetry
    telem_html = [
        html.Div(f"Lat: {orb['lat']:.2f}°, Lon: {orb['lon']:.2f}°, Alt: {orb['alt_km']} km"),
        html.Div(f"Attitude r/p/y: {tel['attitude']['roll']:.1f}, {tel['attitude']['pitch']:.1f}, {tel['attitude']['yaw']:.1f}"),
        html.Div(f"SoC: {tel['power']['soc']:.1f}% | Gen: {tel['power']['gen_w']:.0f} W"),
        html.Div(f"Ground contact: {'Yes' if tel['link']['in_contact'] else 'No'}")
    ]

    # Alerts
    alerts = []
    if tel["power"]["soc"] < 45.0:
        alerts.append("Low battery")
    if not tel["link"]["in_contact"]:
        alerts.append("No ground link")
    alerts_html = [html.Li(a) for a in alerts] if alerts else [html.Li("None")]

    return fig, telem_html, alerts_html, cmd_buf.as_rows()


@app.callback(
    Output("cmd-input", "value"),
    Input("cmd-send", "n_clicks"),
    State("cmd-input", "value"),
    prevent_initial_call=True
)
def send_cmd(n, value):
    if value:
        parts = value.split()
        cmd = parts[0]
        args = {"args": parts[1:]}
        cmd_buf.push(cmd, args)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
