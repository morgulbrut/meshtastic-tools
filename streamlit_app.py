import streamlit as st
import folium
from streamlit_folium import st_folium
import rangetest

st.set_page_config(
    page_title='Meshtatic Tools',
    page_icon=':rocket:',  # This is an emoji shortcode. Could be a URL too.
    layout='wide'
)

# pg = st.navigation([st.Page("map.py"), st.Page("hello.py")])

# pg.run()

# tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
#     ["Rangetest Visualizer", "Tab 2", "Tab 3", "Tab 4", "Tab 5", "Tab 6", "Tab 7", "Tab 8"]
# )

st.title("Meshtatic Tools")

tab1, tab2 = st.tabs(
    ["Readme", "Rangetest Visualizer"]
)

with tab1:
    with open("README.md", "r") as f:
        st.markdown(f.read())

with tab2:
    rangetest.show()
