import streamlit as st
import read_data 
import pandas as pd
import read_pandas
from PIL import Image

from person import Person
from ekgdata import EKGdata


st.write("# EKG Data Analysis")
st.write("## Patient/in auswählen")

if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

person_dict = Person.load_person_data()
person_names = Person.get_person_list(person_dict)

person_id = st.text_input("Personen-ID eingeben:")

# Personendaten anhand der ID laden und anzeigen
if person_id:
    all_persons = Person.load_person_data()
    person_data_by_id = Person.load_by_id(person_id, all_persons)
    if person_data_by_id:
        st.markdown("**Personendaten (per ID):**")
        st.json(person_data_by_id)
        # Optional: Instanz erzeugen und weitere Infos anzeigen
        person_by_id = Person(person_data_by_id)
        age_by_id = person_by_id.calc_age(person_by_id)
        st.markdown(f"**Alter:** {age_by_id} Jahre")
    else:
         st.warning("Keine Person mit dieser ID gefunden.")

st.session_state.current_user = st.selectbox(
    'Patient/in',
    options = person_names, key="sbPatient")

# Anlegen des Session State. Bild, wenn es kein Bild gibt
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

# Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
if st.session_state.current_user in person_names:
    st.session_state.picture_path = Person.find_person_data_by_name(st.session_state.current_user)["picture_path"]
    
# Öffne das Bild und Zeige es an
image = Image.open(st.session_state.picture_path)
st.image(image, caption=st.session_state.current_user)

if st.session_state.current_user in person_names:
    person_data = Person.find_person_data_by_name(st.session_state.current_user)
    person = Person(person_data)
    age = person.calc_age(person_data)
    st.markdown(f"**Alter:** {age} Jahre")
    heartrate = person.calc_max_heart_rate(person_data, age)
    st.markdown(f"**Maximale Herzfrquenz:** {heartrate} bpm")


#EKG-Plot einfügen
df = read_pandas.read_my_csv()

# Plot erstellen
fig = read_pandas.make_plot(df)

# Plot anzeigen
st.plotly_chart(fig)

# Darstellung der weiteren Werte 
summary = read_pandas.calculate_summary(df)

st.markdown(f"**Mittelwert Leistung:** {summary['power_mean']:.1f} Watt")
st.markdown(f"**Maximalwert Leistung:** {summary['power_max']:.1f} Watt")

st.markdown("### Leistung und Zeit pro Zone:")

# Tabelle bauen
zone_data = []
for i in range(1, 6):
    zone = f"Zone {i}"
    zone_data.append({
        "Zone": zone,
        "Zeit (min)": f"{summary['zone_times'][zone]:.1f}",
        "Durchschnittliche Leistung (W)": f"{summary['power_means'][zone]:.1f}"
    })

df_zone_summary = pd.DataFrame(zone_data)

# Index-Spalte entfernen
st.table(df_zone_summary.set_index("Zone"))
