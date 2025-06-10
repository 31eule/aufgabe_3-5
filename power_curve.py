import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

def load_activity_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    df["Time"] = np.arange(len(df))

    return df

def create_powercurve(df, windows_sizes):
    power_values = []
    for window in windows_sizes:
        power = find_best_effort(df, window)
        power_values.append(power)

    return power_values

def find_best_effort(series, windows_size):
    rolling_power = series.rolling(window=windows_size).mean()
    best_effort = rolling_power.max()

    return best_effort

def plot_powercurve(time, power_values):
    df_new = pd.DataFrame({'Time' : time, 'Power' : power_values})
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_new["Time"],
        y=df_new["Power"],
        mode="lines+markers",
        name="Best Effort Power",
        line=dict(color="blue", width=2),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title="Power Curve",
        xaxis_title="Time (seconds)",
        yaxis_title="Power (Watts)",
        xaxis=dict(tickmode='linear', dtick=300),
        yaxis=dict(range=[150, max(power_values) * 1.1]),
        template="plotly_white"
    )

    fig.show()
    return fig


if __name__ == "__main__":
    df = load_activity_data("data/activities/activity.csv")
    series = pd.Series(df["PowerOriginal"])
    windows_size = 300
    watts300 = find_best_effort(series, windows_size)
    windows_sizes = [5, 50, 150, 300, 500, 700, 900, 1200, 1500, 1800]
    watts = create_powercurve(series, windows_sizes)
    print(plot_powercurve(windows_sizes, watts))