# pylint: disable-all

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

colors = ['purple', 'green', 'darkred', 'blue', 'red']


@st.cache_data
def get_data(file):
    df = pd.read_csv(file)
    df = df[df['rx lat'].notna()]
    df = df[df['sender lat'].notna()]
    df = df[df['sender name'].notna()]
    return df


def show():
    file = st.file_uploader('Upload a rangetest file', type=['csv'])

    if file:
        data = get_data(file)

        if data is not None:

            st.sidebar.subheader('Rangetest Data')

            min_distance = st.sidebar.slider('Minimum distance (km)', 0, 150, 0, 1)
            data = data[data['distance'] > min_distance * 1000]

            hop_limit = sorted(data['hop limit'].unique())
            selected_hop_limit = st.sidebar.multiselect('Select hop limit', hop_limit)
            if selected_hop_limit:data = data[data['hop limit'].isin(selected_hop_limit)]

            sender_names = sorted(data['sender name'].unique())
            selected_senders = st.sidebar.multiselect('Select senders', sender_names)
            if selected_senders:
                data = data[data['sender name'].isin(selected_senders)]

            data['max distance'] = data.groupby('sender name')['distance'].transform('max')
            data['sender count'] = data.groupby('sender name')['sender name'].transform('count')

            st.sidebar.subheader("Best senders")
            st.sidebar.write(f"Longest distance: {data['distance'].max()/1000:.2f} km")
            st.sidebar.write(f"Most seen sender: {data['sender name'].mode()[0]}")

            m = folium.Map(location=[data['sender lat'].mean(), data['sender long'].mean()], zoom_start=10)

            drawn_sender = []
            col_indx = 0

            for i, row in data.iterrows():
                if row['sender name'] not in drawn_sender:
                    drawn_sender.append(row['sender name'])
                    sender = row['sender name']

                    html = f"<b>{sender}</b> <p>Max: {row['max distance']/1000} km<br>Count: {int(row['sender count'])}</p>"
                    putext = folium.IFrame(html)
                    pu = folium.Popup(putext,
                                      min_width=200,
                                      max_width=300)
                    folium.Marker(
                        [row['sender lat'], 
                         row['sender long']], 
                         popup=pu, 
                         tooltip=row['sender name'], 
                         icon=folium.Icon(
                            color=colors[col_indx])
                    ).add_to(m)

                    if len(selected_senders) > 0 or min_distance > 10:
                        for i, row in data[data['sender name'] == sender].iterrows():
                            folium.PolyLine(
                                locations=[(row['sender lat'], row['sender long']),
                                           (row['rx lat'], row['rx long'])],
                                color=colors[col_indx],
                                weight=10,
                                opacity=0.2,
                                tooltip=f"{row['distance']/1000} km"
                            ).add_to(m)
                    col_indx = (col_indx + 1) % len(colors)

            # call to render Folium map in Streamlit
            st_data = st_folium(m, width=1980, height=1080)
