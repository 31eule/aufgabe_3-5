# Aufgabe_3-5
Programmieruebung 2 von Katharina und Liliana

# Projekt Streamlit-App
In der Streamlit-App können EKG und Leistungs-Daten von einzelnen Patienten gespeichert. Die Daten werden ausgewertet und als Graphik dargestellt in den fünf Herzfrequenz Zonen. 

Um das Projekt auszuführen, müssen zunächst Python und das Python-Paketverwaltungstool pdm installiert werden (z.B. mit dem Befehl pip install pdm). Anschließend wird das Projekt mit dem Befehl pdm init initialisiert. Dabei gibt man grundlegende Informationen wie Projektname, Version, Beschreibung und Autor an.

Nach der Initialisierung werden die benötigten Abhängigkeiten, wie z. B. streamlit, plotly, numpy, pandas und matplotlib, mit pdm add installiert. Das Projekt wird anschließend von GitHub geklont und man erhält alle notwendigen Dateien.

Die Datei data.csv enthält die gemessenen Leistungsdaten. Diese werden mit der Funktion in read_pandas.py ausgewertet und in einem Plot dargestellt. In der main.py wird der Aufbau der Streamlit-App definiert und es wird auf read_pandas.py zugegriffen, um den Plot und weitere Daten in der Streamlit-App darzustellen.

Nun kann man die Streamlit-App im Browser aufrufen und diese schaut so aus:

![alt text](<Leistungskurve I.png>)