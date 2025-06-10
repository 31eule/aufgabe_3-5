import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

def load_activity_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Time"] = np.arange(len(df))  # 1 Hz: jede Zeile = 1 Sekunde
    return df

def find_best_effort(series, window_size):
    rolling_power = series.rolling(window=window_size).mean()
    best_effort = rolling_power.max()
    return best_effort

def create_powercurve(series, durations_seconds):
    power_values = []
    for duration in durations_seconds:
        power = find_best_effort(series, duration)  # 1 Sample = 1 Sekunde
        power_values.append(power)
    return power_values

def plot_powercurve(durations_seconds, power_values):
    df_new = pd.DataFrame({'Duration (s)' : durations_seconds, 'Power (W)' : power_values})
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_new["Duration (s)"],
        y=df_new["Power (W)"],
        mode="lines+markers",
        name="Best Effort Power",
        line=dict(color="blue", width=2),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title="Power Curve",
        xaxis_title="Zeit (Sekunden)",
        yaxis_title="Power (Watts)",
        xaxis=dict(tickmode='linear', dtick=300),
        yaxis=dict(range=[min(power_values) * 0.9, max(power_values) * 1.1]),
        template="plotly_white"
    )
    fig.show()
    return fig

if __name__ == "__main__":
    df = load_activity_data("data/activities/activity.csv")
    series = pd.Series(df["PowerOriginal"])

    # Diese Werte sind sowohl in Sekunden als auch in Samples gültig, da 1Hz
    durations_seconds = [5, 30, 60, 120, 300, 600, 900, 1200, 1500, 1800]

    watts = create_powercurve(series, durations_seconds)
    plot_powercurve(durations_seconds, watts)