import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        self.ekg_dict = ekg_dict
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
    
    @staticmethod
    def load_by_id(ekg_list, target_id):
        for ekg in ekg_list:
            if int(ekg["id"]) == int(target_id):  # <- sicherer Vergleich
                return ekg
        return None

    
    
    def find_peaks(self, threshold, respacing_factor=5):
        """
        A function to find the peaks in a series
        Args:
            - series (pd.Series): The series to find the peaks in
            - threshold (float): The threshold for the peaks
            - respacing_factor (int): The factor to respace the series
        Returns:
            - peaks (list): A list of the indices of the peaks
        """
        # Respace the series
        series_df = self.df["Messwerte in mV"]

        series = series_df.iloc[::respacing_factor]
        
        # Filter the series
        series = series[series>threshold]


        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index-respacing_factor)

        return peaks

    @staticmethod
    def estimate_hr(peaks):
        if len(peaks) < 2:
            return 0  # Nicht genug Daten für Berechnung

        rr_intervals_ms = [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)]
        mean_rr_ms = sum(rr_intervals_ms) / len(rr_intervals_ms)
        mean_rr_sec = mean_rr_ms / 1000.0
        hr = 60 / mean_rr_sec
        return hr
    
    def plot_time_series(self, peaks):
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df["Zeit in ms"].head(2000),
            y=self.df["Messwerte in mV"].head(2000),
            mode='lines',
            name='EKG Daten',
            line=dict(color='blue', width=2)
        ))

        peak_indices = [i for i in peaks if i < 2000]
        fig.add_trace(go.Scatter(
            x=self.df["Zeit in ms"].iloc[peak_indices],
            y=self.df["Messwerte in mV"].iloc[peak_indices],
            mode='markers',
            name='Peaks',
            marker=dict(color='red', size=8, symbol='circle')
        ))
        fig.update_layout(
            title='EKG Zeitreihe mit Peaks',
            xaxis_title='Zeit in ms',
            yaxis_title='Messwerte in mV',
            template='plotly_white'
        )
        return fig
    
        




if __name__ == "__main__":
    #print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    #print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    #print(ekg.df.head())
    id = 1
    ekg_list = [person_data[0]["ekg_tests"][0], person_data[0]["ekg_tests"][1], person_data[1]["ekg_tests"][0], person_data[2]["ekg_tests"][0]]
    #print(EKGdata.load_by_id(ekg_list, id))
    all_data = EKGdata.load_by_id(ekg_list, id)
    threshold = 340
    peaks = (EKGdata.find_peaks(EKGdata, all_data, threshold))
    #print(EKGdata.find_peaks(EKGdata, all_data, threshold))
    #print(EKGdata.estimate_hr(peaks))
    print(EKGdata.plot_time_series(EKGdata, peaks))

