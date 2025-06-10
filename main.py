import streamlit as st
import read_data
import read_pandas
import pandas as pd
from PIL import Image
from person import Person
from ekgdata import EKGdata

st.write("# EKG Data Analysis")
st.write("## Patient/in auswählen")

person_dict = Person.load_person_data()
person_names = Person.get_person_list(person_dict)
person_ids = [p["id"] for p in person_dict]

def get_id_by_name(name):
    for person in person_dict:
        if f"{person['lastname']}, {person['firstname']}" == name:
            return person["id"]
    return None

def get_name_by_id(pid):
    for person in person_dict:
        if person["id"] == pid:
            return f"{person['lastname']}, {person['firstname']}"
    return None

def sync_name():
    st.session_state.current_id = get_id_by_name(st.session_state.current_user)

def sync_id():
    st.session_state.current_user = get_name_by_id(st.session_state.current_id)

if 'current_user' not in st.session_state:
    st.session_state.current_user = person_names[0]
if 'current_id' not in st.session_state:
    st.session_state.current_id = person_ids[0]

col1, col2 = st.columns(2)
with col1:
    st.selectbox(
        "Patient/in",
        options=person_names,
        index=person_names.index(st.session_state.current_user),
        key="current_user",
        on_change=sync_name
    )
with col2:
    st.selectbox(
        "Personen-ID auswählen",
        options=person_ids,
        index=person_ids.index(st.session_state.current_id),
        key="current_id",
        on_change=sync_id
    )

person = Person.load_by_id(st.session_state.current_id, person_dict)

if person:
    try:
        image = Image.open(person.picture_path)
    except FileNotFoundError:
        image = Image.open("data/pictures/none.jpg")
    st.image(image, caption=f"{person.lastname}, {person.firstname}")

    age = person.calc_age()
    max_hr = person.calc_max_heart_rate()
    st.markdown(f"**Alter:** {age} Jahre")
    st.markdown(f"**Maximale Herzfrequenz:** {max_hr:.1f} bpm")

    if person.ekg_tests:
        ekg_ids = [ekg["id"] for ekg in person.ekg_tests]

        # INITIALISIERE selected_ekg_index nur, wenn Person gewechselt hat oder nicht existiert
        if ('current_person_id_for_ekg' not in st.session_state or
            st.session_state.current_person_id_for_ekg != person.id or
            'selected_ekg_index' not in st.session_state):
            st.session_state.current_person_id_for_ekg = person.id
            st.session_state.selected_ekg_index = 0

        # Erstelle die Selectbox, ohne den Session State danach zu überschreiben
        selected_index = st.selectbox(
            "EKG auswählen",
            options=range(len(ekg_ids)),
            index=st.session_state.selected_ekg_index,
            format_func=lambda x: str(x + 1),
            key="selected_ekg_index"
        )

        # Aktualisiere den Index nur, wenn sich die Auswahl ändert (wenn nötig)
        if selected_index != st.session_state.selected_ekg_index:
            st.session_state.selected_ekg_index = selected_index

        selected_ekg_id = ekg_ids[selected_index]
        ekg_dict = EKGdata.load_by_id(person.ekg_tests, selected_ekg_id)

        if ekg_dict:
            ekg = EKGdata(ekg_dict)
            threshold = 340
            peaks = ekg.find_peaks(threshold)
            fig = ekg.plot_time_series(peaks)
            st.plotly_chart(fig)
            estimated_hr = ekg.estimate_hr(peaks)
            st.markdown(f"**Geschätzte Herzfrequenz:** {estimated_hr:.1f} bpm")
            st.markdown(f"**EKG-Datei:** {ekg_dict['result_link']}")
        else:
            st.warning("Kein EKG mit dieser ID gefunden.")
    else:
        st.warning("Keine EKG-Daten für diese Person vorhanden.")
        
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

