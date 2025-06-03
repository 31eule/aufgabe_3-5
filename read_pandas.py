import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

def read_my_csv():
    
    df = pd.read_csv("data/activities/activity.csv")

    t_end = len(df)
    time = np.arange(0, t_end)

    df["Time"]=time

    return df

def calculate_zone_times(df, time_interval=1):
    return {f"Zone {i}": df[f"Zone {i}"].sum() * time_interval for i in range(1, 6)}


def make_plot(df):

    hf_min = df["HeartRate"].min()
    hf_max = df["HeartRate"].max()
    zone_1 = hf_max*0.6
    zone_2 = hf_max*0.7
    zone_3 = hf_max*0.8
    zone_4 = hf_max*0.9

    df["Zone 1"] = (df["HeartRate"] <= zone_1)
    df["Zone 2"] = (df["HeartRate"] > zone_1) & (df["HeartRate"] <= zone_2)
    df["Zone 3"] = (df["HeartRate"] > zone_2) & (df["HeartRate"] <= zone_3)  
    df["Zone 4"] = (df["HeartRate"] > zone_3) & (df["HeartRate"] <= zone_4) 
    df["Zone 5"] = (df["HeartRate"] > zone_4)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["HeartRate"],
        mode="lines",
        name="Herzfrequenz",
        line=dict(color="black", width=2),
        yaxis="y1"
    ))

    # Rechte y-Achse: Power
    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["PowerOriginal"],
        mode="lines",
        name="Leistung",
        line=dict(color="purple", width=2, dash="solid"),
        yaxis="y2"
    ))

    # Hintergrund-Zonen definieren
    fig.update_layout(shapes=[
        # Zone 1 (blau)
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=0, y1=zone_1,
            fillcolor="deepskyblue", opacity=0.1, layer="below", line_width=0),
        # Zone 2 (grün)
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=zone_1, y1=zone_2,
            fillcolor="green", opacity=0.1, layer="below", line_width=0),
        # Zone 3 (gelb)
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=zone_2, y1=zone_3,
            fillcolor="yellow", opacity=0.1, layer="below", line_width=0),
        # Zone 4 (rot)
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=zone_3, y1=zone_4,
            fillcolor="red", opacity=0.1, layer="below", line_width=0),
        # Zone 5 (lila)
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=zone_4, y1=df["HeartRate"].max()+50,
            fillcolor="purple", opacity=0.1, layer="below", line_width=0),
    ])

    # Achsen-Layout
    fig.update_layout(
        title="Herzfrequenz & Leistung",
        xaxis_title="Zeit (s)",
        yaxis=dict(
            title="Herzfrequenz (bpm)",
            side="left",
            range=[hf_min - 10, hf_max + 10]
        ),
        yaxis2=dict(
            title="Leistung (Watt)",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend_title="Legende",
        template="plotly_white",
        annotations=[ # Zonenbeschriftung
        dict(x=0.01, xref="paper", y=(zone_1 - 32), yref="y",
             text="Zone 1", showarrow=False, font=dict(color="darkblue", size=12)),
        dict(x=0.01, xref="paper", y=(zone_1 + zone_2) / 2, yref="y",
             text="Zone 2", showarrow=False, font=dict(color="green", size=12)),
        dict(x=0.01, xref="paper", y=(zone_2 + zone_3) / 2, yref="y",
             text="Zone 3", showarrow=False, font=dict(color="orange", size=12)),
        dict(x=0.01, xref="paper", y=(zone_3 + zone_4) / 2, yref="y",
             text="Zone 4", showarrow=False, font=dict(color="orangered", size=12)),
        dict(x=0.01, xref="paper", y=(zone_4 + 205) / 2, yref="y",
             text="Zone 5", showarrow=False, font=dict(color="firebrick", size=12))
        ]
    )

    fig.update_layout(
        legend=dict(
            x=1.10,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    return fig

def calculate_summary(df):
    power_mean = df["PowerOriginal"].mean()
    power_max = df["PowerOriginal"].max()
    
    # Zeiten in Minuten pro Zone
    zone_times = {f"Zone {i}": df[f"Zone {i}"].sum() / 60 for i in range(1, 6)}
    
    # Durchschnittliche Power pro Zone
    power_means = {}
    for i in range(1, 6):
        zone_mask = df[f"Zone {i}"]
        if zone_mask.any():
            power_means[f"Zone {i}"] = df.loc[zone_mask, "PowerOriginal"].mean()
        else:
            power_means[f"Zone {i}"] = 0.0
    
    return {
        "power_mean": power_mean,
        "power_max": power_max,
        "zone_times": zone_times,
        "power_means": power_means
    }

if __name__== "__main__":
    df = read_my_csv()
    fig = make_plot(df)
    fig.show()